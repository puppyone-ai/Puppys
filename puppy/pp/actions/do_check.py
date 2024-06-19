def do_check(puppy_instance,
             action_name: str = "",
             tool_list: list = [],
             model="gpt-4-turbo",
             show_prompt=False, show_response=False):

    if hasattr(puppy_instance, 'do') and hasattr(puppy_instance, 'check'):

        puppy_instance.runtime_vars_dict["isFinished"] = False

        while puppy_instance.runtime_vars_dict["isFinished"] == False:
            puppy_instance.do(action_name=action_name, tool_list=tool_list, model=model, show_prompt=show_prompt, show_response=show_response)
            puppy_instance.check(action_name=action_name, tool_list=tool_list, model=model, show_prompt=show_prompt, show_response=show_response)

        puppy_instance.current_code = ""
