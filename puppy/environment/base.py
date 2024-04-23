from __future__ import annotations

class EnvBase:

    def __init__(self,
                 name: str = "",
                 intro: str = '',
                 visibility: bool = False,
                 parent=None,
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

        # the parental instance that this env var connected from
        if parent:
            self.parent = parent
            setattr(parent, name, self)

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

    # Monkey Patching
    # create a new env instance in this env instance
    def create_new_env(self, *args, **kwargs):

        instance = EnvBase(*args, **kwargs, parent=self)
        setattr(self, kwargs['name'], instance)

    # Monkey Patching
    # add an existed env instance into this env instance
    def add_new_env(self, EnvExample : EnvBase):
        instance = EnvExample
        setattr(self, EnvExample.name, instance)


    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            print(f"Error: {e}")
            return None




if __name__ == "__main__":
    """
    Three method that can create a new env in an env:
    """

    # method 1 (with 'add_new_env' monkey patching)
    building = EnvBase()

    floor_1 = EnvBase(name='floor_1', visibility=True)

    building.add_new_env(floor_1)

    print(building.expose())


    ## method 2 (with 'create_new_env' monkey patching)
    building = EnvBase()

    building.create_new_env(name='floor_1', visibility=True)

    print(building.expose())

    ## method 3 (Recommended, define a env method in a class)
    class Building(EnvBase):
        def __init__(self):
            super().__init__(name='Building', visibility=True)

            self.floor_1 = EnvBase(name='floor_1', visibility=True)

    building=Building()
    print(building.expose())