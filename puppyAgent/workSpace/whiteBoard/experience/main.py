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
    # NOTE make sure the newExperiment is a dictionary, and the user filled all the elements
    def addExperiment(self, newExperiment:dict):
        self._experimentList.append(newExperiment)

    # delete experiment
    def deleteExperiment(self, experimentNum:int):
        self._experimentList.pop(experimentNum)

    # clear all experiments
    def clearExperiment(self):
        self._experimentList = []

    # get the experiment list as a prompt (default mode)
    @property
    def experimentListPrompt(self):
        elements = ["title", "author", "discription", "content", "time", "tag"]
        
        prompt = ""
        for i in range(len(self._experimentList)):
            prompt += str(i) + ". "
            for elem in elements:
                prompt += self._experimentList[i][elem] + "\n"
        return prompt

    # get the experiment list as a prompt (user's mode)
    def getExperimentListPrompt(self, elements=None):
        # if user does not specify the elements, then use the default elements
        if elements == None:
            elements = ["title", "author", "discription", "content", "time", "tag"]
        
        prompt = ""
        for i in range(len(self._experimentList)):
            prompt += str(i) + ". "
            for elem in elements:
                prompt += self._experimentList[i][elem] + "\n"
        return prompt


        
