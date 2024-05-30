# from abc import ABC, abstractmethod
from puppy_new.environment.base import EnvBase


class PuppyBase(EnvBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # resolve the warning for dynamic attribute access
    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            print(e)
