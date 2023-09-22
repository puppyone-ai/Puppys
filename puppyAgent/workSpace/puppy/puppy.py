from types import MethodType
import threading

class Puppy:
    def __init__(self, name="", discription="", actionFlow=[], authorizedTools={}, inbox=[],retrieve=[], **kwargs):
        self.name = name
        self.discription = discription
        self.actionFlow = actionFlow
        self.inbox = inbox
        self.authorizedTools = authorizedTools
        self.retrive = retrieve
        
        for key, value in kwargs.items():
            # if the value is a function or method, bind it to the current instance
            if callable(value):
                setattr(self, key, value.__get__(self))
            # else, set it as a property
            else:
                setattr(self, key, value)
        """
        name: the name of the agent
        (for example: "David")
        discription: the discription of the agent
        (for example: "an leader agent that are capable of contacting other agents.
        actionFlow: the action flow that the agent should execute
        (for example: ["action1", "action2"])
        authorized: the authority of the agent
        (for example: {"tools":["tool1", "tool2"]}
        inbox: the message box of the agent
        (for example: ["message1", "message2"])
        """

    def getName(self):
        return self.name
    
    def setName(self, newName):
        self.name = newName
    
    def getDiscription(self):
        return self.discription
    
    def setDiscription(self, newDiscription):
        self.discription = newDiscription
    
    def getAuthorizedTools(self):
        return self.authorizedTools
    
    def setAuthorizedTools(self, newAuthorizedTools):
        self.authorizedTools = newAuthorizedTools

    # add a new customized function to the class
    def addFunction(self, func):
        setattr(self, func.__name__, MethodType(func, self))

    # update a customized function to the class, same as addFunction
    def updateFunction(self, func):
        self.addFunction(func)

    # add a new customized property to the class
    def addProperty(self, attr_name, value):
        setattr(self, attr_name, value)

    # update a customized property to the class, same as addProperty
    def updateProperty(self, attr_name, value):
        self.addProperty(attr_name, value)
    
    # run the agent with two threads, main thread and branch thread,
    # main thread is for the inbox, for total action management,
    # branch thread is for the action
    def run(self):
        mainThread = threading.Thread(target=self.runMainThread)
        branchThread = threading.Thread(target=self.runBranchThread)
        mainThread.start()
        branchThread.start()

        # wait for all threads to finish
        mainThread.join()
        branchThread.join()

    # run the main thread
    def runMainThread(self):
        print("Main thread for agent is running")

    # run the branch thread
    def runBranchThread(self):
        print("Branch thread for agent is running")


if __name__=="__main__":
    A=Puppy("David", {"tools":["tool1", "tool2"]}, "an leader agent that are capable of contacting other agents.",age=25)
    print(A.age)
    A.age=3
    print( A.age)
    A.country=9
    print(A.country)
    A.run()

    
    



