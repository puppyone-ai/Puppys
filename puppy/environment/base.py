from __future__ import annotations
from typing import Union
from meta import EnvMeta


class EnvBase(metaclass=EnvMeta):

    sub_env_list: list = []

    def __init__(self,
                 value: any,
                 name: str = None,
                 description: str = None,
                 *args, **kwargs):

        self.value = value  # value

        self.name = name  # key
        self.description = description  # context

        for key, value in kwargs.items():
            if not isinstance(value, EnvBase):
                raise TypeError('EnvBase could only accept EnvBase instance as key word arguments.')
            setattr(self, key, value)

    @classmethod
    def sub_env_add(cls, *args: str):
        cls.sub_env_list.extend(args)

    @classmethod
    def sub_env_del(cls, *args: str):
        for arg in args:
            if arg in cls.sub_env_list:
                cls.sub_env_list.remove(arg)

    @property
    def env_list(self) -> list:

        result = []

        for k in self.sub_env_list:
            if not isinstance(self.__dict__[k], EnvBase):
                result.append(self.__dict__[k])
            else:
                result.append(self.__dict__[k].intro)

        return result

    @property
    def intro(self) -> dict:

        return {"name": self.name, "description": self.description}

    def add_env(self, *args: EnvBase):

        for sub_env in args:
            if isinstance(sub_env, EnvBase):
                setattr(self, sub_env.name, sub_env)
                self.sub_env_list.append(sub_env.name)

            else:
                raise TypeError('add_env() currently could only dynamically load and link instance from EnvBase.')

    def del_env(self, *args: Union[str, EnvBase]):

        for sub_env in args:

            try:

                if type(sub_env) is str:
                    delattr(self, sub_env)
                    self.sub_env_list.remove(sub_env)

                elif isinstance(sub_env, EnvBase):

                    keys_to_delete = [k for k, v in self.__dict__.items() if v == sub_env]

                    for key in keys_to_delete:
                        delattr(self, key)
                        self.sub_env_list.remove(key)

                else:
                    raise TypeError()

            except AttributeError:
                continue

    def isolated(self):
        self.sub_env_list.clear()

    def __str__(self):
        return self.intro


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

    print(building)

    building.del_env('floor_1')

    # method 2 (with 'create_new_env' monkey patching)

    creat_new_env(front_env=building, name='floor_2', visible=True)

    print(building)

    # method 3 (Define an env method in a class)
    class Building(EnvBase):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.add_env(EnvBase(name='floor_3', visible=True))

    building = Building(name='building', visible=True)
    print(building)
