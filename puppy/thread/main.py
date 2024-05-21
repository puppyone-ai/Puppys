from .base import ThreadBase
from puppy.thread.actionflow.actionflow import Actionflow

from puppy.thread.do import plan_next_action, check_if_action_achieved, achieve_action
from contextlib import redirect_stdout, redirect_stderr

from puppy.tools.usable_tools import UsableTools
from puppy.environment.base import EnvBase


class Thread(ThreadBase):
    def __init__(self, goal='', print_mode='terminal', **kwargs):

        super().__init__()

        # naming the thread
        self.thread_name = kwargs['name'] if 'name' in kwargs else "Default Thread"
        print(f'Created a thread as {self.thread_name}! ')

        # set the  of the thread
        self.goal = goal

        # add exec_environment for the thread
        self.global_var_dict = globals()
        self.runtime_vars_dict = {}
        self.runtime_vars_dict.update({'self': self})

        # cache print from exec_environment
        import io
        import sys

        self.output_buffer = sys.__stdout__
        self.error_buffer = sys.__stderr__

        if 'print_mode' in kwargs:
            if kwargs['print_mode'] == 'buffer':
                self.output_buffer = io.StringIO()
                self.error_buffer = io.StringIO()

        # import the actionflow as an env_var that running all actions
        self.actionflow = Actionflow(thread_instance=self)

        # import the toolbox as an env_var that involves all default functions
        self.tool_box = UsableTools(thread_instance=self)

    # set the default decision tree for run the actionflow
    def default_decisiontree(self) -> None:

        # load tools
        self.tool_box.inventory_tools()

        print(f"\U0001F3B2 Initialize Done ")

        # start the actionflow
        while self.actionflow.pending_list:

            print("\U0001F525 New Action Run")

            # STEP 1: take out the action from ActionFlowPending and put into ActionFlowCurrent

            action = self.actionflow.pending_list.pop_action()

            self.actionflow.current_list.put_action(action)

            # STEP 2: pop out action from ActionFlowCurrent put into ActionOnGoing and run

            while self.actionflow.current_list:

                # STEP 2.1: load the action to ActionOnGoing (for scalability in the future version)

                self.actionflow.show_status()  # print the actionflow

                action = self.actionflow.current_list.pop_action()

                # STEP 2.2: check if the action is fixed, semi-fixed, or changeable, and run sequentially
                if action.status == "fixed":
                    self.thread_exec(action.code)
                    self.actionflow.history_list.put_action(action)

                elif action.status == "semi-fixed":
                    self.actionflow.on_going = action
                    self._do(self.actionflow.on_going)

                elif action.status == "changeable":
                    action_refined = plan_next_action(thread_instance=self, action=action, show_prompt=False)
                    self.actionflow.on_going = action_refined
                    self._do(self.actionflow.on_going)

        self.actionflow.save_actionflow_history()

    def _do(self, attention) -> None:

        self.runtime_vars_dict["finishedOrNot"] = False

        # try action till this action has been achieved

        while self.runtime_vars_dict["finishedOrNot"] is not True:
            # generate and write the code that can achieve the given action
            action_plan = achieve_action(thread_instance=self, action=attention, show_prompt=False)

            # execute the generated code in thread's environment
            self.thread_exec(action_plan.code)

            self.actionflow.history_list.put_action(action_plan)

            # check the action, return 'finishOrNot= True / False'
            check_code = check_if_action_achieved(thread_instance=self, action=action_plan, show_prompt=False)

            self.thread_exec(check_code)

    def thread_exec(self, code):
        # redirect the stdout and stderr to the buffer
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            exec(code, self.global_var_dict, self.runtime_vars_dict)

    @property
    def vars_preview(self, characters_num=300):
        dict_temp = {}

        for key, value in self.runtime_vars_dict.items():
            string_data = str(value)
            preview_info = string_data[:characters_num]
            dict_temp.update({key: {"type: ": type(value), "preview:": preview_info}})

        return dict_temp

    def run(self) -> None:
        # start the code thread
        import threading
        thread_code = threading.Thread(target=self.default_decisiontree)
        thread_code.daemon = False
        thread_code.start()

        # end the code thread
        thread_code.join()
