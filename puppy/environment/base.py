from __future__ import annotations


class EnvBase:

    def __init__(self,
                 name: str = "",
                 description: str = "",
                 visibility: bool = None,
                 sub_env_list:list = [],
                 *args, **kwargs
                 ):

        # the name of this environment var
        self.__name = name

        # description of this environment var
        self.__description = description

        # the tag of this environment var
        self.tag = "env"

        # if this var is default visible for .expose() or not
        self.__visibility = visibility if visibility is not None else False

        # if the sub env list is empty
        self.sub_env_list = sub_env_list

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def visibility(self):
        return self.__visibility

    @visibility.setter
    def visibility(self, value):
        self.__visibility = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value

    """
    vars(self): (current level) all 
    self.intro: (current level) name and intro as a JSON
    self.explore: (hierarchy) non-private 
    """

    @property
    def intro(self):

        """

        Returns:

        {"name":self.name
        "description":self.description}
        """

        intro_JSON={"name":self.name,
        "description":self.description}

        return intro_JSON

    # recursively show non-private attributes under this env
    def explore(self, return_mode : str = "default"):

        """

        Returns:

        {intro:{}
        sub_env_list:[
        {intro:{}]}
        """

        all_JSON = {}

        sub_env_intro_list=[]
        for sub_env in self.sub_env_list:
            sub_env_intro_list.append(sub_env.intro)

        if return_mode == "default":
            all_JSON["intro"] = self.intro
            all_JSON["sub_env_list"] = sub_env_intro_list
            return all_JSON

        elif return_mode =="sub_only":
            return sub_env_intro_list

        else:
            raise ValueError("the explore return_mode must be 'default' or 'sub_only'")

    # Monkey Patching
    # create a new env instance in this env instance
    def create_new_env(self, *args, **kwargs):

        instance = EnvBase(*args, **kwargs, parent=self)
        self.sub_env_list.append(instance)

    # Monkey Patching
    # add an existed env instance into this env instance
    def add_new_env(self, env_example: EnvBase):
        instance = env_example
        self.sub_env_list.append(instance)

    # clear all sub_env
    def clear_env(self):
        self.sub_env_list = []


def new_env(*args, **kwargs):
    return EnvBase(*args, **kwargs)


if __name__ == "__main__":
    """
    Three method that can create a new env in an env:
    """

    # method 1 (with 'add_new_env' monkey patching)
    building = EnvBase(name='building', visible=True)

    floor_1 = EnvBase(name='floor_1', visible=True)

    building.add_new_env(floor_1)

    print(building.explore)

    ## method 2 (with 'create_new_env' monkey patching)
    building = EnvBase(name='building', visible=True)

    building.clear_env()
    building.create_new_env(name='floor_2', visible=True)

    print(building.sub_env_list)
    print(building.explore)


    ## method 3 (Recommended, define an env method in a class)
    class Building(EnvBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.sub_env_list.clear()
            self.sub_env_list.append(EnvBase(name='floor_3', visible=True))

    building = Building(name='building', visible=True)
    print(building.sub_env_list)
    print(building.explore)
