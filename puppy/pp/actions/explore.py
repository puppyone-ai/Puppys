from puppy.env.env import Env
from typing import Type


def explore(env: Env,
            target: Type[Env] = None,
            sub_only: bool = False,
            as_json: bool = False,
            ):

    """

    Returns:

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

    res = {} if sub_only else env.intro

    sub_env_dict = env.env_dict if not target else {k: v for k, v in env.env_dict.items() if isinstance(v, target)}

    res.update(sub_env_dict)

    if as_json is True:
        import json

        intro_json = json.dumps(res)
        return intro_json

    else:
        return res
