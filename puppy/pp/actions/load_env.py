
from puppy.env.env import Env
from puppy.pp.actions.explore import explore
from typing import Type, Any, Dict

# load the sub_env into the puppy's runtime_vars_dict
def load_env(puppy_instance, env_node : Env = None, target: Type[Env] = None):

    # if the env_node is None, use the current environment
    if env_node is None:
        env_node = puppy_instance

    if target is None:
        target = Env


    tools_dict = explore(environment=env_node, target=target)


    name_instance_dict = {}
    for key, value in tools_dict.items():
        name_instance_dict.update({value.name: value})

    puppy_instance.runtime_vars_dict.update(name_instance_dict.items())

    dict = explore(environment=env_node, with_source_env=True, target=target)


"""
if __name__ == "__main__":
    puppy_test=Puppy(name="Puppy")

    puppy_test.map=Env(value="museum in Paris", name="the maple", description="It's a beautiful place")
    puppy_test.map.Louvre_instance=Env(value="good", name="Louvre", description="It's a beautiful museum")


    load_env(puppy_instance=puppy_test)
    print(puppy_test.runtime_vars_dict) # return the list with instance of 'the maple'

    load_env(puppy_instance=puppy_test, env_node = puppy_test.map)
    print(puppy_test.runtime_vars_dict) # return the list with instance of 'Louvre'
"""

