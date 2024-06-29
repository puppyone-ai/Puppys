import inspect
from puppy.env.env import Env
from puppy.utils.parse import parse_code2str

# a default essential env for agent
class Actionflow(Env):
    visible = False

    def __init__(self, puppy_instance, *args, function, **kwargs):
        super().__init__(*args, **kwargs)

        self.puppy_instance = puppy_instance
        self.function = function

        # get the full source code
        self.source_code = inspect.getsource(self.function)

        # get the function signature
        signature = inspect.signature(self.function)

        # or use  get full args pec to get more specific information
        args_spec = inspect.getfullargspec(self.function)

        self.all_code = parse_code2str(self.source_code)

        self.current_code = ""


    def run(self):
        return self.function(self.puppy_instance)
