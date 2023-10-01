import inspect
import re
import copy

class Action():
    def __init__(self):
        self.actionFlow = []
        self.functions = []
        self.currentStep = 0
        self.task=None

    # add a new customized function to the class
    def run(self):
        for func in self.functions:
            func()
    
    # translate the code to action flow in JSON format
    def action(self, func):
        def wrapper(*args, **kwargs):
            sourceCode = inspect.getsource(func)
            lines = sourceCode.split('\n')
            is_comment = False
            comment = ""
            for line in lines:
                if is_comment:
                    is_comment = False
                    if '.act()' in line:
                        self.actionFlow.append({"action":comment,"status":"changable"})
                    else:
                        self.actionFlow.append({"action":comment,"status":"fixed"})
                elif '##' in line:
                    comment = line.split('##', 1)[1].strip()
                    is_comment = True
            print(self.actionFlow)
            self.task= inspect.signature(func).parameters["task"]

            # run the function defined by user
            self.currentStep = 0
            return func(*args, **kwargs)
            
        self.functions.append(wrapper)
        return wrapper
    
    # let puppy to run what was planned to be responsibled for puppy
    def act(self):
        if self.actionFlow[self.currentStep]["status"] == "changable":
            print("action for puppy:",self.actionFlow[self.currentStep]["action"])
        elif self.actionFlow[self.currentStep]["status"] == "fixed":
            print("action for human:",self.actionFlow[self.currentStep]["action"])
        else:
            print("error")
        self.currentStep += 1

    # filling out all the actions in the action flow
    def taskToAction(self):
        print(self.actionFlow)
        print(self.task)
        print(self.currentStep)

    def actionToTools(self):
        print(self.actionFlow(self.currentStep))


puppy1 = Action()

@puppy1.action
def ReAct(task="provide the answer to the input question"):   
    ## search for the quesiton @google search @zhihu search
    puppy1.act()

    ## rethink about the answer @rethinker
    puppy1.act()

    ## clarify I am still running
    print("now i am here")

    ## do whatever you want to do 
    puppy1.act()

    print("end")


puppy1.run()