import inspect
import sys
import os
import threading
import queue
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
import re


class CodeThread():
    def __init__(self):

        self.actionFlow=self.ActionFlow()
        self.threadProperty={}
        self.environment={
            "goal": "send hello to my mom",
        }

    # import tools, initialize the agent
    def initialize(self):
        pass

    # to run the agent
    def run(self):
        
        # start the code thread
        threadCode = threading.Thread(target=self.codeExecution)
        threadCode.daemon = False
        threadCode.start()

        # end the code thread
        threadCode.join()

    class ActionFlow():
        def __init__(self): 
            self.actionFlowAllJSON = []
            self.actionFlowAllPython=""""""
            self.actionFlowHistoryJSON = []
            self.actionFlowHistoryPython=""""""

            self.actionCurrent=""""""

            self.actionPending=queue.Queue()
        
        def actionFlowInitialize(self,sourceCode):
            if self.actionFlowAllJSON == []:

                # updated the actionFlow JSON
                self.actionFlowAllJSON, self.actionFlowAllPython=self.actionFlowTranslate(sourceCode)
                self.actionPendingUpdate(self.actionFlowAllJSON[0]["code"])

            else:
                pass
        
        # return the actionFlowHistoryJSON and actionFlowHistoryPython
        def actionFlowTranslate(self,sourceCode):

            ## initialize the actionFlowHistoryPython
            self.actionFlowAllPython=sourceCode
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

        def actionPendingUpdate(self,action):
            self.actionPending.put(action)

        def actionFinish(self,action):
            self.actionFlowAllJSON.append({"action":action,"status":"fixed"})
            self.actionFlowAllPython += action + "\n"

        def actionExe(self):
            self.taskQueue.put(self.actionPending[0])

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
            print(self.actionFlow.actionFlowAllPython)
            print("InitializedActionFlowJSON:"+str(self.actionFlow.actionFlowAllJSON))
            #print("Start from:"+self.actionFlow.actionPending.get())
            

        if funcName == "trigger":
            # TODO
            pass

        # execute the function with wrapper
        return wrapper

    def codeExecution(self):
        while True:
            task = self.actionFlow.actionPending.get()
            self.actionFlow.actionCurrent=task
            if task is None:
                break
            
            print(task)
            exec(task)

            self.actionFlow.actionPending.task_done()

    def do(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey

        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        from prompt.actionFlowPrompt import ActionDo

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionParameter=LLMChain(llm=llm, prompt= ActionDo)

        """
        self.importTools()
        self.getDescriptions()
        self.getExamples()
        """

        self.functionsSimplified="""
        None
        """

        agentExperience="none"

        newCode=fillingActionParameter.predict(current_action= self.actionFlow.actionCurrent,
                                                 code_history=self.actionFlow.actionFlowHistoryPython,
                                                    code_future="",
                                                    enviroment=self.environment,
                                                    function=self.functionsSimplified,
                                                    experiences=agentExperience)
                                                

        newCodeOnly=newCode.replace("```python\n", "").replace("\n```", "")

        print("newCode:")
        print(newCodeOnly)

        self.actionFlow.actionPendingUpdate(newCodeOnly)

        print("newCodeEnd")


if __name__ == '__main__':

    puppy = CodeThread()

    @puppy.codeThread
    def action():

        ## Invite people
        puppy.do()

    puppy.run()





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
