from __future__ import annotations
from typing import Union


class Env:
    """
    Use to build the environments for the puppys to retrival.

    Init Args:
        value (any, optional): The value of the environment. Defaults to None.
        name (str, optional): The name of the environment. Defaults to None.
        description (str, optional): The description of the environment. Defaults to None.
        sub_env (list, optional): The sub environment of the environment. Defaults to None.
    """

    visible: bool = True
    as_list: bool
    private_keys: list = ["value", "name", "description"]

    def __init__(
        self, 
        value: any = None, 
        *args, 
        name: str = None, 
        description: str = None, 
        sub_env: list = None, 
        **kwargs
    ):
        self.value = value
        self.name = name
        self.description = description

        if sub_env:
            for env in sub_env:
                if not isinstance(env, Env):
                    raise TypeError("sub_env must be a list of Env instance.")

                setattr(self, env.name, env)

    @property
    def env_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k not in self.private_keys}

    @property
    def env_list(self) -> list:
        return [v for v in self.env_dict.values()]

    @property
    def env_read(self) -> str:
        return str(self.env_list) if self.as_list else str(self.env_dict)

    @property
    def intro(self) -> dict:
        return {"name": self.name, "description": self.description}

    def add(self, *args: Env) -> None:
        """
        Add the environment instance to the current environment instance.

        Args:
            *args (Env): The environment instance to add.
        """

        for env in args:
            if isinstance(env, Env):
                setattr(self, env.name, env)
            else:
                raise TypeError("Method: add() currently could only dynamically load Env instances.")

    def remove(self, *args: Union[str, Env]) -> None:
        """
        Remove the environment instance from the current environment instance.

        Args:
            *args (Union[str, Env]): The key or the obj to remove.
        """

        for env in args:
            try:
                if type(env) is str:
                    delattr(self, env)
                elif isinstance(env, Env):
                    keys_to_delete = [k for k, v in self.__dict__.items() if v == env]
                    for key in keys_to_delete:
                        delattr(self, key)
                else:
                    raise TypeError("remove() could only be delivered the key or the obj.")

            except AttributeError:
                continue

    def isolated(self):
        """
        Isolate the environment instance.
        """

        self.__dict__.clear()


def create(*args, **kwargs):
    new_env = Env(*args, **kwargs)

    return new_env


if __name__ == "__main__":
    """
    Recommended three method that to compose a new environment:
    """

    #####################
    # Method 1

    museum = Env(
        "https://www.mbam.qc.ca/en/", 
        name="Montreal Museum of Fine Arts"
    )
    print(museum)

    painting = Env(
        "https://www.mbam.qc.ca/en/works/4577/", 
        name="October", 
        description="by James Tissot"
    )
    print(painting)

    museum.add(painting)
    print(museum)

    # museum.remove("October")
    museum.remove(painting)
    print(museum)

    ####################
    # Method 2

    museum.October = create(
        "https://www.mbam.qc.ca/en/works/4577/", 
        name="October", 
        description="by James Tissot"
    )

    print(museum)


    ####################
    # Method 3 (Define an environment as a class)
    class Museum(Env):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.add(Env(
                "https://www.mbam.qc.ca/en/works/4577/", 
                name="October", 
                description="by James Tissot"
            ))


    museum = Museum(
        value="https://www.mbam.qc.ca/en/",
        name="Montreal Museum of Fine Arts"
    )

    print(museum.env_dict)
