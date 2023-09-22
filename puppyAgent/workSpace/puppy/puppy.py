from types import MethodType

class Puppy:
    def __init__(self, name, authorizedTools={}, discription="", **kwargs):
        self.name = name
        self.discription = discription
        self.authorizedTools = authorizedTools

        
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
        authorized: the authority of the agent
        (for example: {"tools":["tool1", "tool2"]})
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
    
    # run the agent with two threads
    def run(self):
        pass

if __name__=="__main__":
    A=Puppy("David", {"tools":["tool1", "tool2"]}, "an leader agent that are capable of contacting other agents.",age=25)
    print(A.age)
    A.age=3
    print( A.age)
    A.country=9
    print(A.country)

    
    



