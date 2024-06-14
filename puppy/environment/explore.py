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

    sub_env_dict = env.env_list if env.sub_env else {}

    if return_mode == "window_only":
        pass

    elif return_mode == "default":
        sub_env_dict.update(env.intro)

    elif return_mode == "full":
        sub_env_dict.update({k: v.intro for k, v in env.__dict__.items()})

    if as_json is True:
        import json

        intro_json = json.dumps(sub_env_dict)
        return intro_json

    elif as_list is True:
        return [kv for kv in sub_env_dict.items()]

    else:
        return sub_env_dict
