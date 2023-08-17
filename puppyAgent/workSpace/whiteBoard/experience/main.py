#experiment.py

class Experiment:
    def __init__(self, experimentList:list = []):
        self._experimentList = experimentList

    # experimentList should be a list of experiment
    # experiment should be a string

    """
     experience = {
        "title": "title",
        "author": "author",
        "discription": "discription",
        "content": "content",
        "time": "time",
        "tag": "tag"
    }
    """

    @property
    def experimentList(self):
        return self._experimentList
    
    # get the experimentList
    def getExperimentList(self):
        return self._experimentList
    
    # adding new experiment
    def addExperiment(self, newExperiment:dict):
        self._experimentList.append(newExperiment)

    # delete experiment
    def deleteExperiment(self, experimentNum:int):
        self._experimentList.pop(experimentNum)

    # clear all experiments
    def clearExperiment(self):
        self._experimentList = []

    # get the experiment list as a prompt
    # NOTE: need to specify that every index should be involbed in the prompt, while the user can decide which one in True or False
    @property
    def experimentListPrompt(self):
        prompt = ""
        for i in range(len(self._experimentList)):
            prompt += str(i) + ". " + self._experimentList[i]["discription"] + "\n" + self._experimentList[i]["content"] + "\n"
        return prompt


        
