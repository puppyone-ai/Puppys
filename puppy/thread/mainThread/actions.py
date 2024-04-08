import os
from puppy.llm.openAI import OpenAIChat


class Actions:
    def __init__(self,
                 check_prompt: bool = True, plan_prompt: bool = False,
                 **kwargs):

        if "thread_instance" in kwargs:
            thread_instance = kwargs["thread_instance"]
            self.thread_instance = thread_instance

        self.check_prompt = check_prompt
        self.plan_prompt = plan_prompt

        self.actions_list = []

        if "source_code" in kwargs:
            self.pack(kwargs["source_code"])

        """
        actions_list: [actions,actions,actions]
        actions: [action,action,action]
        [
        {"comment": "", "comment+code": "Mei.do()", "status": "changeable"},
        {"comment": "", "comment+code": "",         "status": ""}
        ]
        """

        # could consider introduce the func_name indexing in the future

    def pack(self, source_code: str) -> None:

        """
        Load the action from source code so that we could trigger it in actionflow
        """

        # clean source code

        lines = source_code.split('\n')

        striped_lines = []

        for line in lines[2:]:  # [2:]filter decorator and function name
            line = line.strip()
            if line:
                striped_lines.append(line)

        # load source code to action list sequentially

        for line in striped_lines:

            if '##' in line:
                self.actions_list.append([{"comment": "",
                                         "comment+code": "",
                                          "status": ""}])

                # print(self.action_list[-1])

                self.actions_list[-1][0]["comment"] = line.split('##', 1)[1].strip()
                self.actions_list[-1][0]["comment+code"] += f'{line}\n'

            else:

                self.actions_list[-1][0]["comment+code"] += line + '\n'

        # verify the status of the action

        for actions in self.actions_list:
            for action in actions:

                if ".do()" in action["comment+code"]:
                    if not action["comment"]:
                        action["status"] = "changeable"
                    else:
                        action["status"] = "semi-fixed"

                else:
                    action["status"] = "fixed"

        print(self.actions_list)

    def check_do(self, temperature=0.1, max_tokens=4096, model="gpt-4-0125-preview"):

        """
        write code to achieve the action
        """

        prompt=[
        # 1. define your agent type and name
        {"role": "system",
        "content":f"""You are an AI code assistant agent called {self.thread_instance.puppy_name}. 
        1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code. for example: # Hello, I am an assistant.
        2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately after you write it. If you assume any hypothetical function, the system will crash.
        3. You need to justify if your current action has been achieved or not by history code, and decide to skip the current action or not.
        4. You only need to decide if your current action has been achieved or not. You don't need to write code to achieve it."""},
        
        # 2. set the standard of if the action is done or not
        {"role": "system",
        "content":f"""

        You justify if your current action is done or not, you have two choices:
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
        # I get what I should get, and I don't need to do anything else if there is no other action provide by human.
        finishedOrNot=True"""},

        # 3. provide the goal, current action, code history, code future, environment, knowledge
        {"role": "system", 
        "content":f"""
        You have an overall long-term goal: {self.thread_instance.goal},  and your next action is:
        {self.thread_instance.action_current["comment"]}

        The code for historical actionflow shown as code are:
        {self.thread_instance.actionflow.actionflow_history_get_code()}
                            
        The code of action in the future are(But you don't need to do this part now, just for your information)):
        {self.thread_instance.actionflow.actionflow_pending_get_code()}"""},
        
        # 4. justify if the action is done or not
        {"role": "user",
        "content":f"""
        Now you need to write code to justify if the action of' {self.thread_instance.action_current['comment']} 'is done or not. 
        Your answer is:
        """}
        ]

        if self.check_prompt:
            print("*******checking prompt********")
            print(prompt)

        print("\n")
        print("\U00002705 Checking ********************************************************************")

        new_code = OpenAIChat(prompt=prompt,
                              model=model,
                              temperature=temperature,
                              api_key=os.environ["OPENAI_API_KEY"],
                              max_tokens=max_tokens,
                              printing=True, stream=True)

        new_code = new_code.replace("```python\n", "").replace("\n```", "")

        print("********************************************************************************")

        return new_code

    # TODO
    # modify the code into recursive function
    def do(self,temperature=0.1,max_tokens=4096,model="gpt-4-0125-preview"):

        """
        write code to achieve the action
        """

        continue_action = self.check_do()

        # deliver 'finishedOrNot' to the environment for verification of the final execution.
        exec(continue_action, self.thread_instance.environment)

        if self.thread_instance.environment["finishedOrNot"]:
            # self.thread_instance.actionflow.actionflow_current_JSON.pop(0)
            pass

        elif not self.thread_instance.environment["finishedOrNot"]:

            # prompt for actionDo **************************************************************************************
            prompt = [
            # 1. define your agent type and name
            {"role": "system", 
            "content": f"""
            You are an AI code assistant agent called {self.thread_instance.puppy_name}. 
            1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code. for example: # Hello, I am an assistant.
            2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately after you write it. If you assume any hypothetical function, the the system will crash.
            3. If you cannot do the action, you are allowed to send message to user for help.
            4. Your response cannot only be comment. You HAVE to write codes"""},

            # 2. provide the functions description and example, and knowledge
            {"role": "system", 
            "content":f"""
            You are allowed to use the given functions below. But make sure that you have imported the given package.
            There maybe XXX.do() appearing, The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.
            Pay attention to name your parameter in your code. The naming convention in your code should not be arbitrary, like 'result' or 'response'. It should reflect the property of the parameter.
            
            Your customized functions and their examples are:
            {self.thread_instance.functions_description_and_example}

            
            Try to understand the meaning of each function and its parameter, and decide the best function and use the function for this step to accomplish the action. 
            For example: (current action: search the location of the NBA in 2019@ google search @zhihu search)
            response:
            # Hello! to answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
            location=google_search("Where is the NBA in 2019"
            location= zhihu_search("Where is the NBA in 2019")"""},

            # 3. provide the goal, current action, code history, code future, environment, knowledge

            {"role": "user", 
            "content":f"""
            You have an overall goal: {self.thread_instance.goal},  now you need to write python code to finish your next action:
            {self.thread_instance.action_current['comment']}

            The code for historical actionflow shown as code are:
            {self.thread_instance.actionflow.actionflow_history_get_code()}
                                
            user have already write some code for this action, but it's not finished. You should replace the XXX.do() part. Don't keep the .do() function after your response. The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.:
            {self.thread_instance.action_current['comment+code']}
                                
            The code of action in the future are(But you don't need to do this part now, just for your information)):
            {self.thread_instance.actionflow.actionflow_pending_get_code()}"""},
            

            # 4. provide the code of the action
            {"role": "user",
            "content":f"""
            Now you write code to achieve your action: {self.thread_instance.action_current['comment']}
            DON'T ASSUME you know the knowledge that you don't know. DON'T ASSUME that you have non-existent functions or hypothetical function, and you can show your thinking and reason in the comment. But don't write any code calling undefined functions in this case.
            make sure that the parameter in your respond code follow the type of the parameter in the function instruction. .
            You are NOT allowed to write {self.thread_instance.puppy_name}.do() in your final response as code. When the {self.thread_instance.puppy_name}.do() appears, you HAVE TO change it to other code.
            your response should be similar with the example(ONLY CODE) and NOTHING ELSE.
            """}]

            # prompt finished *****************************************************************************************

            print("\n")
            print("\U0001F4A4 Action ######################################################################")

            if self.plan_prompt:
                print("*******planning prompt********")
                print(prompt)

            new_code = OpenAIChat(prompt=prompt,
                                  model=model,
                                  temperature=temperature,
                                  api_key=os.environ["OPENAI_API_KEY"],
                                  max_tokens=max_tokens,
                                  printing=True, stream=True)

            new_code = new_code.replace("```python\n", "").replace("\n```", "")

            print("################################################################################")

            action_current = self.thread_instance.action_current
            action_current["comment+code"] = new_code
            action_current["status"] = "fixed"
