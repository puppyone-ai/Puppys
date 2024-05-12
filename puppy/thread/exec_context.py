from puppy.environment.base import EnvBase


class ExecContext(EnvBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial_vars_dict = {}
        self.vars_dict = {}
        self.intro = "the context of the exec environment"

    def __call__(self, *args, **kwargs):
        return self.vars_dict

    def initialize(self, env_dict):
        self.vars_dict.update(env_dict)
        self.initial_vars_dict.update(env_dict)

    def add(self, env_dict):
        self.vars_dict.update(env_dict)

    @property
    def preview(self, characters_num=100):

        dict_temp = {}

        for key, value in self.vars_dict.items():
            # if key is not in initial_vars_dict
            if key not in self.initial_vars_dict:
                try:
                    string_data = str(value)
                    preview_info = string_data[:characters_num]
                except Exception as e:
                    # if conversion or extraction fails, return an error message
                    print(f"Error: Unable to process when preview {key} input ({e})")
                    continue

                dict_temp.update({key: preview_info})

        return dict_temp
