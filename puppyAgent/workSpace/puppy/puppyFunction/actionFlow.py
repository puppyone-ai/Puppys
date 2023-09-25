class Action():
    def __init__(self):
        pass


    # add a new customized function to the class
    def runAction(self):
        pass


    """
    support 3 types of actionFlows:
    1. code mode
    2. text mode
    3. JSON mode
    """

    """for example:
    
    #code mode:
    def ReAct(self):
        start()
        searchResult=""
        if answerQuestion(question,searchResult)==False:
            information=Rethink(searchResult)
            searchResult = GoogleSearch(information))
        end()
        return searchResult

    #text mode:
    actionFlow=["start",
    "think if the answer is correct"-->["yes", "no"],
    if "no":[
    "rethink",
    "search"],
    else:[pass],
    "end"]

    #JSON mode:
    {{action:"start"
    }
    
    }

    """
    
    """for example:
    actionFlow=[Think if
    
    """