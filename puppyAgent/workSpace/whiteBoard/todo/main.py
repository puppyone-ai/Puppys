# -*- coding: utf-8 -*-
# @Time : 2023/8/23
# @Author : Guanqun Mu


class Todo:
    def __init__(self, todoList:dict = {}):
        self._todoList = todoList

    # the todoList is a dictionary with:
    """
    todoList={
        value: {"name": "value",
        discription: "discription"
        status: "planed"/ "running"/ "finished"
        }"""

    # get the todoList
    @property
    def todoList(self):
        return self._todoList
    
    # get the todoList
    def getTodoList(self):
        return self._todoList

    # add a new todo
    def add(self, name, value, description="", status=""):
        self._items[name] = self.Item(value, description, status)

    # remove a todo
    def remove(self, name):
        if name in self._items:
            del self._items[name]

    # the class of each todo item
    class Item:
        def __init__(self, value, description, status):
            self.value = value
            self.description = description
            self.status = status
        
        # start to run the todo item
        def run(self, func1):
            return func1(self)

        # pulse the todo item
        def pulse(self):
            # 为简单起见，这里只是返回一个标记字符串，您可以根据需要定制此方法
            return f"Pulse for {self.value}"

        # end the todo item
        def end(self):
            # 同样为了简单起见，这里只是返回一个标记字符串
            return f"End of {self.value}"


    # delete a todo
    def deleteTodoByIndex(self, index:int):
        self._todoList.pop(index)