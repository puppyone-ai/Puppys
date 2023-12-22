from askHumanForHelp import AskHumanForHelp
from googleSearchNative import GoogleSearchNative
from gpt import GPT



def getDescriptions():
    functionsSimplified="""
    """
    functionsSimplified+="1. AskHumanForHelp:"+AskHumanForHelp().getDescription()+"\n"
    functionsSimplified+="2. GoogleSearchNative:"+GoogleSearchNative().getDescription()+"\n"
    functionsSimplified+="3. GPT:"+GPT().getDescription()+"\n"
    return functionsSimplified

def getExamples():
    functionsExample="""
    """
    functionsExample+=AskHumanForHelp().getExample()+"\n"
    functionsExample+=GoogleSearchNative().getExample()+"\n"
    functionsExample+=GPT().getExample()+"\n"
    return functionsExample


if __name__ == "__main__":
    print(getDescriptions())
    print(getExamples())