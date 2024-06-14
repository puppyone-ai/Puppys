from .base import EnvBase


def explore(env: EnvBase,
            return_mode: str = "default",
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

    sub_env_collection = env.sub_env_collections

    if return_mode == "window_only":
        pass

    elif return_mode == "default":
        sub_env_collection.update(env.intro)

    if as_json is True:
        import json

        intro_json = json.dumps(sub_env_collection)
        return intro_json

    else:
        return sub_env_collection
