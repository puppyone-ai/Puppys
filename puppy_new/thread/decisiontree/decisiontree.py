from puppy.thread.decisiontree.do import plan_next_action, check_if_action_achieved, achieve_action

# default decisiontree
def default_decisiontree(self) -> None:

    # load the tools in the tool_box
    for tool in self.tool_box.default_tools:
        self.tool_box.load_tool(tool)

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

            action = self.actionflow.current_list.pop_action()

            # STEP 2.2: check if the action is fixed, semi-fixed, or changeable, and run sequentially
            if action.status == "fixed":
                self.thread_exec(action.code)
                self.actionflow.history_list.put_action(action)

            elif action.status == "semi-fixed":
                self.actionflow.on_going = action
                _do(threadInstance=self, action_now=self.actionflow.on_going)

            elif action.status == "changeable":
                action_refined = plan_next_action(thread_instance=self, action=action, show_prompt=False)
                self.actionflow.on_going = action_refined
                self._do(self.actionflow.on_going)

    self.actionflow.save_actionflow_history()

def _do(threadInstance, action_now) -> None:

    threadInstance.runtime_vars_dict["finishedOrNot"] = False

    # try action till this action has been achieved

    while threadInstance.runtime_vars_dict["finishedOrNot"] is not True:
        # generate and write the code that can achieve the given action
        action_plan = achieve_action(thread_instance=threadInstance, action=action_now, show_prompt=False)

        # execute the generated code in thread's environment
        threadInstance.thread_exec(action_plan.code)

        threadInstance.actionflow.history_list.put_action(action_plan)

        # check the action, return 'finishOrNot= True / False'
        check_code = check_if_action_achieved(thread_instance=threadInstance, action=action_plan, show_prompt=False)

        threadInstance.thread_exec(check_code)