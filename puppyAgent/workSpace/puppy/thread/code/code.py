import inspect
import sys
import os
import threading
import queue
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

class CodeThread():
    def __init__(self):

        self.actionFlow=self.ActionFlow()
        self.taskQueue = queue.Queue()
        self.threadProperty={}

    # import tools, initialize the agent
    def initialize(self):
        pass

    # to run the agent
    def run(self):

        threadCode = threading.Thread(target=self.codeExecution)
        threadCode.start()


        self.action()

        self.taskQueue.put(None)

        # end the code thread
        threadCode.join()

    class ActionFlow():
        def __init__(self): 
            self.actionFlowHistoryJSON = []
            self.actionFlowHistoryPython=""""""

            self.actionPending=[]
        
        def actionFlowInitialize(self,sourceCode):
            if self.actionFlowHistoryJSON == []:
                self.actionFlowHistoryJSON=self.actionFlowTranslate(sourceCode)
            else:
                pass

        def actionFlowTranslate(self,sourceCode):
            # initialize the actionFlowHistoryPython
            self.actionFlowHistoryPython=sourceCode
            actionFlowHistoryJSON=[]

            lines = sourceCode.split('\n')
            searchForDo = False
            comment = ""

            # initialize the actionFlowHistoryJSON
            for line in lines:
                if '##' in line:
                    if searchForDo==True:
                        actionFlowHistoryJSON.append({"action":comment,"status":"fixed"})
                        searchForDo = False
                    comment = line.split('##', 1)[1].strip()
                    searchForDo = True
                else:
                    if searchForDo==True:
                        if '.do()' in line:
                            if comment.strip() == "":
                                actionFlowHistoryJSON.append({"action":comment,"status":"changeable"})
                            else:
                                actionFlowHistoryJSON.append({"action":comment,"status":"semi-fixed"})
                            searchForDo = False
                        else:
                            pass
                    else:
                        pass
            if searchForDo==True:
                actionFlowHistoryJSON.append({"action":comment,"status":"fixed"})
                searchForDo = False 

            return actionFlowHistoryJSON

        def actionPendingRemove(self):
            self.actionPending.pop()

        def actionPendingAdd(self,action):
            self.actionPending.append(action)

        def actionFinish(self,action):
            self.actionFlowHistoryJSON.append({"action":action,"status":"fixed"})
            self.actionFlowHistoryPython += action + "\n"

        def actionExe(self):
            self.taskQueue.put(self.actionPending[0])

    def codeExecution(self):
        while True:
            task = self.taskQueue.get()
            if task is None:
                break
            task()

    # for the wrapper of action
    def codeThread(self, func):
        def wrapper(self, *args, **kwargs):

            self.initialize()
            func(*args, **kwargs)
        
        
        sourseCode=inspect.getsource(func)

        # if the function is action, initialize the actionFlow
        funcName=func.__name__
        if funcName == "action":

            # get source code
            self.actionFlow.actionFlowInitialize(sourseCode)

            print("Initialized: "+funcName)
            print("SourseCode:")
            print(sourseCode)
            print("InitializedActionFlowJSON:"+str(self.actionFlow.actionFlowHistoryJSON))

        if funcName == "trigger":
            # TODO
            pass

        # execute the function with wrapper
        return wrapper
            



if __name__ == '__main__':

    puppy = CodeThread()

    @puppy.codeThread
    def action():
        ## invite people
        print("MulalaG")






"""
Yuning=puppy()

@Yuning.codeThread
def action():
    ## 
    print("action")


def trigger():
    ## once a new PDF is uploaded, trigger the action
    Yunning.do()


@Yuning.goalThread
def action():
    setGoal("You are a bad guy!")

@Yuning.safeThread
def action():



Yuning.run()

"""
