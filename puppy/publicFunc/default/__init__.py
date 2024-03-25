from .send_message_to_human import Send_message_to_human
from .googleSearchnative import Google_search_native
from .gpt import GPT

class ActionDefault:

    def __init__(self, codeThreadInstance):
        self.codeThreadInstance = codeThreadInstance
        self.send_message_to_human = Send_message_to_human(self.codeThreadInstance)
        self.google_search_native = Google_search_native(self.codeThreadInstance)
        self.gpt = GPT(self.codeThreadInstance)


    def get_descriptions(self):
        functionsSimplified="""
        """
        functionsSimplified+="1."+ Send_message_to_human(self.codeThreadInstance).get_name() + Send_message_to_human(self.codeThreadInstance).get_description() + "\n"
        functionsSimplified+="2."+ Google_search_native(self.codeThreadInstance).get_name() + Google_search_native(self.codeThreadInstance).get_description() + "\n"
        functionsSimplified+="3."+ GPT(self.codeThreadInstance).get_name() + GPT(self.codeThreadInstance).get_description() + "\n"
        return functionsSimplified

    def get_examples(self):
        functionsExample="""
        """
        functionsExample+= Send_message_to_human(self.codeThreadInstance).get_example() + "\n"
        functionsExample+= Google_search_native(self.codeThreadInstance).get_example() + "\n"
        functionsExample+= GPT(self.codeThreadInstance).get_example() + "\n"
        return functionsExample

    def get_description_and_example(self):
        
        functionsDescriptionAndExample="""
        """
        functionsDescriptionAndExample+="1."+ Send_message_to_human(self.codeThreadInstance).get_name() + Send_message_to_human(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample+= Send_message_to_human(self.codeThreadInstance).get_example() + "\n"

        functionsDescriptionAndExample+="2." + Google_search_native(self.codeThreadInstance).get_name() + Google_search_native(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample+= Google_search_native(self.codeThreadInstance).get_example() + "\n"

        functionsDescriptionAndExample+="3."+ GPT(self.codeThreadInstance).get_name() + GPT(self.codeThreadInstance).get_description() + "\n"
        functionsDescriptionAndExample+= GPT(self.codeThreadInstance).get_example() + "\n"
        
        return functionsDescriptionAndExample