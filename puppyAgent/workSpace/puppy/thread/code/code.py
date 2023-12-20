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

                # updated the actionFlow JSON
                self.actionFlowHistoryJSON, self.actionFlowHistoryPython=self.actionFlowTranslate(sourceCode)

            else:
                pass
        
        # return the actionFlowHistoryJSON and actionFlowHistoryPython
        def actionFlowTranslate(self,sourceCode):

            ## initialize the actionFlowHistoryPython
            self.actionFlowHistoryPython=sourceCode
            actionFlowHistoryJSON=[]

            lines = sourceCode.split('\n')

            ## deal with space in the head of the code
            comment_pos = None
            indent_level = None
            for i, line in enumerate(lines):
                if '##' in line:
                    comment_pos = i
                    indent_level = len(line) - len(line.lstrip(' '))
                    break

            # if the indent level is found, adjust the indent of the whole function
            if comment_pos is not None and indent_level is not None:

                # delete all the code before the '##' comment
                lines = lines[comment_pos:]

                adjusted_lines = []
                for line in lines:
                    # only adjust the indent of non-empty lines
                    if line.strip():
                        adjusted_lines.append(line[indent_level:])
                    else:
                        adjusted_lines.append(line)
                adjustedSourceCode = '\n'.join(adjusted_lines)
            else:
                adjustedSourceCode = sourceCode

            ## translate the actionFlowPython to actionFlowJSON
            lines = adjustedSourceCode.split('\n')
            searchForDo = False
            comment = ""
            codeSnippet = ""
            actionFlowHistoryJSON = []

            for line in lines:
                if '##' in line:
                    # if there is an unfinished action, add it to the JSON
                    if searchForDo:
                        actionFlowHistoryJSON.append({"action": comment, "status": "semi-fixed", "code": codeSnippet.strip()})
                        codeSnippet = ""

                    comment = line.split('##', 1)[1].strip()
                    searchForDo = True
                else:
                    if searchForDo:
                        codeSnippet += line + '\n'  # history code snippet
                        if '.do()' in line:
                            # if there is a .do(), mark it as semi-fixed
                            actionFlowHistoryJSON.append({"action": comment, "status": "semi-fixed", "code": codeSnippet.strip()})
                            searchForDo = False
                            codeSnippet = ""
                    else:
                        # if not in the comment module, ignore the line
                        pass

            # deal with the last action
            if searchForDo:
                actionFlowHistoryJSON.append({"action": comment, "status": "fixed", "code": codeSnippet.strip()})

            return actionFlowHistoryJSON, adjustedSourceCode

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
            print("actionFlowHistoryPython:")
            print(self.actionFlow.actionFlowHistoryPython)
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

        ## rethink about the result
        puppy.do()

        ## invite people
        print("Please come here")

        ## send the message to me
        puppy.do()





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
