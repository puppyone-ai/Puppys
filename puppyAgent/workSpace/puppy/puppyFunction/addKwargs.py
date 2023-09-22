from types import MethodType

class PuppyKwargs():
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # 如果值是函数或方法，为它绑定当前实例
            if callable(value):
                setattr(self, key, value.__get__(self))
            # 否则，直接设置为属性值
            else:
                setattr(self, key, value)


    # add a new customized function to the class
    def addFunction(self, func):
        setattr(self, func.__name__, MethodType(func, self))

    # update a customized function to the class, same as addFunction
    def updateFunction(self, func):
        self.addFunction(func)

    # add a new customized property to the class
    def addProperty(self, attr_name, value):
        setattr(self, attr_name, value)

    # update a customized property to the class, same as addProperty
    def updateProperty(self, attr_name, value):
        self.addProperty(attr_name, value)

#for workflow: task@puppy
#for puppy: action@tool
# user can design task, such as "def ReAct(self):", and use it by simply call "ReAct()"


if __name__ == "__main__":
    def external_function(self):
        print(self.value)

    def external_function2(self):
        print("Hello from external function 2!")

    # 创建类的实例
    obj = PuppyKwargs(value=5)
    obj.addFunction(external_function)

    obj.external_function()

    obj.addFunction(external_function2)
    obj.external_function2()


