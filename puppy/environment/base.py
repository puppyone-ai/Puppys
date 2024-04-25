from __future__ import annotations


class EnvBase:

    def __init__(self,
                 name: str = "",
                 intro: str = "",
                 visible: bool = None,
                 *args, **kwargs
                 ):

        # the name of this environment var
        self.name = name

        # description of this environment var
        self.intro = intro

        # the tag of this environment var
        self.tag = "env"

        # if this var is default visible for .expose() or not
        self.__visibility = visible if visible is not None else False

    @property
    def visible(self):
        return self.__visibility

    @visible.setter
    def visible(self, value):
        self.__visibility = value

    # overview of this env
    @property
    def detail(self):
        return vars(self)

    # show the env inside
    @property
    def expose(self):

        view_dict = {}

        for key, value in self.detail.items():

            if key.startswith(f"_EnvBase") is False:  # only expose non-private attributes

                if isinstance(value, EnvBase) is False:  # if the attribute is not an env instance
                    view_dict.update({key: value})
                else:
                    view_dict.update({key: value.expose})

        return view_dict

    # Monkey Patching
    # create a new env instance in this env instance
    def create_new_env(self, *args, **kwargs):

        instance = EnvBase(*args, **kwargs, parent=self)
        setattr(self, kwargs['name'], instance)

    # Monkey Patching
    # add an existed env instance into this env instance
    def add_new_env(self, env_example: EnvBase):
        instance = env_example
        setattr(self, env_example.name, instance)

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
    building = EnvBase(name='building', visible=True)

    floor_1 = EnvBase(name='floor_1', visible=True)

    building.add_new_env(floor_1)

    print(building.expose)

    ## method 2 (with 'create_new_env' monkey patching)
    building = EnvBase(name='building', visible=True)

    building.create_new_env(name='floor_1', visible=True)

    print(building.expose)

    ## method 3 (Recommended, define an env method in a class)
    class Building(EnvBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.floor_1 = EnvBase(name='floor_1', visible=True)

    building = Building(name='building', visible=True)
    print(building.expose)
