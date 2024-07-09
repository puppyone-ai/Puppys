from puppys.env.env import Env

# a default essential env for agent
class PuppyVars(Env):
    """
    An essential env for agent.
    It shows the preview of the runtime variables.
    """
    visible = False

    def __init__(self, puppy_instance, global_dict=None, runtime_dict=None, preview_num=300, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if runtime_dict is None:
            runtime_dict = {}

        if global_dict is None:
            global_dict = {}

        self.global_dict = global_dict
        self.runtime_dict = runtime_dict

        self.global_dict.update(globals())
        self.runtime_dict.update({'self': puppy_instance})

        self.preview_num=preview_num


    def add_runtime_vars(self, dict: dict):
        self.runtime_dict.update(dict)

    def delete_runtime_vars(self, keys: list):
        for key in keys:
            if key in self.runtime_dict:
                del self.runtime_dict[key]

    def clear_runtime(self):
        self.runtime_dict.clear()

    def preview(self):
        dict_temp = {}

        for key, value in self.runtime_dict.items():
            string_data = str(value)
            preview_info = string_data[:self.preview_num]
            dict_temp.update({key: {"type": type(value), "preview": preview_info}})

        return dict_temp

