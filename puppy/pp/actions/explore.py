from typing import Type, Any, Dict
from puppy.env.env import Env


def env_to_dict(environment: Env) -> Dict[str, Any]:
    """
    Convert an Env object to a dictionary that can be JSON serialized.
    """
    return {
        "value": environment.value,
        "name": environment.name,
        "description": environment.description
    }


def explore(environment: Env,
            target: Type[Env] = None,
            sub_only: bool = False,
            as_json: bool = False
            ):
    """
    Explore the environment and sub_environments, optionally filtering by type and formatting as JSON.

    Args:
        environment: The main environment instance.
        target: A subclass of Env to filter the sub_environments.
        sub_only: If True, only sub_environments are included in the output.
        as_json: If True, output will be JSON formatted.

    Returns:
        A dictionary or JSON string of the environment details:
    {
    name:*,
    intro:*,
    sub_evn_a:{
               name:**,
               intro:**,
               },
    sub_evn_b:{
               name:***,
               intro:***,
               },
    }
    """

    # Initialize the result dictionary
    res = {} if sub_only else {'name': environment.name, 'intro': environment.description}

    # Filter sub_environments if a target type is specified, else include all
    sub_env_dict = {k: env_to_dict(v) for k, v in environment.env_dict.items() if not target or isinstance(v, target)}

    # Update the result with sub_environments
    res.update({'sub_environments': sub_env_dict})

    # Convert to JSON if requested
    if as_json:
        import json
        return json.dumps(res)
    else:
        return res


if __name__ == "__main__":

    env = Env(value="museum in Paris", name="the maple", description="It's a beautiful place")

    env.Louvre = Env(value="Louvre Museum", name="Louvre", description="It's a beautiful museum")
    print(explore(env))
