# file2.py

class Puppy:
    def __init__(self, name):
        self.name = name

def exec_with_globals(globals_dict):
    # 在这里执行需要的操作，使用globals_dict
    exec("print('This is exec_with_globals function.')", globals_dict)
