# __init__.py
import workFlow


# get what's on the whiteBoard
def getGoal():
    return workFlow.WorkFlow.goal

def getWorkFlow():
    return workFlow.WorkFlow.workFlow




# broadcast what's on the white board to all peoples and puppy agents
def boardCast():
    pass


if __name__ == "__main__":
    print(getWorkFlow())
    workFlow.WorkFlow.updateWorkFlow("ok")
