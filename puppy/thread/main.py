from .base import ThreadBase
from puppy.thread.actionflow.actionflow import Actionflow
from puppy.thread.do import plan_next_action, check_if_action_achieved, achieve_action
from contextlib import redirect_stdout, redirect_stderr
from puppy.tools.usable_tools import UsableTools
from puppy.environment.base import EnvBase


class Thread(ThreadBase):
    def __init__(self, goal='', **kwargs):

        super().__init__()

        # naming the thread
        self._naming(**kwargs)

        # set the  of the thread
        self.goal = goal

        # create the buffer and exec_environment for the thread
        import io

        self.global_var_dict = globals()
        self.runtime_vars_dict = {}
        self.runtime_vars_dict.update({'self': self})

        self.output_buffer = io.StringIO()
        self.error_buffer = io.StringIO()

        # import the actionflow as an env_var that running all actions
        self.actionflow = Actionflow(thread_instance=self)

        # import the toolbox as an env_var that involves all default functions
        self.tool_box = UsableTools(thread_instance=self)

        print(f"{self.thread_name}: Initialize and Done \U0001F3B2")

    # naming the thread with args
    def _naming(self, **kwargs) -> None:
        # if 'puppy' in kwargs:
        #     self.puppy = kwargs['puppy']
        #     self.puppy_name = self.puppy.puppy_name
        # else:
        # self.puppy_name = "Mei"  # the name is essential in the prompt

        #
        if 'name' in kwargs:
            self.thread_name = kwargs['name']
            print(f'Created a thread as {self.thread_name}! ')

        else:
            self.thread_name = "Ur Thread"
            print(f'Created a thread !')

    # set the default decision tree for run the actionflow
    def default_decisiontree(self) -> None:

        # load tools
        for tool in self.tool_box.default_tools:
            self.tool_box.load_tool(tool)

        # start the actionflow

        while self.actionflow.pending_list:

            print("\n\U0001F525 Actionflow Run ----------------------------------------------------------------------")

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

        # set the finishedOrNot to False before all starts
        self.runtime_vars_dict["finishedOrNot"] = False

        # try action till this action has been achieved
        while self.runtime_vars_dict["finishedOrNot"] is not True:

            # generate and write the code that can achieve the given action
            action_plan = achieve_action(thread_instance=self, action=attention, show_prompt=True)

            # execute the generated code in thread's environment
            self.thread_exec(action_plan.code)

            # check if the code has been run successfully
            if self.error_buffer.getvalue() == '':

                # put the action into the history list
                self.actionflow.history_list.put_action(action_plan)

                # if the code has no error, check if the action is achieved, return 'finishOrNot= True / False'
                check_code = check_if_action_achieved(thread_instance=self, action=action_plan, show_prompt=False)
                self.thread_exec(check_code)

            else:
                # if the code has error, add the error message to the action_plan
                action_plan.code += f'\n# Error: {self.error_buffer.getvalue()}'

                # put the action into the history list
                self.actionflow.history_list.put_action(action_plan)

                # clear the error buffer, to avoid the error message from the last run
                self.error_buffer.seek(0)
                self.error_buffer.truncate()

                # do the action again
                self._do(self.actionflow.on_going)

    def thread_exec(self, code):
        # redirect the stdout and stderr to the buffer
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            exec(code, self.global_var_dict, self.runtime_vars_dict)

    @property
    def vars_preview(self, characters_num=200):
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
