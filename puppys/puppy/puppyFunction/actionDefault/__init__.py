from .sendMessageToHuman import SendMessageToHuman
from .googleSearchNative import GoogleSearchNative
from .gpt import GPT

class ActionDefault:

    def __init__(self, codeThreadInstance):
        self.codeThreadInstance = codeThreadInstance
        self.sendMessageToHuman = SendMessageToHuman(self.codeThreadInstance)
        self.googleSearchNative = GoogleSearchNative(self.codeThreadInstance)
        self.gpt = GPT(self.codeThreadInstance)


    def getDescriptions(self):
        functionsSimplified="""
        """
        functionsSimplified+="1. AskHumanForHelp:"+SendMessageToHuman(self.codeThreadInstance).getDescription()+"\n"
        functionsSimplified+="2. GoogleSearchNative:"+GoogleSearchNative(self.codeThreadInstance).getDescription()+"\n"
        functionsSimplified+="3. GPT:"+GPT(self.codeThreadInstance).getDescription()+"\n"
        return functionsSimplified

    def getExamples(self):
        functionsExample="""
        """
        functionsExample+=SendMessageToHuman(self.codeThreadInstance).getExample()+"\n"
        functionsExample+=GoogleSearchNative(self.codeThreadInstance).getExample()+"\n"
        functionsExample+=GPT(self.codeThreadInstance).getExample()+"\n"
        return functionsExample

    def getDescriptionAndExample(self):
        
        functionsDescriptionAndExample="""
        """
        functionsDescriptionAndExample+="1. AskHumanForHelp:"+SendMessageToHuman(self.codeThreadInstance).getDescription()+"\n"
        functionsDescriptionAndExample+=SendMessageToHuman(self.codeThreadInstance).getExample()+"\n"

        functionsDescriptionAndExample+="2. GoogleSearchNative:"+GoogleSearchNative(self.codeThreadInstance).getDescription()+"\n"
        functionsDescriptionAndExample+=GoogleSearchNative(self.codeThreadInstance).getExample()+"\n"

        functionsDescriptionAndExample+="3. GPT:"+GPT(self.codeThreadInstance).getDescription()+"\n"
        functionsDescriptionAndExample+=GPT(self.codeThreadInstance).getExample()+"\n"
        
        return functionsDescriptionAndExample