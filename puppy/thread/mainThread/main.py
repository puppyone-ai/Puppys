import inspect
import threading
from .actionFlow import ActionFlow
from .actions import Actions
from .knowledge import Knowledge
#from ...publicFunction.actionDefault import ActionDefault


class MainThread():
    def __init__(self):
        
        self.currentThreadName="mainThread"
        self.actionFlow=ActionFlow(self)
        self.actions=Actions(self)
        self.knowledge=Knowledge(self)

        self.threadProperty={}

        self.agentVarFunc = {}

        self.agentFunc = {}
        self.agentVar = {}


        self.environment = {"self":self}

        self.goal=""



    # to get value from agentVar
    def __getattr__(self, attr):
        if attr in self.agentVar:
            return attr.value

        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


    ## the templete of an func for agents
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


    ## the templete of an func for agents
    class agentVarTemplete:
        def __init__(self, threadInstance, **kwargs):
            self.threadInstance = threadInstance
            self.name = "None"
            self.tag = "var"
            self.description = "nothing"
            self.value = None



    def newAgentFunc(self, func):
        args = inspect.getfullargspec(func).args
        sourceCode=inspect.getsource(func)
        name=func.__name__

        newAgentVar=self.agentVarTemplete()


        print("name:")
        print(name)

        print("arg:")
        print(args)

        print("sourceCode:")
        print(sourceCode)


    def new_agent_var(self, func):
        args = inspect.getfullargspec(func).args
        sourceCode=inspect.getsource(func)
        name=func.__name__

        print("name:")
        print(name)

        print("arg:")
        print(args)

        print("sourceCode:")
        print(sourceCode)


    # to run the thread
    def MainThreadRun(self):

        # start the code thread
        threadCode = threading.Thread(target=self.mainThreadActionFlowRun)
        threadCode.daemon = False
        threadCode.start()
        

        #self.codeThreadActionFlow.actionOnGoing.put(importTools)


        # end the code thread
        threadCode.join()

    # for the wrapper of action
    def mainThread(self, func):
        def wrapper(self, *args, **kwargs):
            self.initialize()
            func(*args, **kwargs)
        
        self.currentThreadName="mainThread"
        sourseCode=inspect.getsource(func)

        # if the function is action, initialize the actionFlow
        funcName=func.__name__
        if funcName == "actionFlowPending":

            # get source code
            self.actionFlow.initialize(sourseCode)

            print("\U0001F3B2 Initialize Done")
            print("Initialized Function: "+funcName)



        if funcName == "trigger":
            # TODO
            pass

        # execute the function with wrapper
        return wrapper


    def createPuppyInstance(self, instanceName):
        new_instance = Puppy(name=instanceName)
        # 将新创建的实例添加到globalVars字典中，使用instance_name作为键

        globals()[instanceName] = new_instance

    def execMode(self, code, mode="thread"):
        exec(code, self.environment)

    def mainThreadActionFlowRun(self):

        # import tools, for agents


        # loading actions
        from ...publicFunction.actionDefault import ActionDefault

        self.actionDefault = ActionDefault(self)
        self.sendMessageToHuman = self.actionDefault.sendMessageToHuman


        self.actionFlow.actionFlowCurrentClear()


        #print(self.Vars)

        print("\U0001F4E5 Import Done")
        # start the action flow

        while self.actionFlow.actionFlowCurrentJSON ==[] and self.actionFlow.actionFlowPendingJSON !=[]:

            print("\U0001F525 Action Start")

            # STEP 1: load the action from actionFlowPending to actionFlowCurrent
            self.actionFlow.actionCurrentLoad()

            # STEP 2: delete the action from actionFlowPending
            self.actionFlow.actionFlowPendingRemoveFront()

            print("\U0001F51C ActionFlowPending:")
            print(self.actionFlow.actionFlowPendingJSON)
            print("\U000025B6 ActionFlowCurrentJSON:")
            print(self.actionFlow.actionFlowCurrentJSON)
            print("\U0001F519 ActionFlowHistory:")
            print(self.actionFlow.actionFlowHistoryJSON)

            while self.actionFlow.actionFlowCurrentJSON !=[]:
                
                # STEP 3.1: check if the action is fixed, semi-fixed, or changeable
                if self.actionFlow.actionFlowCurrentGetFront()["status"]=="fixed":
                    pass

                elif self.actionFlow.actionFlowCurrentGetFront()["status"]=="semi-fixed":
                    self.actions.do()

                elif self.actionFlow.actionFlowCurrentGetFront()["status"]=="changeable":
                    pass
                
                # STEP 3.2 load the action from actionCurrent to actionOnGoing
                if self.actionFlow.actionFlowCurrentJSON !=[]:
                    self.actionFlow.actionCurrentExecute()
                    
                
                    # STEP 3.3: load the action from actionOngoing and execute the code, and determine if the action is hidden
                    action = self.actionFlow.actionOnGoing.get()

                    print("\n")
                    print("\U0001F697 Running Code ################################################################")
                    print(action)
                    print("################################################################################")
                    


                    exec(action, self.environment)
                    self.actionFlow.actionOnGoing.task_done()

                    # STEP 4: load the action from the actionFlowCurrent to the actionFlowHistory
                    self.actionFlow.actionCurrentSave()


                    # STEP 5: remove the action from the actionFlowCurrent
                    if self.actionFlow.actionFlowCurrentJSON !=[]:
                        self.actionFlow.actionFlowCurrentRemoveFront()
                    
                    else:
                        pass

                else: 
                    pass

        print("Done")


class Puppy(MainThread):
    def __init__(self, name="puppy"):
        
        super().__init__()
        self.puppyName=name

    def run(self):
        self.MainThreadRun()




