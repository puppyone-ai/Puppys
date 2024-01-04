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


class CodeThread():
    def __init__(self):
        self.currentThreadName="codeThread"
        self.codeThreadActionFlow=self.CodeThreadActionFlow()
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
        threadCode = threading.Thread(target=self.codeThreadCodeExecution)
        threadCode.daemon = False
        threadCode.start()
        

        #self.codeThreadActionFlow.actionOnGoing.put(importTools)

        # end the code thread
        threadCode.join()

    class CodeThreadActionFlow():
        def __init__(self): 
            self.actionFlowAllJSON = []
            self.actionFlowAllPython= []

            self.actionFlowHistoryJSON = []
            self.actionFlowHistoryPython= []

            self.actionFlowPendingJSON =[]
            self.actionFlowPendingPython= []

            self.actionFlowCurrentJSON=[]
            self.actionFlowCurrentPython= []

            self.actionOnGoing=queue.Queue()
        
        def actionFlowInitialize(self,sourceCode):

            self.actionFlowHistoryJSON = []
            # updated the actionFlow JSON
            actionFlowInitialJSON, actionFlowInitialPython=self.actionFlowTranslatePython(sourceCode)
            self.actionFlowPendingAddToFront(actionFlowInitialPython)


        def actionFlowTranslatePythonList(self,adjustedSourceCodeList: list):
            """
            translate the source code to actionFlowJSON and actionFlowPython

            args: sourceCode(Python)
            return: actionFlowHistoryJSON(List), actionFlowHistoryPython(String)
            """

            sourceCode="\n".join(adjustedSourceCodeList)
            ## initialize the actionFlowJSON and actionFlowPython
            actionFlowJSON=[]
            actionFlowPython=[]

            lines = sourceCode.split('\n')

            ## deal with space in the head of the code
            comment_pos = None
            indent_level = None
            for i, line in enumerate(lines):
                if '##' in line:
                    comment_pos = i
                    indent_level = len(line) - len(line.lstrip(' '))
                    break
            
            # return the adjusted source code, with is the code without the indent
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


            ## return the actionFlowJSON
            lines = adjustedSourceCode.split('\n')
            searchForDo = False
            comment = ""
            codeSnippet = ""
            actionFlowJSON = []

            for line in lines:
                if '##' in line:
                    # if there is an unfinished action, add it to the JSON
                    if searchForDo:
                        actionFlowJSON.append({"action": comment, "status": "semi-fixed", "code": "## "+comment+"\n"+codeSnippet.strip()})
                        codeSnippet = ""

                    comment = line.split('##', 1)[1].strip()
                    searchForDo = True
                else:
                    if searchForDo:
                        codeSnippet += line + '\n'  # history code snippet
                        if '.do()' in line:
                            # if there is a .do(), mark it as semi-fixed
                            actionFlowJSON.append({"action": comment, "status": "semi-fixed", "code": "## "+comment+"\n"+codeSnippet.strip()})
                            searchForDo = False
                            codeSnippet = ""
                    else:
                        # if not in the comment module, ignore the line
                        pass

            # deal with the last action
            if searchForDo:
                actionFlowJSON.append({"action": comment, "status": "fixed", "code": "## "+comment+"\n"+codeSnippet.strip()})

            ## return the actionFlowPython
            for action in actionFlowJSON:
                actionFlowPython.append(action["code"])

            return actionFlowJSON, actionFlowPython
            

        # return the actionFlowHistoryJSON and actionFlowHistoryPython
        def actionFlowTranslatePython(self, sourceCode: str):

            """
            translate the source code to actionFlowJSON and actionFlowPython

            args: sourceCode(Python)
            return: actionFlowHistoryJSON(List), actionFlowHistoryPython(String)
            """

            ## initialize the actionFlowJSON and actionFlowPython
            actionFlowJSON=[]
            actionFlowPython=[]

            lines = sourceCode.split('\n')

            ## deal with space in the head of the code
            comment_pos = None
            indent_level = None
            for i, line in enumerate(lines):
                if '##' in line:
                    comment_pos = i
                    indent_level = len(line) - len(line.lstrip(' '))
                    break
            
            # return the adjusted source code, with is the code without the indent
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


            ## return the actionFlowJSON
            lines = adjustedSourceCode.split('\n')
            searchForDo = False
            comment = ""
            codeSnippet = ""
            actionFlowJSON = []

            for line in lines:
                if '##' in line:
                    # if there is an unfinished action, add it to the JSON
                    if searchForDo:
                        actionFlowJSON.append({"action": comment, "status": "semi-fixed", "code": "## "+comment+"\n"+codeSnippet.strip()})
                        codeSnippet = ""

                    comment = line.split('##', 1)[1].strip()
                    searchForDo = True
                else:
                    if searchForDo:
                        codeSnippet += line + '\n'  # history code snippet
                        if '.do()' in line:
                            # if there is a .do(), mark it as semi-fixed
                            actionFlowJSON.append({"action": comment, "status": "semi-fixed", "code": "## "+comment+"\n"+codeSnippet.strip()})
                            searchForDo = False
                            codeSnippet = ""
                    else:
                        # if not in the comment module, ignore the line
                        pass

            # deal with the last action
            if searchForDo:
                actionFlowJSON.append({"action": comment, "status": "fixed", "code": "## "+comment+"\n"+codeSnippet.strip()})

            ## return the actionFlowPython
            for action in actionFlowJSON:
                actionFlowPython.append(action["code"])

            return actionFlowJSON, actionFlowPython


        # operation for actionFlowHistory
        def actionFlowHistoryGetFront(self):

            return self.actionFlowHistoryJSON[0],self.actionFlowHistoryPython[0]
        
        def actionFlowHistoryAddToFront(self,actionCode):
            actionJSON,actionPython=self.actionFlowTranslatePythonList(actionCode)
            self.actionFlowHistoryJSON=actionJSON+self.actionFlowHistoryJSON
            self.actionFlowHistoryPython=actionPython+self.actionFlowHistoryPython
            
        def actionFlowHistoryRemoveFront(self):
            self.actionFlowHistoryJSON.pop(0)
            self.actionFlowHistoryPython.pop(0)

        def actionFlowHistoryGetEnd(self):

            return self.actionFlowHistoryJSON[-1],self.actionFlowHistoryPython[-1]
        
        def actionFlowHistoryAddToEnd(self,actionCode):
            actionJSON,actionPython=self.actionFlowTranslatePythonList(actionCode)
            self.actionFlowHistoryJSON=self.actionFlowHistoryJSON+actionJSON
            self.actionFlowHistoryPython=self.actionFlowHistoryPython+actionPython

        def actionFlowHistoryRemoveEnd(self):
            self.actionFlowHistoryJSON.pop()
            self.actionFlowHistoryPython.pop()


        # operation for actionFlowPending
        def actionFlowPendingGetFront(self):

            return self.actionFlowPendingJSON[0],self.actionFlowPendingPython[0]
        
        def actionFlowPendingAddToFront(self,actionCode):
            actionJSON,actionPython=self.actionFlowTranslatePythonList(actionCode)
            self.actionFlowPendingJSON=actionJSON+self.actionFlowPendingJSON
            self.actionFlowPendingPython=actionPython+self.actionFlowPendingPython
            
        def actionFlowPendingRemoveFront(self):
            self.actionFlowPendingJSON.pop(0)
            self.actionFlowPendingPython.pop(0)

        def actionFlowPendingGetEnd(self):

            return self.actionFlowPendingJSON[-1],self.actionFlowPendingPython[-1]
        
        def actionFlowPendingAddToEnd(self,actionCode):
            actionJSON,actionPython=self.actionFlowTranslatePythonList(actionCode)
            self.actionFlowPendingJSON=self.actionFlowPendingJSON+actionJSON
            self.actionFlowPendingPython=self.actionFlowPendingPython+actionPython

        def actionFlowPendingRemoveEnd(self):
            self.actionFlowPendingJSON.pop()
            self.actionFlowPendingPython.pop()

        # operation for actionFlowCurrent
        def actionFlowCurrentGetFront(self):

            return self.actionFlowCurrentJSON[0],self.actionFlowCurrentPython[0]
        
        def actionFlowCurrentAddToFront(self,actionCode):
            actionJSON,actionPython=self.actionFlowTranslatePythonList(actionCode)
            self.actionFlowCurrentJSON=actionJSON+self.actionFlowCurrentJSON
            self.actionFlowCurrentPython=actionPython+self.actionFlowCurrentPython
            
        def actionFlowCurrentRemoveFront(self):
            self.actionFlowCurrentJSON.pop(0)
            self.actionFlowCurrentPython.pop(0)

        def actionFlowCurrentGetEnd(self):

            return self.actionFlowCurrentJSON[-1],self.actionFlowCurrentPython[-1]
        
        def actionFlowCurrentAddToEnd(self,actionCode):
            actionJSON,actionPython=self.actionFlowTranslatePythonList(actionCode)
            self.actionFlowCurrentJSON=self.actionFlowCurrentJSON+actionJSON
            self.actionFlowCurrentPython=self.actionFlowCurrentPython+actionPython

        def actionFlowCurrentRemoveEnd(self):
            self.actionFlowCurrentJSON.pop()
            self.actionFlowCurrentPython.pop()

        def actionFlowCurrentClear(self):
            self.actionFlowCurrentJSON=[]
            self.actionFlowCurrentPython=[]

        # import the action from the actionFlowPending to actionCurrent
        def actionCurrentLoad(self):
            self.actionFlowCurrentAddToEnd([self.actionFlowPendingGetFront()[1]])
            self.actionFlowPendingRemoveFront()

        # save the action from actionCurrent to actionFlowPending
        def actionCurrentSave(self):
            self.actionFlowHistoryAddToFront([self.actionFlowCurrentGetFront()[1]]) 
            self.actionFlowCurrentRemoveFront()

        # put the action from actionCurrent to actionOnGoing
        def actionCurrentExecute(self):
            self.actionOnGoing.put(self.actionFlowCurrentPython[0])


    # for the wrapper of action
    def codeThread(self, func):
        def wrapper(self, *args, **kwargs):
            self.initialize()
            func(*args, **kwargs)
        
        self.currentThreadName="codeThread"
        sourseCode=inspect.getsource(func)

        # if the function is action, initialize the actionFlow
        funcName=func.__name__
        if funcName == "action":

            # get source code
            self.codeThreadActionFlow.actionFlowInitialize(sourseCode)

            print("Initialize Start-------------------------------------------")
            print("Initialized Function: "+funcName)
            print("actionFlowPendingPython:")
            print(self.codeThreadActionFlow.actionFlowPendingPython)
            print("InitializedActionFlowJSON:"+str(self.codeThreadActionFlow.actionFlowPendingJSON))

            

        if funcName == "trigger":
            # TODO
            pass

        # execute the function with wrapper
        return wrapper

    def codeThreadCodeExecution(self):

        # import tools, for agents
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import actionDefault
        from actionDefault import AskHumanForHelp

        print("Import Start ----------------------------------------------")

        self.codeThreadActionFlow.actionFlowCurrentClear()

        while self.codeThreadActionFlow.actionFlowCurrentJSON ==[] and self.codeThreadActionFlow.actionFlowPendingJSON !=[]:
            print("\n")
            print("Action Start ----------------------------------------------")


            self.codeThreadActionFlow.actionCurrentLoad()
            print("actionFlowPending:----->")
            print(self.codeThreadActionFlow.actionFlowPendingPython)
            print("actionFlowCurrent:----->")
            print(self.codeThreadActionFlow.actionFlowCurrentPython)
            print("actionFlowHistory:----->")
            print(self.codeThreadActionFlow.actionFlowHistoryPython)

            while self.codeThreadActionFlow.actionFlowCurrentJSON !=[]:

                self.codeThreadActionFlow.actionCurrentExecute()
                """
                print("Action OnGoing before:")
                print(self.codeThreadActionFlow.actionOnGoing.queue)
"""
                action = self.codeThreadActionFlow.actionOnGoing.get()

                print("\n")
                print("############### following action is running ###############")
                print(action)
                print("###########################################################")
                print("\n")
                if action is None:
                    break
                
                exec(action)
                self.codeThreadActionFlow.actionCurrentSave()

                #self.codeThreadActionFlow.actionOnGoing.task_done()

        print("Done")
                

    def do(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey

        from prompt.actionFlowPrompt import ActionDo

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionParameter=LLMChain(llm=llm, prompt= ActionDo)

        import actionDefault

        self.functionsDescriptionAndExample= actionDefault.getDescriptionAndExample()

        agentExperience="none"

        newCode=fillingActionParameter.predict(goal=self.goal,
                                               current_action=self.codeThreadActionFlow.actionOnGoing,
                                                current_action_Python= self.codeThreadActionFlow.actionFlowCurrentPython,
                                                code_history=self.codeThreadActionFlow.actionFlowHistoryPython,
                                                code_future="",
                                                enviroment=self.environment,
                                                function_description_and_example=self.functionsDescriptionAndExample,
                                                experiences=agentExperience)
                                                

        newCodeOnly=newCode.replace("```python\n", "").replace("\n```", "")
        print("\n")
        print("++++++++++++++++++ Generated Code Start +++++++++++++++++++")
        print(newCodeOnly)
        print("+++++++++++++++++++ Generated Code End ++++++++++++++++++++")
        print("\n")
        self.codeThreadActionFlow.actionFlowCurrentAddToEnd([newCodeOnly])


class Puppy(CodeThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.codeThreadRun()


if __name__ == '__main__':

    Mei = Puppy()

    @Mei.codeThread
    def action():
        
        ## tell me your phone number
        Mei.do()

        ## send message to my dad

        # hello?
        print("Dont Say Hello!")
        print("take me to the church")
        Mei.do()


        
    Mei.run()
