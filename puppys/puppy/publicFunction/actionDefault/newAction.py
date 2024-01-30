class newAction:
    def __init__(self):
        name=""
        self.description = ""
        self.example = """
        ## Ask the user for the informaiton of the phone number of his boss
        X = newAction()
        result = X.run()
        """

        self.functionBeforeAction = []
        self.functionAfterAction = []


    def getExample(self):
        return self.example
    
    def getDescription(self):  
        return self.description
    
    def getFunctionBeforeAction(self):
        return self.functionBeforeAction
    
    def getFunctionAfterAction(self):
        return self.functionAfterAction

    def run(self):
        pass

        