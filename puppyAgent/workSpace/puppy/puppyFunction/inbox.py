class Inbox:
    def __init__(self, initialUnReadList=None, callback=None):
        self.unReadList = initialUnReadList or []
        self.callback = callback

        # define the unread list, in processing list and the read list
        self.unReadList=[]
        self.processingList=[]
        self.finishedList=[]

    # run the inbox
    def run(self):
        for message in self.unReadList:
            self.Execute(message)

    # unfinished
    # use the CALL FUNCTION in the actionLib to execute the message
    def Execute(self, message):
        pass

    # add a new message to the inbox
    def append(self, item):
        self.unReadList.append(item)
        self.run()

    # remove a message from the inbox
    def remove(self, item):
        self.unReadList.remove(item)
        self.run()

    # get the message in the inbox
    def get(self):
        return self.unReadList, self.processingList, self.finishedList

    def __str__(self):
        return str(self.unReadList)

    def __repr__(self):
        return repr(self.unReadList)

# 示例使用
def my_callback(updated_data):
    print(f"数组已更新: {updated_data}")

lst = Inbox(callback=my_callback)
lst.append(1)  # 输出: 数组已更新: [1]
lst.append(2)  # 输出: 数组已更新: [1, 2]
lst.remove(1)  # 输出: 数组已更新: [2]