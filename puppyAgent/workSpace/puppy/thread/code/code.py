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
        
        """
        self.codeThreadActionFlow.actionOnGoing.put("sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))")
        self.codeThreadActionFlow.actionOnGoing.put("print(sys.path)")
        self.codeThreadActionFlow.actionOnGoing.put("print('MotherFucker')")
        self.codeThreadActionFlow.actionOnGoing.put("import actionDefault")
        self.codeThreadActionFlow.actionOnGoing.put("from actionDefault import AskHumanForHelp")
        """

        importTools="""
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import actionDefault
        from actionDefault import AskHumanForHelp
        """

        #self.codeThreadActionFlow.actionOnGoing.put(importTools)

        # end the code thread
        threadCode.join()

    class CodeThreadActionFlow():
        def __init__(self): 
            self.actionFlowAllJSON = []
            self.actionFlowAllPython=""""""

            self.actionFlowHistoryJSON = []
            self.actionFlowHistoryPython=""""""

            self.actionFlowPendingJSON =[]
            self.actionFlowPendingPython=""""""

            self.actionCurrentJSON=[]
            self.actionCurrentPython=""""""

            self.actionOnGoing=queue.Queue()
        
        def actionFlowInitialize(self,sourceCode):

            self.actionFlowHistoryJSON == []
            # updated the actionFlow JSON
            actionFlowInitialJSON, actionFlowInitialPython=self.actionFlowTranslatePython(sourceCode)
            self.actionFlowPendingAddToFront(actionFlowInitialPython)


        # return the actionFlowHistoryJSON and actionFlowHistoryPython
        def actionFlowTranslatePython(self,sourceCode):

            """
            translate the source code to actionFlowJSON and actionFlowPython

            args: sourceCode(Python)
            return: actionFlowHistoryJSON(List), actionFlowHistoryPython(String)
            """

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

        # operation for actionFlowHistory
        def actionFlowHistoryGetFront(self):
            parts = self.actionFlowHistoryPython.split("##")
            print(parts)

            # omit the code before the first "##"
            parts = parts[1:]

            # for each part, add "##" to the front, and store it in the list
            actionFlowList = ["##" + part for part in parts if part.strip()]
            
            return self.actionFlowPendingJSON[0],actionFlowList[0]
        
        def actionFlowHistoryAddToFront(self,actionCode):
            actionJSON,actionCode=self.actionFlowTranslatePython(actionCode)
            self.actionFlowHistoryJSON=actionJSON+self.actionFlowHistoryJSON
            self.actionFlowHistoryPython=str(actionCode)+'\n'+self.actionFlowHistoryPython
            
        def actionFlowHistoryRemoveFront(self):
            self.actionFlowHistoryJSON.pop(0)
            if len(self.actionFlowHistoryPython.split('##',1))>0:
                self.actionFlowHistoryPython=self.actionFlowHistoryPython.split('##',1)[0]
            else:
                self.actionFlowHistoryPython=""

        def actionFlowHistoryGetEnd(self):
            parts = self.actionFlowHistoryPython.split("##")
            print(parts)

            # omit the code before the first "##"
            parts = parts[1:]

            # for each part, add "##" to the front, and store it in the list
            actionFlowList = ["##" + part for part in parts if part.strip()]
            
            return self.actionFlowPendingJSON[0],actionFlowList[-1]
        
        def actionFlowHistoryAddToEnd(self,actionCode):
            actionJSON,actionCode=self.actionFlowTranslatePython(actionCode)
            self.actionFlowHistoryJSON=self.actionFlowHistoryJSON+actionJSON
            self.actionFlowHistoryPython=self.actionFlowHistoryPython+'\n'+str(actionCode)

        def actionFlowHistoryRemoveEnd(self):
            self.actionFlowHistoryJSON.pop()
            if len(self.actionFlowHistoryPython.split('##',1))>0:
                self.actionFlowHistoryPython=self.actionFlowHistoryPython.split('##',1)[-1]
            else:
                self.actionFlowHistoryPython=""

        # operation for actionFlowPending
        def actionFlowPendingGetFront(self):

            parts = self.actionFlowPendingPython.split("##")
            print(parts)

            # omit the code before the first "##"
            parts = parts[1:]

            # for each part, add "##" to the front, and store it in the list
            actionFlowList = ["##" + part for part in parts if part.strip()]
            
            return self.actionFlowPendingJSON[0],actionFlowList[0]
        
        def actionFlowPendingAddToFront(self,actionCode):
            actionJSON,actionCode=self.actionFlowTranslatePython(actionCode)
            self.actionFlowPendingJSON=actionJSON+self.actionFlowPendingJSON
            self.actionFlowPendingPython=str(actionCode)+'\n'+str(self.actionFlowPendingPython)
            
        def actionFlowPendingRemoveFront(self):
            self.actionFlowPendingJSON.pop(0)
            if len(self.actionFlowPendingPython.split('##',1))>0:
                self.actionFlowPendingPython=self.actionFlowPendingPython.split('##',1)[0]
            else:
                self.actionFlowPendingPython=""

        def actionFlowPendingGetEnd(self):
            parts = self.actionFlowPendingPython.split("##")
            print(parts)

            # omit the code before the first "##"
            parts = parts[1:]

            # for each part, add "##" to the front, and store it in the list
            actionFlowList = ["##" + part for part in parts if part.strip()]
            
            return self.actionFlowPendingJSON[0],actionFlowList[-1]
        
        def actionFlowPendingAddToEnd(self,actionCode):
            actionJSON,actionCode=self.actionFlowTranslatePython(actionCode)
            self.actionFlowPendingJSON=self.actionFlowPendingJSON+actionJSON
            self.actionFlowPendingPython=self.actionFlowPendingPython+'\n'+str(actionCode)

        def actionFlowPendingRemoveEnd(self):
            self.actionFlowPendingJSON.pop()
            if len(self.actionFlowPendingPython.split('##',1))>0:
                self.actionFlowPendingPython=self.actionFlowPendingPython.split('##',1)[-1]
            else:
                self.actionFlowPendingPython=""

        # operation for actionCurrent
        def actionCurrentGet(self):
            return self.actionCurrentJSON,self.actionCurrentPython
        
        def actionCurrentUpdate(self,actionCode):
            actionJSON,actionCode=self.actionFlowTranslatePython(actionCode)
            self.actionCurrentJSON=actionJSON
            self.actionCurrentPython=str(actionCode)
        
        def actionCurrentRemove(self):
            self.actionCurrentJSON=[]
            self.actionCurrentPython=""

        # import the action from the actionFlowPending to actionCurrent
        def actionCurrentLoad(self):
            self.actionCurrentUpdate(self.actionFlowPendingGetFront()[1])
            self.actionFlowPendingRemoveFront()

        # save the action from actionCurrent to actionFlowPending
        def actionCurrentSave(self):
            self.actionFlowHistoryAddToFront(self.actionCurrentGet()[1]) 
            self.actionCurrentRemove()

        # put the action from actionCurrent to actionOnGoing
        def actionCurrentExecute(self):
            self.actionOnGoing.put(self.actionCurrentPython)


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

            print("Initializing------------------------------------------")
            print("Initialized Function: "+funcName)
            print("actionFlowPendingPython:")
            print(self.codeThreadActionFlow.actionFlowPendingPython)
            print("InitializedActionFlowJSON:"+str(self.codeThreadActionFlow.actionFlowPendingJSON))
            print("Initialize Done----------------------------------------")
            

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

        print("Import Done--------------------------------------------")


        while True:
            print("Action Start-------------------------------------------")
            action = self.codeThreadActionFlow.actionOnGoing.get()

            print("action:",action)
            if action is None:
                break
            
            exec(action)

            self.codeThreadActionFlow.actionOnGoing.task_done()

    def do(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey

        print("doing...")

        from prompt.actionFlowPrompt import ActionDo

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionParameter=LLMChain(llm=llm, prompt= ActionDo)

        import actionDefault

        self.functionsDescriptionAndExample= actionDefault.getDescriptionAndExample()

        agentExperience="none"

        newCode=fillingActionParameter.predict(goal=self.goal,
                                               current_action=self.codeThreadActionFlow.actionOnGoing,
                                                current_action_Python= self.codeThreadActionFlow.actionCurrentPython,
                                                code_history=self.codeThreadActionFlow.actionFlowHistoryPython,
                                                code_future="",
                                                enviroment=self.environment,
                                                function_description_and_example=self.functionsDescriptionAndExample,
                                                experiences=agentExperience)
                                                

        newCodeOnly=newCode.replace("```python\n", "").replace("\n```", "")

        print("newCode:")
        print(newCodeOnly)

        # import tools, initialize the agent
        self.codeThreadActionFlow.actionPendingUpdate("from actionDefault import AskHumanForHelp")

        # run the code
        self.codeThreadActionFlow.actionPendingUpdate(newCodeOnly)

        print("newCodeEnd")


'''
if __name__ == '__main__':

    puppy = CodeThread()

    @puppy.codeThread
    def action():

        ## Invite people
        puppy.do()

    def trigger():
        pass

    puppy.run()
'''



class Puppy(CodeThread):
    def __init__(self):
        super().__init__()

    def run(self):
        self.codeThreadRun()




if __name__ == '__main__':

    Mei = Puppy()

    @Mei.codeThread
    def action():
        
        ## searth the top 5 earphones in chinese market
        print("hello")

        ## send message to my dad
        Mei.do()

    '''
    @Yuning.goalThread
    def action():

        ## set the goal to "make the world better"
        Yuning.setGoal("make the world better")
        Yuning.update
        Yuning.do()
    '''
        
    Mei.run()
