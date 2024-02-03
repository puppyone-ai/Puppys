class MyClass:
    def __init__(self):
        self.variable = "initial value"
        self.globalVars = {'self': self, }

    def exec_cmd(self, cmd):
        exec(cmd, self.globalVars)

        

# 创建对象
my_object = MyClass()

# 准备代码
code = """
self.variable = "new value"
"""

my_object.exec_cmd(code)
print(my_object.variable)  # new value