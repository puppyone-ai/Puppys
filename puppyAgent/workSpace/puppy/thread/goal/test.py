class GoalThread:
    def goalThread(self, func):
        def wrapper(*args, **kwargs):
            print("Before goalThread")
            result = func(*args, **kwargs)
            print("After goalThread")
            return result
        return wrapper

class CodeThread:
    def codeThread(self, func):
        def wrapper(*args, **kwargs):
            print("Before codeThread")
            result = func(*args, **kwargs)
            print("After codeThread")
            return result
        return wrapper

class puppy:
    def __init__(self):
        self.goal_thread = GoalThread()
        self.code_thread = CodeThread()

    @property
    def goalThread(self):
        return self.goal_thread.goalThread

    @property
    def codeThread(self):
        return self.code_thread.codeThread

    def do(self):
        # Implement the logic that should be triggered by 'do'
        print("Doing something...")

    def run(self):
        # Implement the logic that should be run
        print("Running...")

# 使用示例
Yuning = puppy()

@Yuning.codeThread
def action():
    print("action")

def trigger():
    Yuning.do()

@Yuning.goalThread
def setGoal(goal):
    print(f"You are a {goal}")

Yuning.run()
