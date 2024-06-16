from puppy.environment.env import Env


def explore(env: Env,
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

    res.update(env.env_dict)

    if as_json is True:
        import json

        intro_json = json.dumps(res)
        return intro_json

    else:
        return res
