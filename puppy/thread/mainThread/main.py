import inspect
import threading
from .actionflow import Actionflow
from .actions import Actions
#from ...publicFunc.default import ActionDefault


class MainThread():
    def __init__(self):
        
        self.current_thread_name= "mainThread"
        self.actionflow=Actionflow(self)
        self.actions=Actions(self)

        self.thread_Property={}

        self.agent_var_func = {}

        self.agent_func = {}
        self.agent_var = {}


        self.environment = {"self":self}

        self.goal=""



    # to get value from agentVar
    def __getattr__(self, attr):
        if attr in self.agent_var:
            return attr.value

        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


    ## the templete of an func for agents
    class agent_func_template:
        def __init__(self, thread_instance, **kwargs):
            self.thread_instance = thread_instance
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
    class Agent_var_templete:
        def __init__(self, thread_instance, **kwargs):
            self.thread_instance = thread_instance
            self.name = "None"
            self.tag = "var"
            self.description = "nothing"
            self.value = None


    # TODO
    def add_new_func(self, func):
        pass

    # TODO
    def add_new_var(self, func):
        pass

    def new_agent_func(self, func):
        args = inspect.getfullargspec(func).args
        source_code=inspect.getsource(func)
        name=func.__name__

        newAgentFunc=self.agent_func_templateTemplete()


        print("name:")
        print(name)

        print("arg:")
        print(args)

        print("source_code:")
        print(source_code)


    def new_agent_var(self, func):
        args = inspect.getfullargspec(func).args
        source_code=inspect.getsource(func)
        name=func.__name__

        print("name:")
        print(name)

        print("arg:")
        print(args)

        print("source_code:")
        print(source_code)


    # to run the thread
    def main_thread_run(self):

        # start the code thread
        thread_code = threading.Thread(target=self.mainthread_actionflow_run)
        thread_code.daemon = False
        thread_code.start()
        

        #self.codeThreadActionFlow.actionOnGoing.put(importTools)


        # end the code thread
        thread_code.join()

    # for the wrapper of action
    def main_thread(self, func):
        def wrapper(self, *args, **kwargs):
            self.initialize()
            func(*args, **kwargs)
        
        self.current_thread_name= "mainThread"
        sourse_code=inspect.getsource(func)

        # if the function is action, initialize the actionFlow
        func_name=func.__name__
        if func_name == "actionflow_pending":

            # get source code
            self.actionflow.initialize(sourse_code)

            print("\U0001F3B2 Initialize Done")
            print("Initialized Function: "+func_name)



        if func_name == "trigger":
            # TODO
            pass

        # execute the function with wrapper
        return wrapper


    def create_puppy_instance(self, instance_name):
        new_instance = Puppy(name=instance_name)
        # 将新创建的实例添加到globalVars字典中，使用instance_name作为键

        globals()[instance_name] = new_instance

    def exec_mode(self, code, mode="thread"):
        exec(code, self.environment)

    def mainthread_actionflow_run(self):

        # import tools, for agents


        # loading actions
        from ...publicFunc.default import ActionDefault

        self.action_default = ActionDefault(self)
        self.sendMessageToHuman = self.action_default.sendMessageToHuman

        self.actionflow.actionflow_current_clear()

        #print(self.Vars)

        print("\U0001F4E5 Import Done")
        # start the action flow

        while self.actionflow.actionflow_current_JSON ==[] and self.actionflow.actionflow_pending_JSON !=[]:

            print("\U0001F525 Action Start")

            # STEP 1: load the action from actionFlowPending to actionFlowCurrent
            self.actionflow.action_current_load()

            # STEP 2: delete the action from actionFlowPending
            self.actionflow.actionflow_pending_remove_front()

            print("\U0001F51C ActionFlowPending:")
            print(self.actionflow.actionflow_pending_JSON)
            print("\U000025B6 ActionFlowCurrentJSON:")
            print(self.actionflow.actionflow_current_JSON)
            print("\U0001F519 ActionFlowHistory:")
            print(self.actionflow.actionflow_history_JSON)

            while self.actionflow.actionflow_current_JSON !=[]:
                
                # STEP 3.1: check if the action is fixed, semi-fixed, or changeable
                if self.actionflow.actionflow_current_get_front()["status"]== "fixed":
                    pass

                elif self.actionflow.actionflow_current_get_front()["status"]== "semi-fixed":
                    self.actions.do()

                elif self.actionflow.actionflow_current_get_front()["status"]== "changeable":
                    pass
                
                # STEP 3.2 load the action from actionCurrent to actionOnGoing
                if self.actionflow.actionflow_current_JSON !=[]:
                    self.actionflow.action_current_execute()
                    

                    # STEP 3.3: load the action from actionOngoing and execute the code, and determine if the action is hidden
                    action = self.actionflow.action_on_going.get()

                    print("\n")
                    print("\U0001F697 Running Code ################################################################")
                    print(action)
                    print("################################################################################")
                    


                    exec(action, self.environment)
                    self.actionflow.action_on_going.task_done()

                    # STEP 4: load the action from the actionFlowCurrent to the actionFlowHistory
                    self.actionflow.action_current_save()


                    # STEP 5: remove the action from the actionFlowCurrent
                    if self.actionflow.actionflow_current_JSON !=[]:
                        self.actionflow.actionflow_current_remove_front()
                    
                    else:
                        pass

                else: 
                    pass

        print("Done")


class Puppy(MainThread):
    def __init__(self, name="puppy"):
        
        super().__init__()
        self.puppy_name=name

    def run(self):
        self.main_thread_run()




