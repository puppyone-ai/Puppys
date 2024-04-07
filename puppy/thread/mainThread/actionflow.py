import queue
import copy
from .base import ThreadBase
from .actions import Actions


class Actionflow:
    def __init__(self, thread_instance: ThreadBase):
        self.thread_instance = thread_instance
        self.actions_current = []
        self.action_current = {}

        # self.actionflow_all_JSON = []
        self.actionflow_history = []
        self.actionflow_pending = []
        self.actionflow_current = []
        
        # """
        # actionFlowAllJSON: [{}]"""

        """
        action: {}
        actions: [{},{}]
        actionflow: [[{},{}],[{}]]
        (action_history:[{},{}])
        """

        self.action_on_going = queue.Queue()

    def load_actions(self, actions: Actions):
        self.actionflow_pending.append(actions)

    # def initialize(self, source_code: str):
    #
    #     self.actionflow_history = []
    #     # updated the actionFlow JSON
    #     action_flow_initialized = self.translate_python(source_code)
    #     self.actionflow_pending_add_to_front(action_flow_initialized)

    # def translate_python(source_code: str):
    #
    #     """
    #     translate the source code to actionflow_json and actionflow_python
    #
    #     args: sourceCode(Python)
    #     return: actionFlowHistoryJSON(List), actionFlowHistoryPython(String)
    #     """
    #
    #     ## initialize the actionflow_json and actionflow_python
    #     # actionflow_json = []
    #     # actionflow_python = []
    #
    #     # from str to list
    #     lines = source_code.split('\n')
    #
    #     ## deal with space in the head of the code
    #     comment_pos = None
    #     indent_level = None
    #
    #     # some lines are started with '##', we mark the index of these lines as comment_pos
    #     # and the indent level of before first '##' line as indent_level
    #     for i, line in enumerate(lines):
    #         if '##' in line:
    #             comment_pos = i
    #             indent_level = len(line) - len(line.lstrip(' '))
    #             break
    #
    #     # return the adjusted source code, with is the code without the indent
    #     # if the indent level is found, adjust the indent of the whole function
    #     if comment_pos is not None and indent_level is not None:
    #
    #         # delete all the code before the '##' comment
    #         lines = lines[comment_pos:]
    #
    #         adjusted_lines = []
    #         for line in lines:
    #             # only adjust the indent of non-empty lines
    #             if line.strip():
    #                 adjusted_lines.append(line[indent_level:])
    #             else:
    #                 adjusted_lines.append(line)
    #         # list -> str
    #         adjusted_source_code = '\n'.join(adjusted_lines)
    #
    #     # error!!
    #     else:
    #         adjusted_source_code = source_code
    #
    #     ## return the actionflow_json
    #     lines = adjusted_source_code.split('\n')
    #
    #     search_for_code=False
    #
    #     comment = ""
    #     code_snippet = ""
    #     actionflow_json = []
    #
    #     for line in lines:
    #         if '##' in line:
    #             if search_for_code==True:
    #                 actionflow_json.append({"action": comment, "code": "## "+comment+"\n"+code_snippet.strip()})
    #             else:
    #                 pass
    #             comment = line.split('##', 1)[1].strip()
    #             search_for_code = False
    #             code_snippet = ""
    #         else:
    #             if line.strip()!="":
    #                 search_for_code=True
    #                 code_snippet += line + '\n'  # history code snippet
    #             else:
    #                 pass
    #
    #
    #     # deal with the last action
    #     if search_for_code==True:
    #         actionflow_json.append({"action": comment,  "code": "## "+comment+"\n"+code_snippet.strip()})
    #
    #
    #     for action in actionflow_json:
    #         if ".do()"in action["code"]:
    #             if action["action"]=="":
    #                 action["status"]= "changeable"
    #             else:
    #                 action["status"]="semi-fixed"
    #
    #         else:
    #             action["status"]="fixed"
    #
    #     # ## return the actionflow_python
    #     # for action in actionflow_json:
    #     #     actionflow_python.append(action["code"])
    #
    #     return actionflow_json#, actionflow_python

    def decorate_actionflow_code_to_json(self, name, code, status):
        action = {
            "action": name,
            "code": code,
            "status": status
        }

        return [action]

    # operation for actionFlowHistory
    def actionflow_history_get_code(self):
        code = ""
        for action in self.actionflow_history:
            code += action["comment+code"]+"\n"

        return code

    def actionflow_history_get_front(self):
        return self.actionflow_history[0]

    def actionflow_history_add_to_front(self, actionFlowJSON):
        self.actionflow_history= actionFlowJSON + self.actionflow_history
        
    def actionflow_history_remove_front(self):
        self.actionflow_history.pop(0)

    def actionflow_history_get_end(self):
        return self.actionflow_history[-1]
    
    def actionflow_history_add_to_end(self, actionFlowJSON):
        self.actionflow_history= self.actionflow_history + actionFlowJSON

    def actionflow_history_remove_end(self):
        self.actionflow_history.pop()

    # operation for actionFlowPending
    def actionflow_pending_get_code(self):
        code = ""
        for actions in self.actionflow_pending:
            for action in actions:
                code += actions["comment+code"]+"\n"

        return code

    def actionflow_pending_get_front(self):
        return self.actionflow_pending[0]
    
    def actionflow_pending_add_to_front(self, actionFlowJSON):
        self.actionflow_pending= actionFlowJSON + self.actionflow_pending
        
    def actionflow_pending_remove_front(self):
        self.actionflow_pending.pop(0)

    def actionflow_pending_get_end(self):
        return self.actionflow_pending[-1]
    
    def actionflow_pending_add_to_end(self, actionFlowJSON):
        self.actionflow_pending= self.actionflow_pending + actionFlowJSON

    def actionflow_pending_remove_end(self):
        self.actionflow_pending.pop()

    # operation for actionFlowCurrent
    def actionflow_current_get_code(self):
        return self.actionflow_current[0]["code"]

    # a deep copy of action's name
    def actionflow_current_get_name(self):
        action_dict = self.actionflow_current[0]["action"]
        action_dict_deep_copy = copy.deepcopy(action_dict)
        return action_dict_deep_copy
    
    def actionflow_current_get_front_add_code(self, code):
        self.actionflow_current[0]["code"]= self.actionflow_current[0]["code"] + "\n" + code

    def actionflow_current_skip(self):
        self.actionflow_current.pop(0)
    
    def actionflow_current_get_front(self):
        return self.actionflow_current[0]
    
    def actionflow_current_add_to_front(self, actionFlowJSON):
        self.actionflow_current= actionFlowJSON + self.actionflow_current
        
    def actionflow_current_remove_front(self):
        self.actionflow_current.pop(0)

    def actionflow_current_get_end(self):
        return self.actionflow_current[-1]
    
    ##
    def actionflow_current_add_to_end(self, actionFlowJSON):
        self.actionflow_current= self.actionflow_current + actionFlowJSON

    def actionflow_current_remove_end(self):
        self.actionflow_current.pop()

    # def actionflow_current_clear(self):
    #     self.actionflow_current=[]

    # change the status of the actionFlowCurrent Front
    def actionflow_current_status_change_front(self, status):
        self.actionflow_current[0]["status"]=status

    # import the action from the actionFlowPending to actionCurrent
    def action_current_load(self):
        self.actionflow_current_add_to_end([self.actionflow_pending_get_front()])

    # save the action from actionCurrent to actionFlowPending
    # def action_current_save(self):
    #     self.actionflow_history_add_to_end([self.actionflow_current_get_front()])

    # put the action from actionCurrent to actionOnGoing
    # def action_current_execute(self):
    #     self.action_on_going.put(self.actionflow_current[0]["code"])
