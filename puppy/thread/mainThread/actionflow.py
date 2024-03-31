import queue
import copy

class Actionflow():
    def __init__(self, thread_instance):
        self.thread_instance = thread_instance

        self.actionflow_all_JSON = []
        self.actionflow_history_JSON = []
        self.actionflow_pending_JSON =[]
        self.actionflow_current_JSON=[]
        
        """
        actionFlowAllJSON: [{}]"""

        self.action_on_going=queue.Queue()
    
    def initialize(self, source_code):


        self.actionflow_history_JSON = []
        # updated the actionFlow JSON
        action_flow_initial_JSON, action_flow_initial_python=self.translate_python(source_code)
        self.actionflow_pending_add_to_front(action_flow_initial_JSON)


    # return the actionFlowHistoryJSON and actionFlowHistoryPython by ## in the source code
    def translate_python(self, sourceCode: str):

        """
        translate the source code to actionflow_json and actionflow_python

        args: sourceCode(Python)
        return: actionFlowHistoryJSON(List), actionFlowHistoryPython(String)
        """

        ## initialize the actionflow_json and actionflow_python
        actionflow_json=[]
        actionflow_python=[]

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
            adjusted_source_code = '\n'.join(adjusted_lines)
        else:
            adjusted_source_code = sourceCode


        ## return the actionflow_json
        lines = adjusted_source_code.split('\n')

        search_for_code=False

        comment = ""
        code_snippet = ""
        actionflow_json = []

        for line in lines:
            if '##' in line:
                if search_for_code==True:
                    actionflow_json.append({"action": comment, "code": "## "+comment+"\n"+code_snippet.strip()})
                else:
                    pass
                comment = line.split('##', 1)[1].strip()
                search_for_code = False
                code_snippet = ""
            else:
                if line.strip()!="":
                    search_for_code=True
                    code_snippet += line + '\n'  # history code snippet
                else:
                    pass


        # deal with the last action
        if search_for_code==True:
            actionflow_json.append({"action": comment,  "code": "## "+comment+"\n"+code_snippet.strip()})

        
        for action in actionflow_json:
            if ".do()"in action["code"]:
                if action["action"]=="":
                    action["status"]= "changeable"
                else:
                    action["status"]="semi-fixed"

            else:
                action["status"]="fixed"

        ## return the actionflow_python
        for action in actionflow_json:
            actionflow_python.append(action["code"])

        return actionflow_json, actionflow_python

    def decorate_actionflow_code_to_json(self, name, code, status):
        actionJSON={
            "action": name,
            "code": code,
            "status": status
        }

        return [actionJSON]


    # operation for actionFlowHistory
    def actionflow_history_get_code(self):
        code=""
        for action in self.actionflow_history_JSON:
            code+=action["code"]+"\n"

        return code

    def actionflow_history_get_front(self):
        return self.actionflow_history_JSON[0]

    def actionflow_history_add_to_front(self, actionFlowJSON):
        self.actionflow_history_JSON= actionFlowJSON + self.actionflow_history_JSON
        
    def actionflow_history_remove_front(self):
        self.actionflow_history_JSON.pop(0)

    def actionflow_history_get_end(self):
        return self.actionflow_history_JSON[-1]
    
    def actionflow_history_add_to_end(self, actionFlowJSON):
        self.actionflow_history_JSON= self.actionflow_history_JSON + actionFlowJSON

    def actionflow_history_remove_end(self):
        self.actionflow_history_JSON.pop()

    # operation for actionFlowPending
    def actionflow_pending_get_code(self):
        code=""
        for action in self.actionflow_pending_JSON:
            code+=action["code"]+"\n"

        return code

    def actionflow_pending_get_front(self):
        return self.actionflow_pending_JSON[0]
    
    def actionflow_pending_add_to_front(self, actionFlowJSON):
        self.actionflow_pending_JSON= actionFlowJSON + self.actionflow_pending_JSON
        
    def actionflow_pending_remove_front(self):
        self.actionflow_pending_JSON.pop(0)

    def actionflow_pending_get_end(self):
        return self.actionflow_pending_JSON[-1]
    
    def actionflow_pending_add_to_end(self, actionFlowJSON):
        self.actionflow_pending_JSON= self.actionflow_pending_JSON + actionFlowJSON

    def actionflow_pending_remove_end(self):
        self.actionflow_pending_JSON.pop()

    # operation for actionFlowCurrent
    def actionflow_current_get_code(self):
        return self.actionflow_current_JSON[0]["code"]

    # a deep copy of action's name
    def actionflow_current_get_name(self):
        action_dict = self.actionflow_current_JSON[0]["action"]
        action_dict_deep_copy = copy.deepcopy(action_dict)
        return action_dict_deep_copy
    
    def actionflow_current_get_front_add_code(self, code):
        self.actionflow_current_JSON[0]["code"]= self.actionflow_current_JSON[0]["code"] + "\n" + code


    def actionflow_current_skip(self):
        self.actionflow_current_JSON.pop(0)
    
    def actionflow_current_get_front(self):
        return self.actionflow_current_JSON[0]
    
    def actionflow_current_add_to_front(self, actionFlowJSON):
        self.actionflow_current_JSON= actionFlowJSON + self.actionflow_current_JSON
        
    def actionflow_current_remove_front(self):
        self.actionflow_current_JSON.pop(0)

    def actionflow_current_get_end(self):
        return self.actionflow_current_JSON[-1]
    
    ##
    def actionflow_current_add_to_end(self, actionFlowJSON):
        self.actionflow_current_JSON= self.actionflow_current_JSON + actionFlowJSON

    def actionflow_current_remove_end(self):
        self.actionflow_current_JSON.pop()

    def actionflow_current_clear(self):
        self.actionflow_current_JSON=[]

    # change the status of the actionFlowCurrent Front
    def actionflow_current_status_change_front(self, status):
        self.actionflow_current_JSON[0]["status"]=status


    # import the action from the actionFlowPending to actionCurrent
    def action_current_load(self):
        self.actionflow_current_add_to_end([self.actionflow_pending_get_front()])

    # save the action from actionCurrent to actionFlowPending
    def action_current_save(self):
        self.actionflow_history_add_to_end([self.actionflow_current_get_front()])

    # put the action from actionCurrent to actionOnGoing
    def action_current_execute(self):
        self.action_on_going.put(self.actionflow_current_JSON[0]["code"])
