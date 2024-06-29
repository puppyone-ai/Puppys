def do_check(puppy_instance,
             action_name: str = "",
             tool_list: list = None,
             model="gpt-4-turbo",
             show_prompt=False, show_response=False):

    if hasattr(puppy_instance, 'do') and hasattr(puppy_instance, 'check'):

        checking_result = False

        # do the action till the checking result is true
        while checking_result == False:

            # do the action and return the ran code
            new_code=puppy_instance.do(action_name=action_name, tool_list=tool_list, model=model, show_prompt=show_prompt, show_response=show_response)

            # add the ran code into the current code until the checking result is true
            puppy_instance.actionflow.current_code += new_code
            puppy_instance.actionflow.current_code += "\n"

            # check if the action is finished or not, return True or False
            checking_result = puppy_instance.check(action_name=action_name, tool_list=tool_list, model=model, show_prompt=show_prompt, show_response=show_response)

            # if the result is True, clear the current code and end the while loop
            if checking_result is True:
                puppy_instance.actionflow.current_code = ""

