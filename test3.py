def instance_decorator(cls):
    instance = cls("auto-created", 99)  # 假设构造函数需要两个参数
    return instance  # 返回的是实例而不是类


@instance_decorator
class MyClass:

    def __init__(self, name, value):
        self.name = name
        self.value = value


# MyClass 现在是一个实例而不是类
print(MyClass.name)  # 输出: auto-created


