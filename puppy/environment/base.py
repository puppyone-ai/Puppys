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

    """
    vars(self): (current level) all 
    detail: (current level) non-private 
    expose: (hierarchy) non-private 
    """

    @property
    def detail_dict(self) -> dict:
        return self._show_detail()

    @property
    def detail_json(self) -> str:
        import json
        return json.dumps(self._show_detail())

    def _show_detail(self) -> dict:
        """
        This method is used to show all non-private attributes under this env
        """

        non_private_dict = {}

        mro_classes = self.__class__.__mro__

        for key, value in vars(self).items():

            if not any(key.startswith('_' + cls.__name__ + '__') for cls in mro_classes):  # to filter all private
                non_private_dict.update({key: value})

        return non_private_dict

    def expose(self, as_json: bool = False) -> [dict, str]:
        """
        This method is used to show all non-private attributes under this env
        """

        view_dict = {}

        for key, value in self.detail_dict.items():

            if isinstance(value, EnvBase) is False:  # if target is an env or default var
                view_dict.update({key: value})
            else:
                view_dict.update({key: value.expose()})

        import json

        return view_dict if as_json is False else json.dumps(view_dict)

    # Monkey Patching
    # create a new env instance in this env instance
    def create_new_env(self, *args, **kwargs):

        instance = EnvBase(*args, **kwargs)
        setattr(self, instance.name, instance)

    # Monkey Patching
    # add an existed env instance into this env instance
    def add_env(self, env_instance: EnvBase):
        instance = env_instance
        setattr(self, env_instance.name, instance)

    def delete_env(self,
                   env_name: str = None,
                   env_instance: EnvBase = None):
        if env_name is not None:
            delattr(self, env_name)

        if env_instance is not None:
            delattr(self, env_instance.name)


def new_env(*args, **kwargs):
    return EnvBase(*args, **kwargs)


if __name__ == "__main__":
    """
    Three method that can create a new env in an env:
    """

    # method 1 (with 'add_new_env' monkey patching)
    building = EnvBase(name='building', visible=True)

    floor_1 = EnvBase(name='floor_1', visible=True)

    building.add_env(floor_1)

    print(building.expose())

    ## method 2 (with 'create_new_env' monkey patching)
    building = EnvBase(name='building', visible=True)

    building.create_new_env(name='floor_1', visible=True)

    print(building.expose())


    ## method 3 (Recommended, define an env method in a class)
    class Building(EnvBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.floor_1 = EnvBase(name='floor_1', visible=True)


    building = Building(name='building', visible=True)
    print(building.expose())
