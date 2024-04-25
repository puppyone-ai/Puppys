from puppy.environment.base import EnvBase


class Action(EnvBase):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.name = ""
        self.code = ""
        self.status = ""
        self.visibility = True

        # Could consider introduce the front-end func_name as indexing in the future
