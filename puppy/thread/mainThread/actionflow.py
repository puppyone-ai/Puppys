import queue
from .base import ThreadBase
from .actions import Actions


class Actionflow(list):
    def __init__(self, iterable, thread_instance: ThreadBase = None):

        transformed = [str(item) for item in iterable]
        super().__init__(transformed)

        if thread_instance:
            self.thread_instance = thread_instance

        """
        action: Actions
        actionflow: [A,A,A]
        on_going: (A)
        """

    def put_actions(self, actions: Actions) -> None:
        return self.append(actions)

    def pop_actions(self) -> Actions:
        return self.pop(0)

    def get_code(self):

        code = ""

        for actions in self:
            code += actions["code"] + "\n"

        return code


# def decorate_actionflow_code_to_json(self, name, code, status):
#     action = {
#         "action": name,
#         "code": code,
#         "status": status
#     }
#
#     return [action]
#
# # operation for actionFlowHistory
# def actionflow_history_get_code(self):
#     code = ""
#     for action in self.history:
#         code += action["code"]+"\n"
#
#     return code
#
# def actionflow_history_get_front(self):
#     return self.history[0]
#
# def actionflow_history_add_to_front(self, actionFlowJSON):
#     self.history= actionFlowJSON + self.history
#
# def actionflow_history_remove_front(self):
#     self.history.pop(0)
#
# def actionflow_history_get_end(self):
#     return self.history[-1]
#
# def actionflow_history_add_to_end(self, actionFlowJSON):
#     self.history= self.history + actionFlowJSON
#
# def actionflow_history_remove_end(self):
#     self.history.pop()
#
# # operation for actionFlowPending
# def actionflow_pending_get_code(self):
#     code = ""
#     for actions in self.pending:
#         for action in actions.actions_list:
#             code += action["code"]+"\n"
#
#     return code
#
# def actionflow_pending_get_front(self):
#     return self.pending[0]
#
# def actionflow_pending_add_to_front(self, actionFlowJSON):
#     self.pending= actionFlowJSON + self.pending
#
# def actionflow_pending_remove_front(self):
#     self.pending.pop(0)
#
# def actionflow_pending_get_end(self):
#     return self.pending[-1]
#
# def actionflow_pending_add_to_end(self, actionFlowJSON):
#     self.pending= self.pending + actionFlowJSON
#
# def actionflow_pending_remove_end(self):
#     self.pending.pop()
#
# # operation for actionFlowCurrent
# def actionflow_current_get_code(self):
#     return self.current[0]["code"]
#
# # a deep copy of action's name
# def actionflow_current_get_name(self):
#     action_dict = self.current[0]["action"]
#     action_dict_deep_copy = copy.deepcopy(action_dict)
#     return action_dict_deep_copy
#
# def actionflow_current_get_front_add_code(self, code):
#     self.current[0]["code"]= self.current[0]["code"] + "\n" + code
#
# def actionflow_current_skip(self):
#     self.current.pop(0)
#
# def actionflow_current_get_front(self):
#     return self.current[0]
#
# def actionflow_current_add_to_front(self, actionFlowJSON):
#     self.current= actionFlowJSON + self.current
#
# def actionflow_current_remove_front(self):
#     self.current.pop(0)
#
# def actionflow_current_get_end(self):
#     return self.current[-1]
#
# ##
# def actionflow_current_add_to_end(self, actionFlowJSON):
#     self.current= self.current + actionFlowJSON
#
# def actionflow_current_remove_end(self):
#     self.current.pop()
#
# # def actionflow_current_clear(self):
# #     self.actionflow_current=[]
#
# # change the status of the actionFlowCurrent Front
# def actionflow_current_status_change_front(self, status):
#     self.current[0]["status"]=status
#
# # import the action from the actionFlowPending to actionCurrent
# def action_current_load(self):
#     self.actionflow_current_add_to_end([self.actionflow_pending_get_front()])

# save the action from actionCurrent to actionFlowPending
# def action_current_save(self):
#     self.actionflow_history_add_to_end([self.actionflow_current_get_front()])

# put the action from actionCurrent to actionOnGoing
# def action_current_execute(self):
#     self.action_on_going.put(self.actionflow_current[0]["code"])
