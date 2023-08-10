# workFlow.py

class WorkFlow:
    def __init__(self, workFlow= [None], overallstepNum=None, finishedstepNum=None, remainingstepNum=None):
        self._workFlow = workFlow
        self._overallstepNum = overallstepNum
        self._finishedstepNum = finishedstepNum
        self._remainingstepNum = remainingstepNum

    # get the workFlow and related information
    @property
    def workFlow(self):
        return self._workFlow
    
    @property
    def overallstepNum(self):
        return self._overallstepNum
    
    @property
    def finishedstepNum(self):
        return self._finishedstepNum
    
    @property
    def remainingstepNum(self):
        return self._remainingstepNum

    @workFlow.setter
    # set the workFlow
    def workFlow(self, newWorkFlow):
        self._workFlow = newWorkFlow


    # update the workFlow
    def updateTask(self, newTask:str, xnum:int, ynum:int):
        self._workFlow[xnum][ynum] = newTask


