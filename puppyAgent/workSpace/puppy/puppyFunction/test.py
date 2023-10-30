import inspect

# 新的函数，将在每个 #TODO 后被调用
def newFunction():
    print("New function is executed!")

# 装饰器，用于修改 Test 函数的源代码
def inject_new_function(originalTest):
    def wrapper(*args, **kwargs):
        # 获取原始 Test 函数的源代码
        source = inspect.getsource(originalTest)
        source_lines = source.split('\n')[1:]  # 移除装饰器行

        # 修改源代码，在每个 #TODO 后插入 newFunction 的调用
        modified_lines = []
        for line in source_lines:
            modified_lines.append(line)
            if '#TODO' in line:
                # 计算当前行的缩进
                indent = len(line) - len(line.lstrip())
                # 插入 newFunction 的调用，并保持相同的缩进
                modified_lines.append(' ' * indent + 'newFunction()')

        # 动态创建新的 Test 函数
        modified_source = '\n'.join(modified_lines)
        print(modified_source)
        exec_globals = {}
        exec(modified_source, globals(), exec_globals)
        modifiedTest = exec_globals['Test']

        # 调用修改后的 Test 函数
        return modifiedTest(*args, **kwargs)

    return wrapper


# 创建一个类，其方法 Test 是我们要修改的目标函数
class MyClass:
    def Test(self):
        def ReAct(task="provide the answer to the input question"):
            #TODO search for the quesiton @google search @zhihu search
            completeThis()

            #TODO search for the question @google search @zhihu search

            #DONE: for agent to design the action
            print("Inside ReAct function.")

            #TODO
            completeThis()

            pass

        # 调用内部函数 ReAct
        ReAct()


import threading
import queue

def worker(task_queue):
    while True:
        task = task_queue.get()
        if task is None:
            break
        try:
            exec(task)
        except Exception as e:
            print(f"Error executing task: {e}")
        task_queue.task_done()

task_queue = queue.Queue()
t = threading.Thread(target=worker, args=(task_queue,))
t.start()

# 添加多个任务到队列，其中一个任务会引发错误
tasks = [
    "aaa=1",
    "print(aaa)",
    "1 / 0",  # 这将引发一个 ZeroDivisionError
    "print('Task 4 executed!')"
]

for task in tasks:
    task_queue.put(task)

# 结束工作线程
task_queue.put(None)
t.join()


lst = ["a", "b", "c", "d"]
result = ''.join(lst)  # join the list elements with no delimiter
print(result)


