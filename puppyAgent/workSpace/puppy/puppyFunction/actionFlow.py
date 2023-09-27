class Action():
    def __init__(self):
        import inspect

    # add a new customized function to the class
    def runAction(self):
        pass

    # to extract the comments from the function
    def codeActionFlowInterpreter(self,func,mark="#TODO"):
        import inspect

        comments = []
        
        # 获取多行注释（docstring）
        docstring = inspect.getdoc(func)
        if docstring:
            comments.append(docstring)
        
        # 获取源代码
        source_code = inspect.getsource(func)
        
        # 提取单行注释
        lines = source_code.split('\n')
        for line in lines:
            if mark in line:
                comment = line.split(mark, 1)[1].strip()
                comments.append(comment)
        
        print(comments)
        return comments
    
    # add a new customized function after each #TODO mark
    def puppy(func):
        def wrapper(*args, **kwargs):
            # 获取原函数的源代码
            source_lines = inspect.getsource(func).split('\n')

            # 在每个 #TODO 后动态运行新函数
            for line in source_lines:
                if '#TODO' in line:
                    newFunction()

            # 运行原函数
            return func(*args, **kwargs)

        return wrapper

    @puppy
    def Test(self):
        def ReAct(self, task="provide the answer to the input question"):   
        
            #TODO search for the quesiton @google search @zhihu search
            completeThis()

            #TODO search for the question @google search @zhihu search
            completeThis()

            #DONE: for agent to design the action
            searchResult=""
            while answerQuestion(question,searchResult)==False:
                information=Rethink(searchResult)
                searchResult = GoogleSearch(information)
            puppyDecision()
            return searchResult

            #TODO

            pass

if __name__ == "__main__":
    A=Action()
    A.codeActionFlowInterpreter(A.Test)

"""
    support 3 types of actionFlows:
    1. code mode
    2. text mode
    """

"""
    to determine which typing mode to use, following mode should be tested:
    1. 
    func(self,task)
    ## for agent to design the action
    # for human to design the action


    2. 
    func(self,task)
    ### for agent to design the action
    ## for human to design the action


    3. 
    func(self,task)
    ## for agent to know what the action should be
    action(), for agent to design the action
    ## for human to design the action


    #code mode:
    @puppy1
    def ReAct(self, task="provide the answer to the input question"):   
        
        ### search for the quesiton @google search @google search
        XX()
        ### rethink @rethinking

        ### search again @google search

        ## search for the result 
        searchResult=""
        while answerQuestion(question,searchResult)==False:
            information=Rethink(searchResult)
            searchResult = GoogleSearch(information)
        puppyDecision()
        return searchResult

        ##

        ## end

    puppy1.run()

    """

"""
    #text mode:
    []for the overall flow
    ()for workflow defined by human
    {}for if/else

    actionFlow=

    [("search for the question"@google search),"rethink","search again",[],"end"]

    ["search for the "
        "think if the answer is correct"-->["yes", "no"],
    if "no":[
    "rethink if ",
    "search"],
    else:[pass],
    "end"]

    """