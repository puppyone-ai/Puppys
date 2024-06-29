
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


    sub_env_dict = explore(environment=env_node, target=target)


    name_instance_dict = {}
    for key, value in sub_env_dict.items():
        name_instance_dict.update({value.name: value})

    puppy_instance.runtime_vars_dict.update(name_instance_dict.items())



def unload_env(puppy_instance, env_node : Env = None, target: Type[Env] = None):

    # if the env_node is None, use the current environment
    if env_node is None:
        env_node = puppy_instance

    if target is None:
        target = Env


    sub_env_dict = explore(environment=env_node, target=target)

    name_instance_dict = {}
    for key, value in sub_env_dict.items():
        name_instance_dict.update({value.name: value})

    for key in name_instance_dict.keys():
        del puppy_instance.runtime_vars_dict[key]












