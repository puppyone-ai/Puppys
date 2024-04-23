

def new_env(*args, **kwargs):
    return EnvBase(*args, **kwargs)


class EnvBase:

    def __init__(self,
                 name: str = "",
                 intro: str = '',
                 # detail: str = '',
                 visibility: bool = False,
                 parent=None,
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

        # the parental instance that this env var connected from
        if parent:
            self.parent = parent
            setattr(parent, name, self)

        else:
            raise ValueError("The parent of this env var is not defined")

    # show the env inside
    def expose(self):
        vars_dict = vars(self)
        view_dict = {}

        for var in vars_dict:
            # get the value of the var, if it doesn't exist, return True
            if getattr(vars_dict[var], 'visibility', False) is False:
                pass

            elif getattr(vars_dict[var], 'visibility', False) is True:
                view_dict.update({var: vars_dict[var].detail})

        return view_dict

    # use to create a sub env var under this env node
    def create_new_env(self, *args, **kwargs):

        instance = EnvBase(*args, **kwargs, parent=self)
        setattr(self, kwargs['name'], instance)

    # introduce the __getattribute__ method of super() to rewrite the __dict__ of current instance
    # to avoid the unresolved reference warning for dynamic attributes created
    def __getattribute__(self, item):
        try:
            return super().__getattribute__(item)
        except AttributeError as e:
            print(f"Error: {e}")
            return None


if __name__ == "__main__":
    Building = EnvBase()

    # Building.floor_1 = new_env(visibility=True, parent=Building, name='floor_1', intro='The first floor of the building')

    Building.create_new_env(name='floor_1', visibility=True)

    Building.floor_1.create_new_env(name='floor_2', visibility=True)

    Building.floor_1.create_new_env(name='room_1', visibility=True)
    Building.floor_1.create_new_env(name='room_2', visibility=True)

    floor_2 = new_env(name='floor_2', visibility=True, parent=Building.floor_1)
    floor_3 = new_env(name='floor_3', visibility=True, parent=floor_2)
    # floor_3 = new_env(name='floor_3', visibility=True, parent=Building.floor_1.floor_2)

    # print(Building.floor_1.name)
    #
    # print(Building.expose())
    # print(Building.floor_1.expose())
    # print(Building.floor_1.floor_2.expose())
    print(floor_3.parent.parent.room_1.expose())
