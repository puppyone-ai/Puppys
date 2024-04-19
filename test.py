from abc import ABC, abstractmethod


class EnvBase:

    def __init__(self,
                 name: str = "",
                 description: str = '',
                 visibility: bool = False,

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

    def new_env(self, cls):

        name = cls.__name__
        instance = cls()
        setattr(self, name, instance)  # Create instance and set it as an attribute


if __name__ == "__main__":
    Thread = EnvBase()

    print(Thread.name)
    Thread._take = EnvBase(visibility=True)


    @Thread.new_env
    class CCC:
        def __init__(self):
            print("CCC")
            self.visibility = True
            self.overview = {
                "the only one element": "Ture"
            }


    print(Thread.CCC)
    print(Thread.expose())
