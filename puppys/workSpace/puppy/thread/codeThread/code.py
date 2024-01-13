import inspect
import sys
import os
import threading
import queue
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import re
import time
from actionFlow import ActionFlow


class CodeThread():
    def __init__(self):
        self.currentThreadName="codeThread"
        self.actionFlow=ActionFlow()
        self.actions=self.Action(self)
        self.threadProperty={}
        self.environment={
        }

        self.goal="make the earth better"

    # import tools, initialize the agent
    def codeThreadInitialize(self):
        pass

    # to run the thread
    def codeThreadRun(self):
        
        # start the code thread
        threadCode = threading.Thread(target=self.CodeExecution)
        threadCode.daemon = False
        threadCode.start()
        

        #self.codeThreadActionFlow.actionOnGoing.put(importTools)

        # end the code thread
        threadCode.join()

    

    class Action():
        def __init__(self, codeThreadInstance):
            self.codeThreadInstance = codeThreadInstance
            self.actionList=[{"action":"do",
                             "code":"",
                             "function_before_action":[],
                                "function_after_action":[],}]

        # opreations for actions
        def actionGet(self):
            return self.actionList
        
        def actionAdd(self,action):
            self.actionList.update(action)

        def actionRemove(self,action):
            self.actionList.pop(action)

        def actionClear(self):
            self.actionList={}

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
       
    def do(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey
        """
        write code to achieve the action
        """

        from prompt.actionFlowPrompt import ActionDo

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionParameter=LLMChain(llm=llm, prompt= ActionDo)

        import actionDefault

        self.functionsDescriptionAndExample= actionDefault.getDescriptionAndExample()

        agentExperience="none"

        newCode=fillingActionParameter.predict(goal=self.goal,
                                            current_action=self.actionFlow.actionOnGoing,
                                                current_action_Python= self.actionFlow.actionFlowCurrentGetCode(),
                                                code_history=self.actionFlow.actionFlowHistoryGetCode(),
                                                code_future=self.actionFlow.actionFlowPendingGetCode(),
                                                enviroment=self.environment,
                                                function_description_and_example=self.functionsDescriptionAndExample,
                                                experiences=agentExperience)
                                                

        newCode=newCode.replace("```python\n", "").replace("\n```", "")
        print("\n")
        print("++++++++++++++++++ Generated Code Start +++++++++++++++++++")
        print(newCode)
        print("+++++++++++++++++++ Generated Code End ++++++++++++++++++++")
        print("\n")
        self.actionFlow.actionFlowCurrentAddToFront(self.actionFlow.decorateActionFlowCodeToJSON(newCode,status="fixed"))

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



    # for the wrapper of action
    def codeThread(self, func):
        def wrapper(self, *args, **kwargs):
            self.initialize()
            func(*args, **kwargs)
        
        self.currentThreadName="codeThread"
        sourseCode=inspect.getsource(func)

        # if the function is action, initialize the actionFlow
        funcName=func.__name__
        if funcName == "actionFlow":

            # get source code
            self.actionFlow.initialize(sourseCode)

            print("Initialize Start-------------------------------------------")
            print("Initialized Function: "+funcName)
            print("actionFlowPending:")
            print(self.actionFlow.actionFlowPendingJSON)


        if funcName == "trigger":
            # TODO
            pass

        # execute the function with wrapper
        return wrapper

    def CodeExecution(self):

        # import tools, for agents
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import actionDefault
        from actionDefault import AskHumanForHelp
        from actionDefault import GoogleSearchNative
        from actionDefault import GPT

        print("Import Start ----------------------------------------------")

        self.actionFlow.actionFlowCurrentClear()

        while self.actionFlow.actionFlowCurrentJSON ==[] and self.actionFlow.actionFlowPendingJSON !=[]:
            print("\n")
            print("Action Start ----------------------------------------------")

            # STEP 1: load the action from actionFlowPending to actionFlowCurrent
            self.actionFlow.actionCurrentLoad()

            # STEP 2: delete the action from actionFlowPending
            self.actionFlow.actionFlowPendingRemoveFront()

            print("actionFlowPending:----->")
            print(self.actionFlow.actionFlowPendingJSON)
            print("actionFlowCurrentJSON:----->")
            print(self.actionFlow.actionFlowCurrentJSON)
            print("actionFlowHistory:----->")
            print(self.actionFlow.actionFlowHistoryJSON)

            while self.actionFlow.actionFlowCurrentJSON !=[]:
                
                # STEP 3: load the action from actionFlowCurrent to actionOngoing
                if self.actionFlow.actionFlowCurrentGetFront()["status"]=="fixed":

                    self.actionFlow.actionCurrentExecute()

                elif self.actionFlow.actionFlowCurrentGetFront()["status"]=="semi-fixed":
                    self.do()
                    self.actionFlow.actionCurrentExecute()

                elif self.actionFlow.actionFlowCurrentGetFront()["status"]=="changeable":
                    pass
                    ## TODO
                
                # STEP 4: load the action from actionOngoing and execute the code
                action = self.actionFlow.actionOnGoing.get()

                print("\n")
                print("############### following action is running ###############")
                print(action)
                print("###########################################################")
                print("\n")
                if action is None:
                    break
                
                exec(action)
                self.actionFlow.actionOnGoing.task_done()

                # STEP 5: load the action from the actionFlowCurrent to the actionFlowHistory
                self.actionFlow.actionCurrentSave()

                # STEP 6: evaluate if the action is done
                # TODO

                # STEP 7: remove the action from the actionFlowCurrent


                if self.actionFlow.actionFlowCurrentGetFront()["status"]=="fixed":
                    self.actionFlow.actionFlowCurrentRemoveFront()
                    self.actionFlow.actionFlowCurrentRemoveFront()

                elif self.actionFlow.actionFlowCurrentGetFront()["status"]=="semi-fixed":
                    self.actionFlow.actionFlowCurrentRemoveFront()

                else:
                    self.actionFlow.actionFlowCurrentRemoveFront()


        print("Done")
    
    # the wrapper for the action for the code thread


class Puppy(CodeThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.codeThreadRun()

        



"""
把反省 agent 是否完成了任务加到 action 里面
"""






if __name__ == '__main__':

    ZIQI = Puppy()

    @ZIQI.codeThread
    def actionFlow():

        ## 帮我找到一个中国市场上最好用的五款耳机
        ZIQI.do()

        ## 帮我把你的结果发给我
        ZIQI.do()

    ZIQI.run()

