import inspect
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompt.actionFlowPrompt import fillingActionFlow_JSON_to_JSON, fillingActionFlow_JSON_to_JSON_RAW,flillingActionFlow_Python_to_Python, flillingActionFlow_Python_to_Python_RAW, fillingActionParameter_JSON_to_Python


class Action():
    def __init__(self):
        self.actionFlow = []
        self.functions = []
        self.currentStep = 0
        self.task=None

    # add a new customized function to the class
    def run(self):
        for func in self.functions:
            func()
    
    # translate the code to action flow in JSON format
    def action(self, func):
        def wrapper(*args, **kwargs):

            # read the source code and extract the action flow
            sourceCode = inspect.getsource(func)
            lines = sourceCode.split('\n')
            searchForDo = False
            comment = ""
            for line in lines:
                if '##' in line:
                    if searchForDo==True:
                        self.actionFlow.append({"action":comment,"status":"fixed"})
                        searchForDo = False
                    comment = line.split('##', 1)[1].strip()
                    searchForDo = True
                else:
                    if searchForDo==True:
                        if '.do()' in line:
                            if comment.strip() == "":
                                self.actionFlow.append({"action":comment,"status":"changeable"})
                            else:
                                self.actionFlow.append({"action":comment,"status":"semi-fixed"})
                            searchForDo = False
                        else:

                            #TODO: add the code to the list
                            pass
                    else:
                        pass
            if searchForDo==True:
                self.actionFlow.append({"action":comment,"status":"fixed"})
                searchForDo = False

            # distilate the task from the function
            print(self.actionFlow)
            self.task= inspect.signature(func).parameters["task"]

            # make the overall plan for the agent
            try:
                self.planning= inspect.signature(func).parameters["planning"].default
                if self.planning == False:
                    pass
                else:
                    self.plan()

            except:
                self.plan()            

            # run the function defined by user
            self.currentStep = 0

            return func(*args, **kwargs)
            
        self.functions.append(wrapper)
        return wrapper
    
    # make the overall plan for the task
    def plan(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-0613",ApiKey="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"):
        # set up the Action planning

        # only for testing
        os.environ["OPENAI_API_KEY"]=ApiKey

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionFlow=LLMChain(llm=llm, prompt= fillingActionFlow_JSON_to_JSON)

        # only for testing:
        toolsSimplified="""
        google_search: search for information via GoogleSearch, it's aviliable anytime you search
        zhihu_search: search for knowledge via ZhihuSearch, recommended for Chinese knowledge
        ChatGPT: ask ChatGPT for help, you can find information that is not timely
        Nothing: just write python code
        Message: send a message to the user
        Save: save the result to the database
        """
        agentExperience="none"

        # predict the workflow
        newActionFlowStr=fillingActionFlow.predict(task =self.task, action_flow=self.actionFlow,tools_overview=toolsSimplified, experiences=agentExperience,language="Chinese")
        self.actionFlow=eval(newActionFlowStr)

        print(self.actionFlow)

    # for each action, decide how to do and do it
    def act(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-0613",ApiKey="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"):

        # only for testing
        os.environ["OPENAI_API_KEY"]=ApiKey

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionParameter=LLMChain(llm=llm, prompt= fillingActionParameter_JSON_to_Python)

        # only for testing:
        toolsSimplified="""
        google_search: search for information via GoogleSearch, it's aviliable anytime you search
        zhihu_search: search for knowledge via ZhihuSearch, recommended for Chinese knowledge
        ChatGPT: ask ChatGPT for help, you can find information that is not timely
        Nothing: just write python code
        Message: send a message to the user
        Save: save the result to the database
        """
        agentExperience="none"

        # predict the workflow
        newAction=fillingActionParameter.predict(task=self.task, action_flow=self.actionFlow, num=self.currentStep, current_action=self.actionFlow[self.currentStep],tools_detail=toolsSimplified, experiences=agentExperience)
        print(newAction)
        

    # do the action 
    #TODO: If the user set multiple consecutively actions with the status as "changeable", an Index error will be reported.
    def do(self):
        print("current step:",self.currentStep)
        if self.actionFlow[self.currentStep]["status"] == "semi-fixed":
            print("action:", self.actionFlow[self.currentStep]["action"])
            self.act()
            self.currentStep += 1

        elif self.actionFlow[self.currentStep]["status"] == "fixed":
            print("action:", self.actionFlow[self.currentStep]["action"])
            self.currentStep += 1
            self.do()
        
        elif self.actionFlow[self.currentStep]["status"] == "changeable":
            print("action:", self.actionFlow[self.currentStep]["action"])
            self.act()
            try:
                while self.actionFlow[self.currentStep+1]["status"] == "changeable":
                    self.currentStep += 1
                    self.act()
            except IndexError:
                pass
            self.currentStep += 1


    # filling out all the actions in the action flow
    def taskToAction(self):
        print(self.actionFlow)
        print(self.task)
        print(self.currentStep)

    def actionToTools(self):
        print(self.actionFlow(self.currentStep))
        
puppy1 = Action()


@puppy1.action
def WeatherAgent(task="告诉我Who won the US Open men's final in 2019? What is his age raised to the 0.334 power?",planning=True): 

    ## search for the quesiton @google search
    puppy1.do()

    ## rethink about the answer @rethinker
    puppy1.do()

    ## clarify I am still running
    print("now i am here")

    ##
    puppy1.do()

    ## send the message to the president of the United States
    puppy1.do()

puppy1.run()


'''
    ## search for the quesiton @google search @zhihu search
    puppy1.do()

    ## rethink about the answer @rethinker
    puppy1.do()

    ## clarify I am still running
    print("now i am here")

    ##
    puppy1.do()

    ## rethink about the answer @rethinker
    puppy1.do()'''