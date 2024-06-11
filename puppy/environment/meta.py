class EnvMeta(type):

    def __new__(cls, name, bases, class_dict):

        # 获取 window 属性，如果存在的话
        window = class_dict.get('window', [])

        # 如果父类有 window 属性，合并它们
        for base in bases:
            if hasattr(base, 'window'):
                window = list(set(window) | set(base.sub_env_list))

        class_dict['window'] = window

        return super().__new__(cls, name, bases, class_dict)
