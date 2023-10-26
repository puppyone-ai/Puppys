class Authority:
    def __init__(self):

        # define the authorized tools
        self.authorizedTools = """
        google_search: search for information via GoogleSearch, it's aviliable anytime you search
        zhihu_search: search for knowledge via ZhihuSearch, recommended for Chinese knowledge
        ChatGPT: ask ChatGPT for help, you can find information that is not timely
        Nothing: just write python code
        Message: send a message to the user
        Save: save the result to the database
        """

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


    