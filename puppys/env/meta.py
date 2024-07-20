class EnvMeta(type):

    def __new__(
        cls, 
        name, 
        bases: list, 
        class_dict: dict
    ):
        """
        The metaclass for the Env class.
        """

        # Get window property, if it exists
        window = class_dict.get("window", [])

        # If the base class has a window property, add it to the window
        for base in bases:
            if hasattr(base, "window"):
                window = list(set(window) | set(base.sub_env))

        class_dict["window"] = window

        return super().__new__(cls, name, bases, class_dict)
