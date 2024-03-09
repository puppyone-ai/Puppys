import time
import inspect


def newAgentFunc(func):
    args = inspect.getfullargspec(func).args
    sourceCode=inspect.getsource(func)
    name=func.__name__

    print("name:")
    print(name)

    print("arg:")
    print(args)

    print("sourceCode:")
    print(sourceCode)


def newAgentVar(var):
    args = inspect.getfullargspec(func).args
    sourceCode=inspect.getsource(func)
    name=func.__name__

    print("name:")
    print(name)

    print("arg:")
    print(args)

    print("sourceCode:")
    print(sourceCode)

# This is an example of a function for agents
class agentFuncTemplate:
    def __init__(self, threadInstance, **kwargs):
        self.threadInstance = threadInstance
        self.name = "None"
        self.tag = "func"
        self.description = "nothing"
        self.example = """
        ## doing nothing
        pass
        """

    def __call__(self, **kwargs):
        self.run(**kwargs)

    def run(self, **kwargs):
        pass


# This is an example of a function for agents
class agentVarsTemplate:
    def __init__(self, threadInstance, **kwargs):
        self.threadInstance = threadInstance
        self.name = "None"
        self.tag = "vars"
        self.description = "nothing"
        self.example = """
        ## doing nothing
        pass
        """

    def __call__(self, **kwargs):
        self.run(**kwargs)

    def run(self, **kwargs):
        pass


class numApples:
    def __init__(self):
        self.name = "numApples"
        self.tag = "vars"
        self.description = "the number of apple"
        self.value = 5

    @newAgentFunc
    def takeApple(self):
        ## take one apple from the kitchen
        self.value = 5
        print("I have taken one apple! You mother fxxker!")


'''
class ThreadSpace:
    def __init__(self):
        self.params = {"ok"}

    def __getattr__(self, item):

        return self.params.get(item, None)

    def add_param(self, key, value):
        # 添加参数到params字典中
        self.params[key] = value
'''





if __name__ == "__main__":

    @newAgentFunc
    def wakeMeUp(threadInstance,seconds):
        ## wake me up after seconds
        print(threadInstance.actionFlow)

        ## wake me up after seconds
        time.sleep(seconds)
        print("shut up you mother fucker")