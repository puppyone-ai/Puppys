import queue

class ActionFlow():
    def __init__(self, codeThreadInstance): 
        self.codeThreadInstance = codeThreadInstance

        self.actionFlowAllJSON = []
        self.actionFlowHistoryJSON = []
        self.actionFlowPendingJSON =[]
        self.actionFlowCurrentJSON=[]
        
        """
        actionFlowAllJSON: [{}]"""

        self.actionOnGoing=queue.Queue()
    
    def initialize(self,sourceCode):


        self.actionFlowHistoryJSON = []
        # updated the actionFlow JSON
        actionFlowInitialJSON, actionFlowInitialPython=self.translatePython(sourceCode)
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
        return self.actionFlowCurrentJSON[0]["code"]
    
    def actionFlowCurrentGetName(self):
        return self.actionFlowCurrentJSON[0]["action"]
    
    def actionFlowCurrentGetFrontAddCode(self,code):
        self.actionFlowCurrentJSON[0]["code"]=self.actionFlowCurrentJSON[0]["code"]+"\n"+code


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

    def actionFlowCurrentSkip(self):
        self.actionFlowCurrentJSON.pop(0)