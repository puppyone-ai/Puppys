import inspect
import threading
from .actionFlow import ActionFlow
from .actions import Actions
from .knowledge import Knowledge
#from ...publicFunction.actionDefault import ActionDefault


class CodeThread():
    def __init__(self):
        
        self.currentThreadName="codeThread"
        self.actionFlow=ActionFlow(self)
        self.actions=Actions(self)
        self.knowledge=Knowledge(self)

        self.threadProperty={}
        self.environment={
        }


        self.vars_ForDev = {}
        self.funcs_forDev ={}

        self.vars_Shared = {}
        self.funcs_Shared = {}

        self.varsFuncs_Temp = {"self":self}

        self.goal=""


    # import tools, initialize the agent
    def codeThreadInitialize(self):
        pass

    # to run the thread
    def codeThreadRun(self):
        
        # start the code thread
        threadCode = threading.Thread(target=self.codeThreadActionFlowRun)
        threadCode.daemon = False
        threadCode.start()
        

        #self.codeThreadActionFlow.actionOnGoing.put(importTools)

        # end the code thread
        threadCode.join()

    # for the wrapper of action
    def codeThread(self, func):
        def wrapper(self, *args, **kwargs):
            self.initialize()
            func(*args, **kwargs)
        
        self.currentThreadName="codeThread"
        sourseCode=inspect.getsource(func)

        # if the function is action, initialize the actionFlow
        funcName=func.__name__
        if funcName == "actionFlow":

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
        exec(code, self.varsFuncs_Temp)


    def codeThreadActionFlowRun(self):

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
                    


                    exec(action, self.varsFuncs_Temp)
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


class Puppy(CodeThread):
    def __init__(self, name="puppy"):
        
        super().__init__()
        self.puppyName=name

    def run(self):
        self.codeThreadRun()




