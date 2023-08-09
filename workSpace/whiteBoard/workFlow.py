# workFlow.py

class WorkFlow:
    def __init__(self):
        self.workFlow = ["ok了家人们"]
        self.overallstepNum = 0
        self.finishedstepNum = 0
        self.remainingstepNum = 0


    def updateWorkFlow(self, newWorkFlow):
        self.workFlow = newWorkFlow

    def show(self):
        print("workFlow: ", self.workFlow)

    
