import inspect
import os
import re
import copy
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompt.actionFlowPrompt import FlillingActionFlow_JSON_to_JSON, FillingActionFlow_JSON_to_JSON_GPTPolished

#FlillingActionFlow_Python_to_Python, FlillingActionFlow_Python_to_Python_GPTPolished, FillingActionParameter_JSON_to_Python


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
            sourceCode = inspect.getsource(func)
            lines = sourceCode.split('\n')
            is_comment = False
            comment = ""
            for line in lines:
                if is_comment:
                    is_comment = False
                    if '.do()' in line:
                        self.actionFlow.append({"action":comment,"status":"changable"})
                    else:
                        self.actionFlow.append({"action":comment,"status":"fixed"})
                elif '##' in line:
                    comment = line.split('##', 1)[1].strip()
                    is_comment = True
            print(self.actionFlow)
            self.task= inspect.signature(func).parameters["task"]

            self.plan()

            # run the function defined by user
            self.currentStep = 0

            return func(*args, **kwargs)
            
        self.functions.append(wrapper)
        return wrapper
    
    # make the overall plan for the agent
    def plan(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-0613",ApiKey="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"):
        # set up the AgentAction for planning action and filling parameter

        # only for testing
        os.environ["OPENAI_API_KEY"]=ApiKey

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionFlow=LLMChain(llm=llm, prompt= FlillingActionFlow_JSON_to_JSON)

        # only for testing:
        toolsSimplified="google_search, zhihu_search, code, ChatGPT"
        agentExperience="none"


        # predict the workflow
        NewActionFlowStr=fillingActionFlow.predict(task =self.task, action_flow=self.actionFlow,tools_overview=toolsSimplified, experiences=agentExperience,language="Chinese")
        self.actionFlow=eval(NewActionFlowStr)

        print(self.actionFlow)


    # let puppy to run what was planned to be responsibled for puppy
    def do(self):
        if self.actionFlow[self.currentStep]["status"] == "changable":
            print("action for puppy:",self.actionFlow[self.currentStep]["action"])
        elif self.actionFlow[self.currentStep]["status"] == "fixed":
            print("action for human:",self.actionFlow[self.currentStep]["action"])
        else:
            print("error")
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
def ReAct(task="provide the answer to the input question"): 

    ## search for the quesiton @google search @zhihu search
    puppy1.do()

    ## rethink about the answer @rethinker
    puppy1.do()

    ## clarify I am still running
    print("now i am here")

    ##TODO
    puppy1.do()

    print("end")


puppy1.run()