import inspect
import sys
import os
import threading
import queue
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import re
import time
from actionFlow import ActionFlow
from actions import Actions


class CodeThread():
    def __init__(self):
        self.currentThreadName="codeThread"
        self.actionFlow=ActionFlow()
        self.actions=Actions(self)
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
                    self.actions.do()
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

