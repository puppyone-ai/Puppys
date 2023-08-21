# workFlow.py

class Todo:
    def __init__(self, todoList:list = []):
        self._todoList = todoList

    # get the todoList
    @property
    def todoList(self):
        return self._todoList
    
    # get the todoList
    def getTodoList(self):
        return self._todoList

    # add a new todo
    def addTodo(self, newTodo:str):
        self._todoList.append(newTodo)

    # delete a todo
    def deleteTodoByIndex(self, index:int):
        self._todoList.pop(index)