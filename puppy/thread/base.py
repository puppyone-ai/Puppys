# from abc import ABC, abstractmethod
from puppy.environment.base import EnvBase


class ThreadBase(EnvBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
