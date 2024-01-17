class MyClass:
    def __init__(self):
        self.value = 5
        self.functions_list = [self.method1, external_function_with_self]
        self.functions_list.append(external_function_without_self)

    def method1(self):
        print(f"Method 1 is called from inside the class, value is {self.value}")

    def run_functions(self):
        for func in self.functions_list:
            if "self" in func.__code__.co_varnames:
                func(self)
            else:
                func()

def external_function_with_self(self):
    print(f"External function with self, value is {self.value}")

def external_function_without_self():
    print("External function without self")

# 创建 MyClass 的实例
my_instance = MyClass()

# 运行所有函数
my_instance.run_functions()
