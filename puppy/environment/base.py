class BaseEnv:

    def __init__(self,
                 name: str = "",
                 intro: str = '',
                 detail: str = '',
                 visibility: bool = False,
                 **kwargs

                 ):
        # the name of this environment var
        self.name = name

        # description of this environment var
        self.intro = intro

        # the overview of the env var
        self.detail = {
            "name": self.name,
            "tag": "env",
            "intro": self.intro}

        # sort the env vars
        self.tag = []

        # if this var is default visible for .expose() or not
        self.visibility = visibility


    # show the env inside
    def expose(self):
        vars_dict = vars(self)
        view_dict = {}

        for var in vars_dict:
            # get the value of the var, if it doesn't exist, return True
            if getattr(vars_dict[var], 'visibility', False) == False:
                pass

            elif getattr(vars_dict[var], 'visibility', False) == True:
                view_dict.update({var: vars_dict[var].detail})

        return view_dict

    def new_env(self, **kwargs):
        return BaseEnv(**kwargs)


if __name__ == "__main__":
    Building = BaseEnv()
    Building.floor_1=Building.new_env(visibility =  True)

    print(Building.expose())

