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
            print("*****")
            print(actionFlowInitialJSON)
            print(actionFlowInitialPython)
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

            searchForCode=False

            comment = ""
            codeSnippet = ""
            actionFlowJSON = []

            for line in lines:
                if '##' in line:
                    if searchForCode==True:
                        actionFlowJSON.append({"action": comment, "code": "## "+comment+"\n"+codeSnippet.strip()})
                    else:
                        pass
                    comment = line.split('##', 1)[1].strip()
                    searchForCode = False
                    codeSnippet = ""
                else:
                    if line.strip()!="":
                        searchForCode=True
                        codeSnippet += line + '\n'  # history code snippet
                    else:
                        pass


            # deal with the last action
            if searchForCode==True:
                actionFlowJSON.append({"action": comment,  "code": "## "+comment+"\n"+codeSnippet.strip()})

            
            for action in actionFlowJSON:
                if ".do()"in action["code"]:
                    if action["action"]=="":
                        action["status"]= "changeable"
                    else:
                        action["status"]="semi-fixed"

                else:
                    action["status"]="fixed"

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

            searchForCode=False

            comment = ""
            codeSnippet = ""
            actionFlowJSON = []

            for line in lines:
                if '##' in line:
                    if searchForCode==True:
                        actionFlowJSON.append({"action": comment, "code": "## "+comment+"\n"+codeSnippet.strip()})
                    else:
                        pass
                    comment = line.split('##', 1)[1].strip()
                    searchForCode = False
                    codeSnippet = ""
                else:
                    if line.strip()!="":
                        searchForCode=True
                        codeSnippet += line + '\n'  # history code snippet
                    else:
                        pass


            # deal with the last action
            if searchForCode==True:
                actionFlowJSON.append({"action": comment,  "code": "## "+comment+"\n"+codeSnippet.strip()})

            
            for action in actionFlowJSON:
                if ".do()"in action["code"]:
                    if action["action"]=="":
                        action["status"]= "changeable"
                    else:
                        action["status"]="semi-fixed"

                else:
                    action["status"]="fixed"

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

        # change the status of the actionFlowCurrent Front
        def actionFlowCurrentStatusChangeFront(self,status):
            self.actionFlowCurrentJSON[0]["status"]=status


        # import the action from the actionFlowPending to actionCurrent
        def actionCurrentLoad(self):
            self.actionFlowCurrentAddToEnd([self.actionFlowPendingGetFront()[1]])

        # save the action from actionCurrent to actionFlowPending
        def actionCurrentSave(self):
            self.actionFlowHistoryAddToFront([self.actionFlowCurrentGetFront()[1]]) 

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

            # STEP 1: load the action from actionFlowPending to actionFlowCurrent
            self.codeThreadActionFlow.actionCurrentLoad()

            # STEP 2: delete the action from actionFlowPending
            self.codeThreadActionFlow.actionFlowPendingRemoveFront()

            print("actionFlowPending:----->")
            print(self.codeThreadActionFlow.actionFlowPendingPython)
            print("actionFlowCurrentJSON:----->")
            print(self.codeThreadActionFlow.actionFlowCurrentJSON)
            print("actionFlowHistory:----->")
            print(self.codeThreadActionFlow.actionFlowHistoryPython)

            while self.codeThreadActionFlow.actionFlowCurrentJSON !=[]:
                
                # STEP 3: load the action from actionFlowCurrent to actionOngoing
                if self.codeThreadActionFlow.actionFlowCurrentGetFront()[0]["status"]=="fixed":

                    self.codeThreadActionFlow.actionCurrentExecute()

                elif self.codeThreadActionFlow.actionFlowCurrentGetFront()[0]["status"]=="semi-fixed":
                    self.codeThreadDo()

                elif self.codeThreadActionFlow.actionFlowCurrentGetFront()[0]["status"]=="changeable":
                    pass
                    ## TODO
                
                # STEP 4: load the action from actionOngoing and execute the code
                action = self.codeThreadActionFlow.actionOnGoing.get()

                print("\n")
                print("############### following action is running ###############")
                print(action)
                print("###########################################################")
                print("\n")
                if action is None:
                    break
                
                exec(action)
                self.codeThreadActionFlow.actionOnGoing.task_done()

                # STEP 5: load the action from the actionFlowCurrent to the actionFlowHistory
                self.codeThreadActionFlow.actionCurrentSave()

                # STEP 6: evaluate if the action is done
                # TODO

                # STEP 7: remove the action from the actionFlowCurrent

                if self.codeThreadActionFlow.actionFlowCurrentGetFront()[0]["status"]=="fixed":
                    self.codeThreadActionFlow.actionFlowCurrentRemoveFront()

                else:
                    pass


        print("Done")
                

    def codeThreadDo(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
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
        
        ##    


        ##    
        print("action")


        ## print hello world
        print("Hello World!")

        ## send the message to my boss
        Mei.do()

        ##
        Mei.do()

        ##   
        Mei.do()

        ##
        print("take me")

        ##



        
    Mei.run()
