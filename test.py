import ast
import re
from puppy.pp.actions.load_env import load_env, unload_env
from puppy.env.env import Env


def func(self):
    pass


from puppy.pp.main import Puppy

puppy_test = Puppy(name="Puppy", value=func)

puppy_test.map = Env(value="museum in Paris", name="the maple", description="It's a beautiful place")
puppy_test.map.Louvre_instance = Env(value="good", name="Louvre", description="It's a beautiful museum")

load_env(puppy_instance=puppy_test)
print(puppy_test.runtime_vars_dict)  # return the list with instance of 'the maple'

load_env(puppy_instance=puppy_test, env_node=puppy_test.map)
print(puppy_test.runtime_vars_dict)  # return the list with instance of 'Louvre'

unload_env(puppy_instance=puppy_test, env_node=puppy_test.map)
print(puppy_test.runtime_vars_dict)  # return the list with instance of 'the maple'

unload_env(puppy_instance=puppy_test)
print(puppy_test.runtime_vars_dict)  # return the list with instance of 'Puppy'