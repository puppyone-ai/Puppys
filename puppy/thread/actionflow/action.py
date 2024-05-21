from puppy.environment.base import EnvBase


class Action(EnvBase):
    def __init__(self, *args, **kwargs):

        """
        {
            "EnvBase": {
                "name": "",
                "intro": "",
                "tag": "env",
                "__visibility": False
            }
        }
        """

        super().__init__(*args, **kwargs)

        self.name = ""
        self.tag = "action"

        self.code = ""
        self.status = ""
        self.visible = True

        # Could consider introduce the front-end func_name as indexing in the future


if __name__ == "__main__":

    revolver = EnvBase(name='revolver', visible=True)

    action = Action(name='trigger', code='print("Bang!")', visible=True)

    revolver.add_env(action)

    print(revolver.expose())
