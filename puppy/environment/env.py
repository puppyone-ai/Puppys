from __future__ import annotations
from typing import Union


class Env:

    """
    Use to build the environment for the puppy to retrival.
    """

    sub_env: list[str]   # Optional collector for sub-env, has higher priority than __dict__.keys()
    as_list: bool
    name: str

    def __new__(cls, *args,
                as_list: bool = False,
                sub_env: list = None,
                name: str = None,
                **kwargs):

        cls.as_list = as_list
        cls.sub_env = sub_env if sub_env else []
        cls.name = name if name else cls.name if hasattr(cls, 'name') else cls.__name__

        return super().__new__(cls)

    def __init__(self, *args, value, description=None, **kwargs):

        self.value = value
        self.description = description

        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def sub_env_add(cls, *args: str):
        cls.sub_env.extend(args)

    @classmethod
    def sub_env_del(cls, *args: str):
        for arg in args:
            if arg in cls.sub_env:
                cls.sub_env.remove(arg)

    @property
    def env_list(self) -> list:

        res = []

        sub_env_keys = self.sub_env if self.sub_env else self.__dict__.keys()

        for k in sub_env_keys:
            if isinstance(self.__dict__[k], Env):
                res.append(self.__dict__[k].intro)
            else:
                res.append(self.__dict__[k])

        return res

    @property
    def env_dict(self) -> dict:

        res = {}

        sub_env_keys = self.sub_env if self.sub_env else self.__dict__.keys()

        for k in sub_env_keys:
            if isinstance(self.__dict__[k], Env):
                res.update({k: self.__dict__[k].intro})
            else:
                res.update({k: self.__dict__[k]})

        return res

    @property
    def env_read(self) -> Union[list, dict]:
        return self.env_list if self.as_list else self.env_dict

    @property
    def intro(self) -> dict:

        return {"name": self.name, "description": self.description}

    def add_env(self, *args: Env):

        for env in args:
            if isinstance(env, Env):
                setattr(self, env.name, env)
                self.sub_env.append(env.name)

            else:
                raise TypeError('add_env() currently could only dynamically load and link instance from EnvBase.')

    def del_env(self, *args: Union[str, Env]):

        for sub_env in args:

            try:

                if type(sub_env) is str:
                    delattr(self, sub_env)
                    self.sub_env.remove(sub_env)

                elif isinstance(sub_env, Env):

                    keys_to_delete = [k for k, v in self.__dict__.items() if v == sub_env]

                    for key in keys_to_delete:
                        delattr(self, key)
                        self.sub_env.remove(key)

                else:
                    raise TypeError()

            except AttributeError:
                continue

    def isolated(self):
        self.sub_env.clear()

    def __str__(self):
        return str(self.intro)


def creat_new_env(from_env: Env = None, *args, **kwargs):

    new_env = Env(*args, **kwargs)

    if from_env is None:
        return new_env

    else:
        setattr(from_env, new_env.name, new_env)


if __name__ == "__main__":

    """
    Recommended three method that to compose a new env:
    """

    building = Env(name='building', visible=True)

    # method 1 (with 'add_env' monkey patching)
    floor_1 = Env(name='floor_1', visible=True)

    building.add_env(floor_1)

    print(building)

    building.del_env('floor_1')

    # method 2 (with 'create_new_env' monkey patching)

    creat_new_env(front_env=building, name='floor_2', visible=True)

    print(building)

    # method 3 (Define an env method in a class)
    class Building(Env):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.add_env(Env(name='floor_3', visible=True))

    building = Building(name='building', visible=True)
    print(building)
