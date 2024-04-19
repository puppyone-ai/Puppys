import inspect


class Environment:

    def __init__(self, thread_instance,
                 name: str = "",
                 description: str = '',
                 visibility: bool = False,

                 ):

        # the name of this environment var
        self.name = name

        # description of this environment var
        self.description = description

        # if this var is default visible for .read() or not
        self.visibility = visibility


    def create(self, func) -> None:

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        source_code = inspect.getsource(func)
        func_name = func.__name__


        return





    @property
    def read(self) -> dict:
        return vars(self)


@Environment.create(thread_instance=main_thread)
def function_name(self, para):
    pass


