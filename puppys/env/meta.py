class EnvMeta(type):

    def __new__(cls, name, bases, class_dict):

        # get window property, if it exists
        window = class_dict.get('window', [])

        # if the base class has a window property, add it to the window
        for base in bases:
            if hasattr(base, 'window'):
                window = list(set(window) | set(base.sub_env))

        class_dict['window'] = window

        return super().__new__(cls, name, bases, class_dict)
