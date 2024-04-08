import queue
import copy
from .base import ThreadBase
from .actions import Actions


class Actionflow:
    def __init__(self, thread_instance: ThreadBase):
        self.thread_instance = thread_instance

        self.actions_current = []
        self.action_current = {}

        self.actionflow_history = []
        self.actionflow_pending = []
        self.actionflow_current = []

        """
        action: {}
        actions: [{},{}]
        actionflow: [[{},{}],[{}]]
        (action_history:[{},{}])
        """

        self.action_on_going = queue.Queue()

    def load_actions(self, actions: Actions):
        self.actionflow_pending.append(actions)

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
                code += action["comment+code"]+"\n"

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
