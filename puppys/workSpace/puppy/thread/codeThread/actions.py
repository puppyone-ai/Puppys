from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from openai import OpenAI
from openai import OpenAI
import os

class Actions():
    def __init__(self, codeThreadInstance):
        self.codeThreadInstance = codeThreadInstance
        self.actionList=[{"name":"do",
                            "code":"",
                            "function_before_action":[],
                            "function_after_action":[],}]
        
    # add a new action to the action list
    def actionAdd(self,name,code,function_before_action,function_after_action):
        action={"name":name,
                "code":code,
                "function_before_action":function_before_action,
                "function_after_action":function_after_action,}
        self.actionList.update(action)

    # opreations for actions
    def actionGet(self):
        return self.actionList
    
    # remove an action from the action list
    def actionRemove(self,action):
        self.actionList.pop(action)

    # clear the action list
    def actionClear(self):
        self.actionList={}

    # every action should be wrapped by this function
    def actionWrapper(self, func):
        def wrapper(*args, **kwargs):
            print("Before action:")
            for function in self.actionList[func.__name__]["function_before_action"]:
                function()
                exec(function)

            result = func(*args, **kwargs)

            print("After action")
            for function in self.actionList[func.__name__]["function_before_action"]:
                function()
                exec(function)

            return result

    
    def addNewAction(self,action):
        self.actionList.append(action)


    def addFunctionBeforeActionFront(self,function,action):
        for e in self.actionList:
            if e["action"]==action:
                e["function_before_action"].insert(0,function)
    
    def addFunctionBeforeActionEnd(self,function,action):
        for e in self.actionList:
            if e["action"]==action:
                e["function_before_action"].append(function)

    def addFunctionAfterActionFront(self,function,action):
        for e in self.actionList:
            if e["action"]==action:
                e["function_after_action"].insert(0,function)

    def addFunctionAfterActionEnd(self,function,action):
        for e in self.actionList:
            if e["action"]==action:
                e["function_after_action"].append(function)


    def getFunctionBeforeAction(self,action):
        return self.actionList[action]["function_before_action"]
    
    def getFunctionAfterAction(self,action):
        return self.actionList[action]["function_after_action"]
        
    def thinkKeepGoingOrNot(self):
        pass
    
    def checkDo(self,temperature=0.1,max_token_num=4096,model_name="gpt-4-turbo-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey
        """
        write code to achieve the action
        """
        print("checking")

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ApiKey))
        
        self.codeThreadInstance.functionsDescriptionAndExample= self.codeThreadInstance.sendMessageToHuman.getDescriptionAndExample()

        # prompt for actionDo ***********************************************************************************************
        prompt=[
        # 1. define your agent type and name
        {"role": "system",
        "content":f"""You are an AI code assistant agent called {self.codeThreadInstance.puppyName}. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code. for example: # Hello, I am an assistant.
        DONT'T ASSUME you know any unclear knowledge or information that you don't know. DON'T ASSUME that you have unexsited functions or hypothetical function. Your code will be run imediately after you write it. If you assume any hypothetical function, the the system will crash.
        You need to justify if your current action has been achieved or not by history code, and decide to skip the current action or not.
        You only need to decide if your current action has been achieved or not. You don't need to write code to achieve it."""},

        # 2. provide the goal, current action, code history, code future, enviroment, knowledge
        {"role": "system", 
        "content":f"""
        You have an overall long-term goal: {self.codeThreadInstance.goal},  now you need to write python code to finish your next action:
        {self.codeThreadInstance.actionFlow.actionFlowCurrentGetFront()["action"]}

        The code for historical actionflow shown as code are:
        {self.codeThreadInstance.actionFlow.actionFlowHistoryGetCode()}
                            
        user have already write some code for this action, but it's not finished. You should replace the XXX.do() part. Don't keep the .do() function after your response. The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.:
        {self.codeThreadInstance.actionFlow.actionFlowCurrentGetCode()}
                            
        The code of action in the future are(But you don't need to do this part now, just for your information)):
        {self.codeThreadInstance.actionFlow.actionFlowPendingGetCode()}

        And the current enviroment shown as Python code are(sometimes there is something important):
        {self.codeThreadInstance.environment}

        Here are the knowledge you have learned:
        {self.codeThreadInstance.knowledge.getKnowledgeStr()}"""},

        # 3. set the standard of if the action is done or not
        {"role": "system",
        "content":f"""

        You jutisfy if your current action is done or not, you have two choices:
        1. Done: That means you don't need to write code to achieve it again. The action history shows that you have already know what you want to know or have already achieve the action. In this case, you should write Python code to return Ture, and your generated code should be:
        finishedOrNot=True

        2. Unfinished: That means you need to write code to achieve it again, or their is some unfinished action that you need to make . In this case, you should write Python code to return False, and the your generated code should be:
        finishedOrNot=False

        for example:
        1. the latest action in the action history: 
        ## 发信息给我妈妈 @ask for help
        # Since I don't have any information about the user's mother or the content of the message, I need to ask the user for help.
        message_content = XiaoMei.askHumanForHelp.run("What message would you like to send to your mom?")
        # the user claimed that the message is "I love you mom"
        
        your response:
        # the action is not done, because I get what I should send, but I haven't send it yet. Maybe next action is to send it
        finishedOrNot=False

        2. current action:
        ## get what happened about COVID in the the 2nd Feb 2020 @google search
        # I need to search the information about what happened in the the 2nd Feb 2020. The function returns as a string.
        result=google_search("What happened in the the 2nd Feb 2020")
        # the result is "First death resulting from Coronavirus outside China reported."

        your response:
        # I get what I should get, and I don't need to do anything else if their is no other action provide by human.
        finishedOrNot=True"""},

        # 4. justfy if the action is done or not
        {"role": "user",
        "content":f"""
        Now you need to write code to justify if the action of {self.codeThreadInstance.actionFlow.actionFlowCurrentGetFront()["action"]} is done or not. 
        """}
        ]

        # prompt finished **************************************************************************************************

        completion = client.chat.completions.create(
            model=model_name,
            messages=prompt,
            temperature=0.1,
            max_tokens=max_token_num,
            n=1,
            )

        # return the output code
        newCode=completion.choices[0].message.content


        newCode=newCode.replace("```python\n", "").replace("\n```", "")

        print("\n")
        print("++++++++++++++++++ Checking Code Start +++++++++++++++++++")
        print(newCode)
        print("+++++++++++++++++++ Checking Code End ++++++++++++++++++++")
        print("\n")


        return newCode

    
    def do(self,temperature=0.1,max_token_num=4096,model_name="gpt-4-turbo-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey
        """
        write code to achieve the action
        """

        continueAction= self.checkDo()
        exec(continueAction,self.codeThreadInstance.codeThreadVars)

        if self.codeThreadInstance.codeThreadVars["finishedOrNot"]==True:
            self.codeThreadInstance.actionFlow.actionFlowCurrentJSON.pop(0)

        elif self.codeThreadInstance.codeThreadVars["finishedOrNot"]==False:


            self.codeThreadInstance.functionsDescriptionAndExample= self.codeThreadInstance.sendMessageToHuman.getDescriptionAndExample()

            client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ApiKey))


            # prompt for actionDo ***********************************************************************************************
            prompt=[
            # 1. define your agent type and name
            {"role": "system", 
            "content": f"""
            You are an AI code assistant agent called {self.codeThreadInstance.puppyName}. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code. for example: # Hello, I am an assistant.
            DONT'T ASSUME you know any unclear knowledge or information that you don't know. DON'T ASSUME that you have unexsited functions or hypothetical function. Your code will be run imediately after you write it. If you assume any hypothetical function, the the system will crash.
            If you cannot do the action, you are allowed to addmit it and send message to user. You are not always assume that you can do it."""},
            

            # 2. provide the goal, current action, code history, code future, enviroment, knowledge
            {"role": "system", 
            "content":f"""
            You have an overall goal: {self.codeThreadInstance.goal},  now you need to write python code to finish your next action:
            {self.codeThreadInstance.actionFlow.actionFlowCurrentGetFront()["action"]}

            The code for historical actionflow shown as code are:
            {self.codeThreadInstance.actionFlow.actionFlowHistoryGetCode()}
                                
            user have already write some code for this action, but it's not finished. You should replace the XXX.do() part. Don't keep the .do() function after your response. The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.:
            {self.codeThreadInstance.actionFlow.actionFlowCurrentGetCode()}
                                
            The code of action in the future are(But you don't need to do this part now, just for your information)):
            {self.codeThreadInstance.actionFlow.actionFlowPendingGetCode()}

            And the current enviroment shown as Python code are(sometimes there is something important):
            {self.codeThreadInstance.environment}"""},
            
            
            # 3. provide the functions description and example, and knowledge
            {"role": "system", 
            "content":f"""
            You are allowed to use the given functions below. But make sure that you have imoprted the given package.
            There maybe XXX.do() appearing, The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.
            Pay attention to name your parameter in your code. The naming convention in your code should not be arbitrary, like 'result' or 'response'. It should reflect the property of the parameter.
            
            Your customized functions and their examples are:
            {self.codeThreadInstance.functionsDescriptionAndExample}

            Here are the knowledge you have learned:{self.codeThreadInstance.knowledge.getKnowledgeStr()}
            
            Try to understand the meaning of each function and its parameter, and decide the best function and use the function for this step to accomplish the action. 
            For example: (current action: search the location of the NBA in 2019)
            response:
            ## search the location of the NBA in 2019 @google search @zhihu search
            # Hello! to answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
            location=google_search("Where is the NBA in 2019")"""},

            # 4. provide the code of the action
            {"role": "user",
            "content":f"""

            Now you write code to achieve your action: {self.codeThreadInstance.actionFlow.actionFlowCurrentGetFront()["action"]}
            DONT'T ASSUME you know the knowledge that you don't know. DON'T ASSUME that you have unexsited functions or hypothetical function, and you can show your thinking and reason in the comment. But don't write any code calling undefined functions in this case.
            make sure that the parameter in your respond code follow the type of the parameter in the function instruction. .
            You are NOT allowed to write {self.codeThreadInstance.puppyName}.do() in your final response as code. When the {self.codeThreadInstance.puppyName}.do() appears, you HAVE TO change it to other code.
            your response should be similiar with the example(ONLY CODE) and NOTHING ELSE.
            """}]

            # prompt finished **************************************************************************************************

            completion = client.chat.completions.create(
            model=model_name,
            messages=prompt,
            temperature=0.1,
            max_tokens=max_token_num,
            n=1,
            )

            # return the output code
            newCode=completion.choices[0].message.content
            

            newCode=newCode.replace("```python\n", "").replace("\n```", "")

            print("\n")
            print("++++++++++++++++++ Generated Code Start +++++++++++++++++++")
            print(newCode)
            print("+++++++++++++++++++ Generated Code End ++++++++++++++++++++")
            print("\n")

            self.codeThreadInstance.actionFlow.actionFlowCurrentAddToFront(self.codeThreadInstance.actionFlow.decorateActionFlowCodeToJSON(newCode,status="fixed"))

    def reflect(self,temperature=0.1,max_tokens=4096,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey
        """
        reflect if the action is done or not.
        """
        
        from promptTemplete.actionFlowPrompt import ActionReflect


    def codeThreadDoCheckCode(self, code):
        """
        check if the code is valid
        """

        actionFlowJSON,actionFlowPython=self.actionFlow.translatePython(code)
        if actionFlowJSON[0]["action"]==self.actionFlow.actionFlowCurrentGetFront()[0]["action"]:
            actionJSON=True

        if actionFlowPython[0]==self.actionFlow.actionFlowCurrentGetFront()[1]:
            actionPython=True

    def checkIfActionIsDone(self):
        pass