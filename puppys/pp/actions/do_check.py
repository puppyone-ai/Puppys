def do_check(puppy_instance,
             action_name: str = "",
             model="gpt-4-turbo",
             show_prompt=False, show_response=False):

    """
    do the action and check if it finished or not
    """

    if hasattr(puppy_instance, 'do') and hasattr(puppy_instance, 'check'):

        checking_result = False

        # do the action till the checking result is true
        while checking_result == False:

            # do the action and return the ran code
            puppy_instance.do(action_name=action_name, model=model, show_prompt=show_prompt, show_response=show_response)

            # check if the action is finished or not, return True or False
            checking_result = puppy_instance.check(action_name=action_name, model=model, show_prompt=show_prompt, show_response=show_response)

            # if the result is True, clear the current code and end the while loop
            if checking_result is True:
                puppy_instance.actionflow.current_action_code = ""

