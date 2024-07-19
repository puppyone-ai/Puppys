from typing import Type, Any, Dict
from puppys.env.env import Env


def env_to_dict(
    environment: Env, 
    attributes: list
) -> Dict[str, Any]:
    """
    Convert an Env object to a dictionary that can be JSON serialized.

    Args:
        environment (Env): The environment to convert.
        attributes (list): The list of attributes to include in the output.

    Returns:
        dict: The dictionary representation of the environment.
    """

    res = {}
    for k in attributes:
        res[k] = getattr(environment, k)

    return res


def get_target_env_dict(
    environment: Env, 
    target: Type[Env], 
    attributes: list, 
    mode: str
) -> Dict[str, Any]:
    """
    Get the target environment dictionary.

    Args:
        environment (Env): The environment to explore.
        target (Type[Env]): The target environment type to filter by.
        attributes (list): The list of attributes to include in the output.
        mode (str): The mode for output content ("instance" or "attribute").

    Returns:
        dict: The target environment dictionary.
    """

    target_env_dict = {}
    for k, v in environment.env_dict.items():
        if isinstance(v, target) and v.visible:
            if mode == "instance":
                target_env_dict[k] = v
            elif mode == "attribute":
                target_env_dict[k] = env_to_dict(v, attributes)
    return target_env_dict


def get_self_env_dict(
    environment: Env, 
    attributes: list, 
    mode: str
) -> Dict[str, Any]:
    """
    Get the self environment dictionary. Exception will be raised if the mode is invalid.

    Args:
        environment (Env): The environment to explore.
        attributes (list): The list of attributes to include in the output.
        mode (str): The mode for output content ("instance" or "attribute").

    Returns:
        dict: The self environment dictionary.
    """

    if mode == "instance":
        return environment
    elif mode == "attribute":
        return env_to_dict(environment, attributes)
    else:
        raise ValueError("output_content_mode must be either `instance` or `attribute`.")

def prepare_response(
    self_env_dict: Dict[str, Any],
    target_env_dict: Dict[str, Any],
    with_source_env: bool
) -> Any:
    """
    Return the target environment dictionary or the source environment dictionary.

    Args:
        self_env_dict (Dict[str, Any]): The self environment dictionary.
        target_env_dict (Dict[str, Any]): The target environment dictionary.
        with_source_env (bool): Flag indicating whether to include the source environment.
    """

    if with_source_env:
        return [self_env_dict, target_env_dict]
    return target_env_dict

def convert_to_json(
    res: any, 
    as_json: bool
) -> any:
    """
    Convert the result to JSON format if requested.

    Args:
        res (any): The result to convert.
        as_json (bool): Flag indicating whether to return the result as JSON format.

    Returns:
        any: The result in JSON format if requested.
    """

    if as_json:
        import json
        return json.dumps(res)
    return res


def explore(
    environment: Env,
    target: Type[Env] = None,
    output_content_mode = "instance",
    attributes: list = None,
    with_source_env: bool = False,
    as_json: bool = False
) -> dict:
    """
    A function that explores the environment based on the specified parameters and returns the result.

    Args:
        environment (Env): The environment to explore.
        target (Type[Env], optional): The target environment type to filter by. Defaults to None.
        output_content_mode (str, optional): The mode for output content ("instance" or "attribute"). Defaults to "instance".
        attributes (list, optional): The list of attributes to include in the output. Defaults to None.
        with_source_env (bool, optional): Flag indicating whether to include the source environment. Defaults to False.
        as_json (bool, optional): Flag indicating whether to return the result as JSON format. Defaults to False.


    For example:

    env = Env(value="museum in Paris", name="the maple", description="It's a beautiful place")
    env.Louvre = Env(value="good", name="Louvre", description="It's a beautiful museum")


    Returns(if with_source_env is False, output_content_mode is "instance"):
        {"Louvre": <puppys.env.env.Env object at 0x1078f91d0>}

    Returns(if with_source_env is True, output_content_mode is "instance"):
        [<puppys.env.env.Env object at 0x11ffb0dd0>, {"Louvre": <puppys.env.env.Env object at 0x11ffb11d0>}]

    Returns(if with_source_env is False, output_content_mode is "attribute", attributes is ["value", "name", "description"]):
        {"value": "good", "name": "Louvre", "description": "It's a beautiful museum"}

    Returns(if with_source_env is True, output_content_mode is "attribute", attributes is ["value", "name", "description"]):
        [{"value": "museum in Paris", "name": "the maple", "description": "It"s a beautiful place"}, {"value": "good", "name": "Louvre", "description": "It"s a beautiful museum"}]
    """

    if not target:
        target = Env

    target_env_dict = get_target_env_dict(environment, target, attributes, output_content_mode)
    self_env_dict = get_self_env_dict(environment, attributes, output_content_mode)
    res = prepare_response(self_env_dict, target_env_dict, with_source_env)
    return convert_to_json(res, as_json)


if __name__ == "__main__":
    Museum = Env(
        value="museum in Paris", 
        name="the maple", 
        description="It's a beautiful place"
    )

    Museum.Louvre = Env(
        value="good", 
        name="Louvre", 
        description="It's a beautiful museum"
    )
    Museum.Eiffel = Env(
        value="bad", 
        name="Eiffel", 
        description="It's a ugly tower"
    )

    result = explore(
        Museum, 
        target=Env,
        attributes=["value", "name", "description"], 
        output_content_mode="attribute",
        with_source_env=False
    )

    print(result)
