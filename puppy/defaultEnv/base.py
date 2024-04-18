from abc import ABC, abstractmethod


class EnvBase(ABC):

    def __init__(self):
        self._name = name

    @property
    @abstractmethod
    def name(self):
        return self._name