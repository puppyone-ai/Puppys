
import pandas as pd
from googleapiclient.discovery import build


class AskHumanForHelp:
    def __init__(self, threadInstance, question='',**kwargs):
        self.threadInstance = threadInstance
        self.name="askHumanForHelp"
        self.description = "Use it when you have no idea how to achieve an action based on the current information knowledge, or functions."
        self.example = """
        ## Ask the user for the informaiton of the phone number of his boss
        answer = puppy.askHumanForHelp.run("What's the phone number of your boss?") # where the puppy is name, change it with your name
        """
        self.functionBeforeAction = []
        self.functionAfterAction = []
        self.allowedThread = ["codeThread"]


        self.question = question


    def getExample(self):
        return self.example
    
    def getDescription(self):  
        return self.description
    
    def getDescriptionAndExample(self):
        return self.description+"\n"+self.example
    
    def setQuestion(self,question):
        self.question=question

    
    def run(self,question=""):
        self.question=question

        userInput=input(question+"\n"+"Your answer:")
        print("Sure, I have already add what you said to my knowledge.")

        self.threadInstance.actionFlow.actionFlowCurrentGetFrontAddCode(str("'''\n")+userInput+str("\n'''"))

        return userInput
