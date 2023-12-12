import inspect
import sys
import os
import threading
import queue
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompt.actionFlowPrompt import *

class CodeThread():
    def __init__(self):

        self.actionFlow=self.ActionFlow()
        self.taskQueue = queue.Queue()

    # import tools, initialize the agent
    def initialize(self):
        pass

    # to run the agent
    def run(self):

        threadCode = threading.Thread(target=self.codeThread, args=(self.taskQueue,))
        threadCode.start()

        #TODO

        self.taskQueue.put(None)

        # end the code thread
        threadCode.join()

    class ActionFlow():
        def __init__(self): 
            self.actionFlowHistoryJSON = []
            self.actionFlowHistoryPython=""""""

            self.actionPending=[]
        
        def actionFlowTranslate(self,sourceCode):
            # initialize the actionFlowHistoryPython
            self.actionFlowHistoryPython=sourceCode

            lines = sourceCode.split('\n')
            searchForDo = False
            comment = ""

            # initialize the actionFlowHistoryJSON
            for line in lines:
                if '##' in line:
                    if searchForDo==True:
                        self.actionFlowHistoryJSON.append({"action":comment,"status":"fixed"})
                        searchForDo = False
                    comment = line.split('##', 1)[1].strip()
                    searchForDo = True
                else:
                    if searchForDo==True:
                        if '.do()' in line:
                            if comment.strip() == "":
                                self.actionFlowHistoryJSON.append({"action":comment,"status":"changeable"})
                            else:
                                self.actionFlowHistoryJSON.append({"action":comment,"status":"semi-fixed"})
                            searchForDo = False
                        else:
                            pass
                    else:
                        pass
            if searchForDo==True:
                self.actionFlowHistoryJSON.append({"action":comment,"status":"fixed"})
                searchForDo = False 

        def actionPendingRemove(self):
            self.actionPending.pop()

        def actionPendingAdd(self,action):
            self.actionPending.append(action)

        def actionFinish(self,action):
            self.actionFlowHistoryJSON.append({"action":action,"status":"fixed"})
            self.actionFlowHistoryPython += action + "\n"

        def actionExe(self):
            self.taskQueue.put(self.actionPending[0])

        

    
