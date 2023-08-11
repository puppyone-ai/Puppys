# workFlow.py

class Goal:
    def __init__(self, goal:str = "None"):
        self._goal = goal

    # get the goal
    @property
    def goal(self):
        return self._goal
    
    # get the goal
    def getGoal(self):
        return self._goal

    # set the goal
    @goal.setter
    def goal(self, newGoal:str):
        self._goal = newGoal

    # update the goal
    def updateGoal(self, newGoal:str):
        self._goal = newGoal