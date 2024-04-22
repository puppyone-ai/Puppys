from puppy.thread.base import ThreadBase


class EnvBase:

    def __init__(self,
                 name: str = "",
                 intro: str = '',
                 # detail: str = '',
                 visibility: bool = False,
                 **kwargs
                 ):

        # the name of this environment var
        self.name = name

        # description of this environment var
        self.intro = intro

        # the overview of the env var
        self.detail = {
            "name": self.name,
            "tag": "env",
            "intro": self.intro}

        # sort the env vars
        self.tag = []

        # if this var is default visible for .expose() or not
        self.visibility = visibility

        # the thread instance that this env var belongs to
        if 'thread_instance' in kwargs and 'parent_env' in kwargs:
            raise ValueError("You can't assign both thread_instance and parent_env to the same env var.")

        else:
            if 'thread_instance' in kwargs:
                self.parent = kwargs['thread_instance']

            elif 'parent_env' in kwargs:
                self.parent = kwargs['parent_env']

    # show the env inside
    def expose(self):
        vars_dict = vars(self)
        view_dict = {}

        for var in vars_dict:
            # get the value of the var, if it doesn't exist, return True
            if getattr(vars_dict[var], 'visibility', False) is False:
                pass

            elif getattr(vars_dict[var], 'visibility', False) is True:
                view_dict.update({var: vars_dict[var].detail})

        return view_dict

    def new_env(self, **kwargs):

        return EnvBase(**kwargs, parent_env=self)


if __name__ == "__main__":
    Building = EnvBase()
    Building.floor_1 = Building.new_env(visibility=True)

    print(Building.expose())
