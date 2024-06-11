from .base import EnvBase


def explore(env: EnvBase,
            return_mode: str = "default",
            as_json: bool = False, as_list: bool = False,
            recursive: bool = False
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

    sub_envs = env.env_list if env.sub_env_list else {}

    if return_mode == "window_only":
        pass

    elif return_mode == "default":
        sub_envs.update(env.intro)

    elif return_mode == "full":
        sub_envs.update({k: v.intro for k, v in env.__dict__.items()})

    if as_json is True:
        import json

        intro_json = json.dumps(sub_envs)
        return intro_json

    elif as_list is True:
        return [kv for kv in sub_envs.items()]

    else:
        return sub_envs
