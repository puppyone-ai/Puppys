from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
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
    
    def checkDo(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-turbo-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey
        """
        write code to achieve the action
        """
        print("checking")

        from prompt.actionFlowPrompt import ActionCheckDone

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        checkIfActionIsDone=LLMChain(llm=llm, prompt= ActionCheckDone)

        self.codeThreadInstance.functionsDescriptionAndExample= self.codeThreadInstance.sendMessageToHuman.getDescriptionAndExample()

        newCode=checkIfActionIsDone.predict(puppyName=self.codeThreadInstance.puppyName,
                                               goal=self.codeThreadInstance.goal,
                                                current_action=self.codeThreadInstance.actionFlow.actionFlowCurrentGetFront()["action"],
                                                code_history=self.codeThreadInstance.actionFlow.actionFlowHistoryGetCode(),
                                                code_future=self.codeThreadInstance.actionFlow.actionFlowPendingGetCode(),
                                                enviroment=self.codeThreadInstance.environment,
                                                knowledge=self.codeThreadInstance.knowledge.getKnowledgeStr())
                                                

        newCode=newCode.replace("```python\n", "").replace("\n```", "")

        print("\n")
        print("++++++++++++++++++ Checking Code Start +++++++++++++++++++")
        print(newCode)
        print("+++++++++++++++++++ Checking Code End ++++++++++++++++++++")
        print("\n")


        return newCode

    
    def do(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-turbo-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey
        """
        write code to achieve the action
        """

        continueAction= self.checkDo()
        exec(continueAction,self.codeThreadInstance.codeThreadVars)

        if self.codeThreadInstance.codeThreadVars["finishedOrNot"]==True:
            self.codeThreadInstance.actionFlow.actionFlowCurrentJSON.pop(0)
            print("afterchecking:*****",self.codeThreadInstance.actionFlow.actionFlowCurrentJSON)

        elif self.codeThreadInstance.codeThreadVars["finishedOrNot"]==False:

            print("afterchecking:*****",self.codeThreadInstance.actionFlow.actionFlowCurrentJSON)

    
            from prompt.actionFlowPrompt import ActionDo

            llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
            fillingActionParameter=LLMChain(llm=llm, prompt= ActionDo)


            self.codeThreadInstance.functionsDescriptionAndExample= self.codeThreadInstance.sendMessageToHuman.getDescriptionAndExample()


            newCode=fillingActionParameter.predict(puppyName=self.codeThreadInstance.puppyName,
                                                goal=self.codeThreadInstance.goal,
                                                    current_action=self.codeThreadInstance.actionFlow.actionFlowCurrentGetFront()["action"],
                                                    current_action_Python= self.codeThreadInstance.actionFlow.actionFlowCurrentGetCode(),
                                                    code_history=self.codeThreadInstance.actionFlow.actionFlowHistoryGetCode(),
                                                    code_future=self.codeThreadInstance.actionFlow.actionFlowPendingGetCode(),
                                                    enviroment=self.codeThreadInstance.environment,
                                                    function_description_and_example=self.codeThreadInstance.functionsDescriptionAndExample,
                                                    knowledge=self.codeThreadInstance.knowledge.getKnowledgeStr())
                                                    

            newCode=newCode.replace("```python\n", "").replace("\n```", "")

            print("\n")
            print("++++++++++++++++++ Generated Code Start +++++++++++++++++++")
            print(newCode)
            print("+++++++++++++++++++ Generated Code End ++++++++++++++++++++")
            print("\n")

            self.codeThreadInstance.actionFlow.actionFlowCurrentAddToFront(self.codeThreadInstance.actionFlow.decorateActionFlowCodeToJSON(newCode,status="fixed"))

    def reflect(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey
        """
        reflect if the action is done or not.
        """
        
        from prompt.actionFlowPrompt import ActionReflect


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