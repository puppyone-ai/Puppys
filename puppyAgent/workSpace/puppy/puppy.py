class Puppy:
    def __init__(self, name, authorizedTools={}, discription=""):
        self.name = name
        self.discription = discription
        self.authorizedTools = authorizedTools

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
    
    def getDiscription(self):
        return self.discription
    
    def getAuthorizedTools(self):
        return self.authorizedTools
    
    

