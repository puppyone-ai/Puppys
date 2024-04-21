

class BaseEnv:

    def __init__(self,
                 name: str = "",
                 description: str = '',
                 visibility: bool = False,
                 **kwargs

                 ):
        # the name of this environment var
        self.name = name

        # description of this environment var
        self.description = description

        # sort the env vars
        self.tag = []

        # if this var is default visible for .expose() or not
        self.visibility = visibility

        # the overview of the env var
        self.overview = {
            "name": self.name,
            "tag": "class",
            "description": self.description}

    # show the env inside
    def expose(self):
        vars_dict = vars(self)
        view_dict = {}

        for var in vars_dict:
            # get the value of the var, if it doesn't exist, return True
            if getattr(vars_dict[var], 'visibility', False) == False:
                pass

            elif getattr(vars_dict[var], 'visibility', False) == True:
                view_dict.update({var: vars_dict[var].overview})

        return view_dict

    def create_env(self, **kwargs):
        return BaseEnv(**kwargs)


if __name__ == "__main__":
    Building = BaseEnv()
    Building.floor_1=Building.create_env(visibility =  True)

    print(Building.expose())
