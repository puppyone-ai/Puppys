from .base import ThreadBase
from puppy.thread.actionflow.actionflow import Actionflow
from puppy.thread.do import plan_next_action, check_if_action_achieved, achieve_action
from puppy.utils.std import redirected_stdout
from puppy.tools.usable_tools import UsableTools
from puppy.environment.base import EnvBase
import copy


class Thread(ThreadBase):
    def __init__(self, **kwargs):

        super().__init__()

        # naming the thread
        self._naming(**kwargs)

        # set the  of the thread
        self.goal = ""

        # create a buffer and exec_environment for the thread
        import io


        self.vars_dict = globals()
        self.vars_dict.update({'self': self})
        self.runtime_vars_dict = {}

        self.buffer = io.StringIO()

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
                    exec(action.code, self.exec_context)
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

        self.vars_dict["finishedOrNot"] = False

        # try action till this action has been achieved

        while self.vars_dict["finishedOrNot"] is not True :

            # generate and write the code that can achieve the given action
            action_plan = achieve_action(thread_instance=self, action=attention, show_prompt=False)

            # execute the generated code in thread's environment and redirect the stdout to the buffer
            with redirected_stdout(self.buffer):
                self.thread_exec(action_plan.code)

            self.actionflow.history_list.put_action(action_plan)

            # check the action, return 'finishOrNot= True / False'
            check_code=check_if_action_achieved(thread_instance=self, action=action_plan, show_prompt=False)

            self.thread_exec(check_code)

    def thread_exec(self, code):
        previous_env_dict = self.vars_dict.copy()

        exec(code, self.vars_dict)

        new_globals = {k: v for k, v in self.vars_dict.items() if k not in previous_env_dict or previous_env_dict[k] != v}

        self.runtime_vars_dict.update(new_globals)

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


