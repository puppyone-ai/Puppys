from typing import Type, Any, Dict
from puppys.env.env import Env


def env_to_dict(environment: Env, attributes: list) -> Dict[str, Any]:
    """
    Convert an Env object to a dictionary that can be JSON serialized.
    """
    res = {}
    for k in attributes:
        res[k] = getattr(environment, k)

    return res


def explore(environment: Env,
            target: Type[Env] = None,
            output_content_mode="instance",
            attributes: list = None,
            with_source_env: bool = False,
            as_json: bool = False
            ):
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
        {'Louvre': <puppys.env.env.Env object at 0x1078f91d0>}

    Returns(if with_source_env is True, output_content_mode is "instance"):
        [<puppys.env.env.Env object at 0x11ffb0dd0>, {'Louvre': <puppys.env.env.Env object at 0x11ffb11d0>}]

    Returns(if with_source_env is False, output_content_mode is "attribute", attributes is ["value", "name", "description"]):
        {'value': 'good', 'name': 'Louvre', 'description': "It's a beautiful museum"}

    Returns(if with_source_env is True, output_content_mode is "attribute", attributes is ["value", "name", "description"]):
        [{'value': 'museum in Paris', 'name': 'the maple', 'description': "It's a beautiful place"}, {'value': 'good', 'name': 'Louvre', 'description': "It's a beautiful museum"}]
    """

    if target is None:
        target = Env

    # output content mode
    if output_content_mode == "instance":
        target_env_dict = {}
        for k, v in environment.env_dict.items():

            if isinstance(v, target) and v.visible is True:
                target_env_dict[k] = v

        self_env_dict = environment

    elif output_content_mode == "attribute":

        target_env_dict = {}
        for k, v in environment.env_dict.items():

            if isinstance(v, target) and v.visible is True:
                target_env_dict[k] = env_to_dict(v, attributes)

        self_env_dict = env_to_dict(environment, attributes)

    else:
        raise ValueError("output_content_mode must be either 'instance' or 'dict'.")

    # with the source env or not
    if with_source_env is False:
        res = target_env_dict

    else:
        res = [self_env_dict, target_env_dict]

    # Convert to JSON if requested
    if as_json:
        import json
        return json.dumps(res)
    else:
        return res


if __name__ == "__main__":
    Museum = Env(value="museum in Paris", name="the maple", description="It's a beautiful place")

    Museum.Louvre = Env(value="good", name="Louvre", description="It's a beautiful museum")
    Museum.Eiffel = Env(value="bad", name="Eiffel", description="It's a ugly tower")

    result=explore(Museum, target=Env,
                  attributes=["value", "name", "description"], output_content_mode="attribute",
                  with_source_env=False)

    print(result)
