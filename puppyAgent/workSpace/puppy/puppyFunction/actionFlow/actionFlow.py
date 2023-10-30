import inspect
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompt.actionFlowPrompt import *

import threading
import queue

class Action():
    def __init__(self):
        self.actionFlowJSON = []
        self.actionFlowPython=[]
        self.functions = []
        self.currentStep = 0
        self.task=None

    # to run the agent
    def run(self):
        for func in self.functions:
            func()

    # translate the actionFlowPython to actionFlowJSON(Initial)
    def actionFlowPython2JSONInitial(self,code):
        lines = code.split('\n')
        searchForDo = False
        comment = ""

        # translate the actionFlowPython to actionFlowJSON 
        for line in lines:
            if '##' in line:
                if searchForDo==True:
                    self.actionFlowJSON.append({"action":comment,"status":"fixed"})
                    searchForDo = False
                comment = line.split('##', 1)[1].strip()
                searchForDo = True
            else:
                if searchForDo==True:
                    if '.do()' in line:
                        if comment.strip() == "":
                            self.actionFlowJSON.append({"action":comment,"status":"changeable"})
                        else:
                            self.actionFlowJSON.append({"action":comment,"status":"semi-fixed"})
                        searchForDo = False
                    else:
                        pass
                else:
                    pass
        if searchForDo==True:
            self.actionFlowJSON.append({"action":comment,"status":"fixed"})
            searchForDo = False

    # translate the code to action flow in JSON format, and run the agent
    def action(self, func):
        def wrapper(*args, **kwargs):
            sourceCode = inspect.getsource(func)

            # translate user's code to JSON actionflow
            self.actionFlowPython2JSONInitial(sourceCode)
            
            # distilate the task from the function
            print(self.actionFlowJSON)
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

            self.taskQueue = queue.Queue()
            tCode = threading.Thread(target=self.codeThread, args=(self.taskQueue,))
            tCode.start()

            self.currentStep = 0

            result = func(*args, **kwargs)
            self.taskQueue.put(None)
            tCode.join()

            print("CODE HISTORY:",''.join(self.actionFlowPython))
            
            return result

        self.functions.append(wrapper)
        return wrapper
    
    def codeThread(self, task_queue):
        while True:
            task = task_queue.get()
            if task is None:
                break
            try:
                self.actionFlowPython.append('##'+self.actionFlowJSON[self.currentStep]["action"]+'\n'+task+'\n')
                exec(task)
            except Exception as e:
                print(f"Error executing task: {e}")
            task_queue.task_done()

    # make the overall plan for the task
    def plan(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-0613",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionFlow=LLMChain(llm=llm, prompt= fillingActionFlow_JSON_to_JSON)

        functionsSimplified="""
        google_search: search for information via GoogleSearch, it's aviliable anytime you search
        zhihu_search: search for knowledge via ZhihuSearch, recommended for Chinese knowledge
        ChatGPT: ask ChatGPT for help, you can find information that is not timely
        Nothing: just write python code
        Message: send a message to the user
        Save: save the result to the database
        """
        agentExperience="none"

        # predict the workflow
        newActionFlowStr=fillingActionFlow.predict(task=self.task, action_flow=self.actionFlowJSON,functions_overview=functionsSimplified, experiences=agentExperience,language="Chinese")
        self.actionFlowJSON=eval(newActionFlowStr)

        print(self.actionFlowJSON)

    # for each action, decide how to do and do it
    def act(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-0613",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionParameter=LLMChain(llm=llm, prompt= fillingActionParameter_JSON_to_Python)

        functionsSimplified="""
        google_search: search for information via GoogleSearch, it's aviliable anytime you search
        zhihu_search: search for knowledge via ZhihuSearch, recommended for Chinese knowledge
        ChatGPT: ask ChatGPT for help, you can find information that is not timely
        Nothing: just write python code
        Message: send a message to the user
        Save: save the result to the database
        """
        agentExperience="none"

        newAction=fillingActionParameter.predict(task=self.task, action_flow=self.actionFlowJSON, num=self.currentStep, current_action=self.actionFlowJSON[self.currentStep],functions_detail=functionsSimplified, code_history=''.join(self.actionFlowPython),experiences=agentExperience)
        self.taskQueue.put(newAction)

        print(newAction)

    # for each action, puppy writes code to achieve the action.
    def do(self):

        print("current step:",self.currentStep)
        if self.actionFlowJSON[self.currentStep]["status"] == "semi-fixed":
            print("action:", self.actionFlowJSON[self.currentStep]["action"])
            self.act()
            self.currentStep += 1

        elif self.actionFlowJSON[self.currentStep]["status"] == "fixed":
            print("action:", self.actionFlowJSON[self.currentStep]["action"])
            self.currentStep += 1
            self.do()
        
        elif self.actionFlowJSON[self.currentStep]["status"] == "changeable":
            print("action:", self.actionFlowJSON[self.currentStep]["action"])
            self.act()
            try:
                while self.actionFlowJSON[self.currentStep+1]["status"] == "changeable":
                    self.currentStep += 1
                    self.act()
            except IndexError:
                pass
            self.currentStep += 1

    def taskToAction(self):
        print(self.actionFlowJSON)
        print(self.task)
        print(self.currentStep)

    def actionToFunctions(self):
        print(self.actionFlowJSON(self.currentStep))

puppy1 = Action()

@puppy1.action
def WeatherAgent(task="compare about the price of Skyline1 and Skyline2(they are games)",planning=True): 

    ##
    puppy1.do()

    ## rethink about the result
    puppy1.do()

    ## compare about the price
    puppy1.do()
    
    ## send the result to my mom
    print("sent")

puppy1.run()
