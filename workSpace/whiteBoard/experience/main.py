#experiment.py

class Experiment:
    def __init__(self, experimentList:list = []):
        self._experimentList = experimentList

    # experimentList should be a list of experiment
    # experiment should be a string

    """
     experience = {
        "title": "title",
        "discription": "discription",
        "author": "author",
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

        
