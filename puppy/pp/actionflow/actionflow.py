from puppy.environment.base import EnvBase
from puppy.pp.base import PuppyBase
from puppy.pp.actionflow.action import Action
from puppy.utils.parse import parse_code2list

import queue


# the intermediate env for governing the actionflow in the pp
class Actionflow(EnvBase):
    def __init__(self, puppy_instance: PuppyBase = PuppyBase(), **kwargs):

        """
        {
            "EnvBase": {
                "name": "",
                "description": "",
                "tag": "env",
                "__visibility": False
            }
        }
        """

        super().__init__(name="actionflow",
                         description="an actionflow that governs all actionflow_list in the Puppy",
                         visible=False, **kwargs)

        self.__thread_instance = puppy_instance


        self.all_code = ""
        self.current_code = ""
        self.exception = ""



