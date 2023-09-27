

class Authority:
    def __init__(self, authorizedTools=None):

        # define the authorized tools
        self.authorizedTools = authorizedTools

    # add a new authorized tool
    def append(self, item: str):
        self.authorizedTools.append(item)

    # remove a tool from the authorized tools
    def remove(self, item: str):
        self.authorizedTools.remove(item)

    # clear the authorized tools
    def clear(self):
        self.authorizedTools.clear()

    # get the authorized tools
    def get(self):
        return self.authorizedTools
    
    def __str__(self):
        return str(self.authorizedTools)
    
    def __repr__(self):
        return repr(self.authorizedTools)

    #TODO define the tools picker
    def toolsPicker(self):
        pass