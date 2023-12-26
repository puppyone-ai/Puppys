import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def getDescriptionAndExample():
    
    functionsDescriptionAndExample="""
    """
    functionsDescriptionAndExample+="1. AskHumanForHelp:"+AskHumanForHelp().getDescription()+"\n"
    functionsDescriptionAndExample+=AskHumanForHelp().getExample()+"\n"

    functionsDescriptionAndExample+="2. GoogleSearchNative:"+GoogleSearchNative().getDescription()+"\n"
    functionsDescriptionAndExample+=GoogleSearchNative().getExample()+"\n"

    functionsDescriptionAndExample+="3. GPT:"+GPT().getDescription()+"\n"
    functionsDescriptionAndExample+=GPT().getExample()+"\n"
    
    return functionsDescriptionAndExample


if __name__ == "__main__":
    print(getDescriptions())
    print(getExamples())