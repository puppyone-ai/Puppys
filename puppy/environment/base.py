from __future__ import annotations
from typing import Union


class EnvBase:

    visibility: bool = False

    def __init__(self, name, description, *args, **kwargs):

        self.name = name
        self.description = description

        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def window(self):
        return []

    @property
    def intro(self):

        return {"name": self.name, "description": self.description}

    def add_env(self, *args: EnvBase):

        for sub_env in args:
            if isinstance(sub_env, EnvBase):
                setattr(self, sub_env.name, sub_env)
            else:
                raise TypeError('add_env() currently could only dynamically load and link instance from EnvBase.')

    def del_env(self, *args: Union[str, EnvBase]):

        for sub_env in args:

            try:

                if type(sub_env) is str:
                    delattr(self, sub_env)

                elif isinstance(sub_env, EnvBase):

                    keys_to_delete = [k for k, v in self.__dict__.items() if v == sub_env]

                    for key in keys_to_delete:
                        delattr(self, key)

                else:
                    raise TypeError()

            except AttributeError:
                continue

    def clear_env(self):
        self.__dict__.clear()

    def __str__(self):
        try:
            return str({k: str(v.attr_dict) for k, v in self.__dict__.items()})

        except RecursionError as e:
            print(e)


def explore(env: EnvBase,
            return_mode: str = "default",
            as_json: bool = False, as_list: bool = False,
            recursive: bool = False
            ):

    """

    Returns:

    {
    name:*,
    intro:*,
    sub_evn_a:{
               name:**,
               intro:**,
               },
    sub_evn_b:{
               name:***,
               intro:***,
               },
    }
    """

    sub_env_dict = {}

    for key, value in env.__dict__.items():

        if value.window:

            sub_env_dict.update({key: env.__dict__[key] for key in value.window})

        else:

            if not isinstance(value, EnvBase):

                sub_env_dict.update({key: value})

            if value.visibility is True:

                sub_env_dict.update({key: value.intro}) if recursive is False else sub_env_dict.update({key: explore(value)})

    if return_mode == "sub_only":
        pass

    elif return_mode == "default":
        sub_env_dict.update(env.intro)

    if as_json is True:
        import json

        intro_json = json.dumps(sub_env_dict)
        return intro_json

    elif as_list is True:
        return [kv for kv in sub_env_dict.items()]

    else:
        return sub_env_dict


def creat_new_env(from_env: EnvBase = None, *args, **kwargs):

    new_env = EnvBase(*args, **kwargs)

    if from_env is None:
        return new_env

    else:
        setattr(from_env, new_env.name, new_env)


if __name__ == "__main__":

    """
    Recommended three method that to compose a new env:
    """

    building = EnvBase(name='building', visible=True)

    # method 1 (with 'add_env' monkey patching)
    floor_1 = EnvBase(name='floor_1', visible=True)

    building.add_env(floor_1)

    print(explore(building))

    building.del_env('floor_1')

    # method 2 (with 'create_new_env' monkey patching)

    creat_new_env(front_env=building, name='floor_2', visible=True)

    print(explore(building))

    # method 3 (Define an env method in a class)
    class Building(EnvBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.add_env(EnvBase(name='floor_3', visible=True))

    building = Building(name='building', visible=True)
    print(explore(building))
