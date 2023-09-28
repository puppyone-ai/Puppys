import inspect
import re

class Action():
    def __init__(self):
        self.actionFlow = []
        self.functions = []

    # add a new customized function to the class
    def run(self):
        for func in self.functions:
            func()
    
    # translate the code to action flow in JSON format
    def action(self, func):
        def wrapper(*args, **kwargs):
            source_code = inspect.getsource(func)
            lines = source_code.split('\n')
            is_comment = False
            comment = ""
            for line in lines:
                if is_comment:
                    is_comment = False
                    if '.toDo()' in line:
                        self.actionFlow.append({"action":comment,"executor":"puppy"})
                    else:
                        self.actionFlow.append({"action":comment,"executor":"human"})
                elif '##' in line:
                    comment = line.split('##', 1)[1].strip()
                    is_comment = True
            print(self.actionFlow)
            return func(*args, **kwargs)
        self.functions.append(wrapper)
        return wrapper
    
    # let puppy to run what was planned to be responsibled for puppy
    def toDo(self):

        if self.actionFlow[0]["executor"] == "puppy":
            print("action for puppy:",self.actionFlow[0]["action"])
            self.actionFlow.pop(0)
        elif self.actionFlow[0]["executor"] == "human":
            print("action for human:",self.actionFlow[0]["action"])
            self.actionFlow.pop(0)
            self.toDo()
        else:
            print("error")
            self.actionFlow.pop(0)
            self.toDo()

puppy1 = Action()

@puppy1.action
def ReAct(task="provide the answer to the input question"):   
    ## search for the quesiton @google search @zhihu search
    puppy1.toDo()

    ## rethink about the answer @rethinker
    puppy1.toDo()

    ## 塔克斯的狗粮
    print("now i am here")


    ## do whatever you want to do 
    puppy1.toDo()

    print("end")


puppy1.run()
