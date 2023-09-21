class Puppy:
    def __init__(self, name, authorizedTools={}, discription="", **kwargs):
        self.name = name
        self.discription = discription
        self.authorizedTools = authorizedTools

        
        for key, value in kwargs.items():
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

    
    



