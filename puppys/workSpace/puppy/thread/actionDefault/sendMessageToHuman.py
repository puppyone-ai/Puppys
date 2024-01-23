
import pandas as pd
from googleapiclient.discovery import build


class SendMessageToHuman:
    def __init__(self, threadInstance, question='',**kwargs):
        self.puppyName=threadInstance.puppyName
        self.threadInstance = threadInstance
        self.ActionName="sendMessageToHuman"
        self.description = """Use it when you have no idea how to achieve an action based on the current information knowledge, or functions. or you want to convey a message to the user
        If you feel confused about any knowledge that are essential for following actions. You can stop keeping going and only ask human for help. You don't need to finish all the actions in one time.
        """
        self.example = f"""
        ## Ask the user about the phone number of his boss
        answer = {self.puppyName}.sendMessageToHuman.run("What's the phone number of your boss?") 
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
        print("example is",self.example)
        self.question=question

        userInput=input(question+"\n"+"Your response:")
        print("Sure, I have already add what you said to my knowledge.")

        chatHistory="\n"+str('"""')+"Your response:"+str(self.question)+"\n"+"User's response:"+userInput+"\n"+str('"""')

        self.threadInstance.actionFlow.actionFlowCurrentGetFrontAddCode(chatHistory)  
        return userInput
    
