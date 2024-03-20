from .send_message_to_human import Send_message_to_human
from .googleSearchNative import GoogleSearchNative
from .gpt import GPT

class ActionDefault:

    def __init__(self, codeThreadInstance):
        self.codeThreadInstance = codeThreadInstance
        self.sendMessageToHuman = Send_message_to_human(self.codeThreadInstance)
        self.googleSearchNative = GoogleSearchNative(self.codeThreadInstance)
        self.gpt = GPT(self.codeThreadInstance)


    def getDescriptions(self):
        functionsSimplified="""
        """
        functionsSimplified+="1. AskHumanForHelp:" + Send_message_to_human(self.codeThreadInstance).get_description() + "\n"
        functionsSimplified+="2. GoogleSearchNative:"+GoogleSearchNative(self.codeThreadInstance).getDescription()+"\n"
        functionsSimplified+="3. GPT:" + GPT(self.codeThreadInstance).get_description() + "\n"
        return functionsSimplified

    def getExamples(self):
        functionsExample="""
        """
        functionsExample+= Send_message_to_human(self.codeThreadInstance).get_example() + "\n"
        functionsExample+=GoogleSearchNative(self.codeThreadInstance).getExample()+"\n"
        functionsExample+= GPT(self.codeThreadInstance).get_example() + "\n"
        return functionsExample

    def getDescriptionAndExample(self):
        
        functionsDescriptionAndExample="""
        """
        functionsDescriptionAndExample+="1. AskHumanForHelp:" + Send_message_to_human(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample+= Send_message_to_human(self.codeThreadInstance).get_example() + "\n"

        functionsDescriptionAndExample+="2. GoogleSearchNative:"+GoogleSearchNative(self.codeThreadInstance).getDescription()+"\n"
        functionsDescriptionAndExample+=GoogleSearchNative(self.codeThreadInstance).getExample()+"\n"

        functionsDescriptionAndExample+="3. GPT:" + GPT(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample+= GPT(self.codeThreadInstance).get_example() + "\n"
        
        return functionsDescriptionAndExample