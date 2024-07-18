from typing import Type
from puppys.env.env import Env
from puppys.pp.actions.explore import explore


def load_env(
    puppy_instance: any, 
    env_node: Env = None, 
    target: Type[Env] = None
):
    """
    Load the sub_env into the puppy's runtime_vars_dict
    """

    # If the env_node is None, use the current environment
    if env_node is None:
        env_node = puppy_instance.env_node

    if target is None:
        target = Env

    # Create the dict that contains the sub_env in one env
    sub_env_dict = explore(environment=env_node, target=target)

    # Create the dict that contains the name and value in one env
    name_instance_dict = {}
    for _, value in sub_env_dict.items():
        name_instance_dict.update({value.name: value})

    # Update the vars as a dict into puppys's runtime_vars_dict
    puppy_instance.puppy_vars.runtime_dict.update(name_instance_dict.items())


def unload_env(
    puppy_instance: any, 
    env_node: Env = None, 
    target: Type[Env] = None
):
    """
    Unload the sub_env from the puppy's runtime_vars_dict
    """

    # If the env_node is None, use the current environment
    if env_node is None:
        env_node = puppy_instance

    if target is None:
        target = Env

    # Create the dict that contains the sub_env in one env
    sub_env_dict = explore(environment=env_node, target=target)

    # Create the dict that contains the name and value in one env
    name_instance_dict = {}
    for key, value in sub_env_dict.items():
        name_instance_dict.update({value.name: value})

    # Delete the vars in the puppys's runtime_vars_dict
    for key in name_instance_dict.keys():
        del puppy_instance.puppy_vars.runtime_dict[key]
