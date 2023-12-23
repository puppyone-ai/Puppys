
import pandas as pd
from googleapiclient.discovery import build


class AskHumanForHelp:
    def __init__(self, question='',**kwargs):
        self.description = "Use it when you have no idea how to achieve an action based on the current information knowledge, or functions."
        self.example = """
        ## Ask the user for the informaiton of the phone number of his boss
        askingHuman = AskHumanForHelp("what is the phone number of your boss?")
        answer = askingHuman.run()
        """

        self.question = question


    def getExample(self):
        return self.example
    
    def getDescription(self):  
        return self.description

    
    def run(self):
        print("waiting.........")





        