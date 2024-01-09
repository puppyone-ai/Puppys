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
        self.actionFlow=self.ActionFlow()
        self.actions=self.Action(self)
        self.threadProperty={}
        self.environment={
        }

        self.goal="make the earth better"

    # import tools, initialize the agent
    def codeThreadInitialize(self):
        pass

    # to run the thread
    def run(self):
        
        # start the code thread
        threadCode = threading.Thread(target=self.CodeExecution)
        threadCode.daemon = False
        threadCode.start()
        

        #self.codeThreadActionFlow.actionOnGoing.put(importTools)

        # end the code thread
        threadCode.join()

    class ActionFlow():
        def __init__(self): 
            self.actionFlowAllJSON = []

            self.actionFlowHistoryJSON = []

            self.actionFlowPendingJSON =[]

            self.actionFlowCurrentJSON=[]

            self.actionOnGoing=queue.Queue()
        
        def initialize(self,sourceCode):

            self.actionFlowHistoryJSON = []
            # updated the actionFlow JSON
            actionFlowInitialJSON, actionFlowInitialPython=self.translatePython(sourceCode)
            print("*****")
            print(actionFlowInitialJSON)
            self.actionFlowPendingAddToFront(actionFlowInitialJSON)


        # return the actionFlowHistoryJSON and actionFlowHistoryPython
        def translatePython(self, sourceCode: str):

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

        def decorateActionFlowCodeToJSON(self, code, status="undefined"):
            actionFlowJSON=self.translatePython(code)[0]

            if status=="undefined":
                pass
            else:
                for action in actionFlowJSON:
                    action["status"]=status
            
            return actionFlowJSON


        # operation for actionFlowHistory
        def actionFlowHistoryGetCode(self):
            code=""
            for action in self.actionFlowHistoryJSON:
                code+=action["code"]+"\n"

            return code

        def actionFlowHistoryGetFront(self):
            return self.actionFlowHistoryJSON[0]
        
        ##
        def actionFlowHistoryAddToFront(self,actionFlowJSON):
            self.actionFlowHistoryJSON=actionFlowJSON+self.actionFlowHistoryJSON
            
        def actionFlowHistoryRemoveFront(self):
            self.actionFlowHistoryJSON.pop(0)

        def actionFlowHistoryGetEnd(self):
            return self.actionFlowHistoryJSON[-1]
        
        def actionFlowHistoryAddToEnd(self,actionFlowJSON):
            self.actionFlowHistoryJSON=self.actionFlowHistoryJSON+actionFlowJSON

        def actionFlowHistoryRemoveEnd(self):
            self.actionFlowHistoryJSON.pop()

        # operation for actionFlowPending
        def actionFlowPendingGetCode(self):
            code=""
            for action in self.actionFlowPendingJSON:
                code+=action["code"]+"\n"

            return code

        def actionFlowPendingGetFront(self):
            return self.actionFlowPendingJSON[0]
        
        def actionFlowPendingAddToFront(self,actionFlowJSON):
            self.actionFlowPendingJSON=actionFlowJSON+self.actionFlowPendingJSON
            
        def actionFlowPendingRemoveFront(self):
            self.actionFlowPendingJSON.pop(0)

        def actionFlowPendingGetEnd(self):
            return self.actionFlowPendingJSON[-1]
        
        def actionFlowPendingAddToEnd(self,actionFlowJSON):
            self.actionFlowPendingJSON=self.actionFlowPendingJSON+actionFlowJSON

        def actionFlowPendingRemoveEnd(self):
            self.actionFlowPendingJSON.pop()

        # operation for actionFlowCurrent
        def actionFlowCurrentGetCode(self):
            code=""
            for action in self.actionFlowCurrentJSON:
                code+=action["code"]+"\n"

            return code
        
        def actionFlowCurrentSkip(self):
            self.actionFlowCurrentJSON.pop(0)
        
        def actionFlowCurrentGetFront(self):
            return self.actionFlowCurrentJSON[0]
        
        def actionFlowCurrentAddToFront(self,actionFlowJSON):
            self.actionFlowCurrentJSON=actionFlowJSON+self.actionFlowCurrentJSON
            
        def actionFlowCurrentRemoveFront(self):
            self.actionFlowCurrentJSON.pop(0)

        def actionFlowCurrentGetEnd(self):
            return self.actionFlowCurrentJSON[-1]
        
        ##
        def actionFlowCurrentAddToEnd(self,actionFlowJSON):
            self.actionFlowCurrentJSON=self.actionFlowCurrentJSON+actionFlowJSON

        def actionFlowCurrentRemoveEnd(self):
            self.actionFlowCurrentJSON.pop()

        def actionFlowCurrentClear(self):
            self.actionFlowCurrentJSON=[]

        # change the status of the actionFlowCurrent Front
        def actionFlowCurrentStatusChangeFront(self,status):
            self.actionFlowCurrentJSON[0]["status"]=status


        # import the action from the actionFlowPending to actionCurrent
        def actionCurrentLoad(self):
            self.actionFlowCurrentAddToEnd([self.actionFlowPendingGetFront()])

        # save the action from actionCurrent to actionFlowPending
        def actionCurrentSave(self):
            self.actionFlowHistoryAddToFront([self.actionFlowCurrentGetFront()]) 

        # put the action from actionCurrent to actionOnGoing
        def actionCurrentExecute(self):
            self.actionOnGoing.put(self.actionFlowCurrentJSON[0]["code"])

    class Action():
        def __init__(self, codeThreadInstance):
            self.codeThreadInstance = codeThreadInstance
            self.actionList={}

        # opreations for actions
        def actionGet(self):
            return self.actionList
        
        def actionAdd(self,action):
            self.actionList.update(action)

        def actionRemove(self,action):
            self.actionList.pop(action)

        def actionClear(self):
            self.actionList={}

        class Do():
            """
            write code to achieve the action
            """
            pass

        # define default actions for codeThread
        
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
        if funcName == "action":

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

                else:
                    pass


        print("Done")
    
    # the wrapper for the action for the code thread


class Puppy(CodeThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.run()

        



"""
把反省 agent 是否完成了任务加到 action 里面"""

















if __name__ == '__main__':

    Mei = Puppy()

    @Mei.codeThread
    def action():

        ## find the price of the game Cities: Skylines 2 on Steam
        Mei.do()

        ## campare if the price is lower than 10 dollars
        Mei.do()




    Mei.run()

