
import pandas as pd
from googleapiclient.discovery import build


class SendMessageToHuman:
    def __init__(self, threadInstance, question='',**kwargs):
        self.threadInstance = threadInstance
        self.name="sendMessageToHuman"
        self.description = "Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user "
        self.example = """
        ## Ask the user about the phone number of his boss
        answer = puppy.sendMessageToHuman.run("What's the phone number of your boss?") # where the puppy is name, change it with your name
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

        userInput=input(question+"\n"+"Your response:")
        print("Sure, I have already add what you said to my knowledge.")

        chatHistory="\n"+str('"""')+"Your response:"+str(self.question)+"\n"+"User's response:"+userInput+"\n"+str('"""')

        self.threadInstance.actionFlow.actionFlowCurrentGetFrontAddCode(chatHistory)  
        return userInput