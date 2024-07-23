from puppys.env.env import Env


# A default essential env for agent
class PuppyVars(Env):
    """
    An essential env for agent.
    It shows the preview of the runtime variables.
    It inherits from the Env class to be an invisible environment.

    Init Args:
        puppy_instance (any): The instance of the agent.
        global_dict (dict, optional): The global dictionary. Defaults to None.
        runtime_dict (dict, optional): The runtime dictionary. Defaults to None.
        preview_num (int, optional): The number of characters to preview. Defaults to 300.
    """

    visible = False

    def __init__(
        self, 
        puppy_instance: any, 
        global_dict: dict = None, 
        runtime_dict: dict = None, 
        preview_num: int = 300, 
        *args, 
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        if not runtime_dict:
            runtime_dict = {}

        if not global_dict:
            global_dict = {}

        self.global_dict = global_dict
        self.runtime_dict = runtime_dict

        self.global_dict.update(globals())
        self.runtime_dict.update({"self": puppy_instance})

        self.preview_num=preview_num

    def add_runtime_vars(
        self, 
        dict: dict
    ) -> None:
        """
        Add runtime variables to the runtime dictionary.

        Args:
            dict (dict): The dictionary of the runtime variables.
        """

        self.runtime_dict.update(dict)

    def delete_runtime_vars(
        self, 
        keys: list
    ) -> None:
        """
        Delete runtime variables from the runtime dictionary.

        Args:
            keys (list): The list of keys to delete.
        """

        for key in keys:
            if key in self.runtime_dict:
                del self.runtime_dict[key]

    def clear_runtime(self):
        """
        Clear the runtime dictionary.
        """

        self.runtime_dict.clear()

    def preview(self):
        """
        Preview all the values inside the runtime dictionary.
        """

        dict_temp = {}

        for key, value in self.runtime_dict.items():
            string_data = str(value)
            preview_info = string_data[:self.preview_num]
            dict_temp.update({key: {"type": type(value), "preview": preview_info}})

        return dict_temp

