import inspect

def newFunction():
    print("New function is executed!")

def proxyTest(originalTest):
    def wrapper(*args, **kwargs):
        # 获取原始 Test 函数的源代码
        source = inspect.getsource(originalTest)
        source_lines = source.split('\n')

        # 修改源代码，插入 newFunction 的调用
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
        exec_globals = {}
        exec(modified_source, globals(), exec_globals)
        modifiedTest = exec_globals['Test']

        # 调用修改后的 Test 函数
        return modifiedTest(*args, **kwargs)

    return wrapper

# 定义原始 Test 函数
def Test():
    def ReAct( task="provide the answer to the input question"):
        #TODO search for the quesiton @google search @zhihu search

        #TODO search for the question @google search @zhihu search

        #DONE: for agent to design the action
        searchResult = ""
        while answerQuestion(question, searchResult) == False:
            information = Rethink(searchResult)
            searchResult = GoogleSearch(information)
        puppyDecision()
        return searchResult

        #TODO whatever you want to do
        pass

# 创建代理 Test 函数
proxyTest = proxyTest(Test)
property(Test())
