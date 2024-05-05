from .base import ThreadBase
from puppy.thread.actionflow.actionflow import Actionflow
from puppy.thread.do import check, achieve, conceive
from puppy.utils.std import redirected_stdout
from puppy.tools.usable_tools import UsableTools


class Thread(ThreadBase):
    def __init__(self, **kwargs):

        super().__init__()

        # naming the thread
        self._naming(**kwargs)

        # set the  of the thread
        self.goal = ""
        self.action_attention = None

        # create a buffer and exec_environment for the thread
        import io
        self.exec_environment = {"self": self}
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
            self.tool_box.load_tool(tool(thread_instance=self))

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

                self.actionflow.on_going.put(action)

                action = self.actionflow.on_going.get()

                # STEP 2.2: check if the action is fixed, semi-fixed, or changeable, and run sequentially
                if action.status == "fixed":
                    exec(action.code, self.exec_environment)
                    self.actionflow.history_list.put_action(action)

                elif action.status == "semi-fixed":
                    self.action_attention = action  # set the action to attention
                    self._do(self.action_attention)

                # TODO: finish the changeable mode
                elif action.status == "changeable":
                    actions_conceive = conceive(thread_instance=self, action=action, seed_num=1, show_prompt=True)
                    for action in actions_conceive:
                        self.action_attention = action
                        self._do(self.action_attention)

        self.actionflow.save_actionflow_history()

    def _do(self, attention, iterate_limit: int = 0) -> None:

        self.exec_environment["finishedOrNot"] = False

        # check(thread_instance=self, action=attention, show_prompt=False)

        # try action till this action has been achieved

        cnt = 0

        while self.exec_environment["finishedOrNot"] is not True and (cnt < iterate_limit or iterate_limit == 0):

            # generate and write the code that can achieve the given action
            action_plan = achieve(thread_instance=self, action=attention, show_prompt=False)

            # execute the generated code in thread's environment and redirect the stdout to the buffer
            with redirected_stdout(self.buffer):
                exec(action_plan.code, self.exec_environment)

            self.actionflow.history_list.put_action(action_plan)

            # check the action, return 'finishOrNot= True / False'
            check(thread_instance=self, action=action_plan, show_prompt=False)

            cnt += 1

    def run(self) -> None:
        # start the code thread
        import threading
        thread_code = threading.Thread(target=self.default_decisiontree)
        thread_code.daemon = False
        thread_code.start()

        # end the code thread
        thread_code.join()
