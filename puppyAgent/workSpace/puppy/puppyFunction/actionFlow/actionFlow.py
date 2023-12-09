import inspect
import sys
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

    def actionFlowJSON2Python(self,JSON):
        pass

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

            
            # import the default tools in the code thread
            importDefault="""
            from actionLib.actionDefault.googleSearchNative import GoogleSearchNative
            from actionLib.actionDefault.GPT import GPT
            """

            # start to run the agent in the code thread
            self.taskQueue.put(importDefault)
            
            

            self.currentStep = 0

            result = func(*args, **kwargs)
            self.taskQueue.put(None)

            # end the code thread
            tCode.join()

            print("CODE HISTORY:",''.join(self.actionFlowPython))
            
            return result

        self.functions.append(wrapper)
        return wrapper
    
    def code(self, function):
        pass

    def planning(self, function):
        pass


    # the thread for running code(actionFlow should be run in this thread)
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

    def importTools(self): 

        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

        from actionLib.actionDefault.googleSearchNative import GoogleSearchNative
        from actionLib.actionDefault.GPT import GPT

        self.toolsBox=[]
        self.toolsBox.append(GoogleSearchNative)
        self.toolsBox.append(GPT)

    def getDescriptions(self):

        self.functionsSimplified="""
        """
        for tool in self.toolsBox:
            self.functionsSimplified+=tool().getDescription()+"\n"

    def getExamples(self):

        self.functionsExample="""
        """
        for tool in self.toolsBox:
            self.functionsExample+=tool().getExample()+"\n"

        
    # make the overall plan for the task
    def plan(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionFlow=LLMChain(llm=llm, prompt= fillingActionFlow_JSON_to_JSON)

        self.importTools()
        self.getDescriptions()
        self.getExamples()

        agentExperience="none"

        # predict the workflow
        newActionFlowStr=fillingActionFlow.predict(task=self.task, action_flow=self.actionFlowJSON,functions_overview=self.functionsSimplified, experiences=agentExperience,language="Chinese")
        self.actionFlowJSON=eval(newActionFlowStr)

        print(self.actionFlowJSON)

    # for each action, decide how to do and do it
    def act(self,temperature=0.1,max_tokens=2000,model_name="gpt-4-1106-preview",ApiKey="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"):
        os.environ["OPENAI_API_KEY"]=ApiKey

        llm=ChatOpenAI(temperature=temperature,max_tokens=max_tokens,model_name=model_name)
        fillingActionParameter=LLMChain(llm=llm, prompt= fillingActionParameter_JSON_to_Python)

        self.importTools()
        self.getDescriptions()
        self.getExamples()

        agentExperience="none"

        newAction=fillingActionParameter.predict(task=self.task, action_flow=self.actionFlowJSON, num=self.currentStep, current_action=self.actionFlowJSON[self.currentStep],example=self.functionsExample, code_history=''.join(self.actionFlowPython),experiences=agentExperience)
        
        # only for GPT-4
        newAction=newAction.replace("```python\n", "").replace("\n```", "")
        self.taskQueue.put(newAction)

        print("newAction:",newAction)


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
                    print("action:", self.actionFlowJSON[self.currentStep]["action"])
                    self.act()
            except IndexError:
                print("IndexError")

            self.currentStep += 1

    def taskToAction(self):
        print(self.actionFlowJSON)
        print(self.task)
        print(self.currentStep)

    def actionToFunctions(self):
        print(self.actionFlowJSON(self.currentStep))







puppy1 = Action()

@puppy1.action
def Yuning(task="帮我找到全网最便宜的 iPhone 购买渠道",planning=True): 

    ##
    puppy1.do()

    ## send the message to me 
    puppy1.do()

    ##
    puppy1.do()


puppy1.run()

