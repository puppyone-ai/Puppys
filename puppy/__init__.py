from puppy.thread.mainThread.thread import Thread


class Puppy:
    def __init__(self, name: str = ""):

        self.puppy_name = name

    def creat_thread(self, thread_name):

        # TODO: if thread_name is not a string, or not delivered, raise an error

        if not hasattr(self, thread_name):
            setattr(self, thread_name, Thread(puppy=self))

    def __getattribute__(self, attr: str):
        if attr in self.__dict__:
            target_thread = getattr(self, attr)
            return target_thread.parse_and_load

        raise AttributeError(f"{self.puppy_name} has no thread: {attr}")

    def run(self, thread_name):

        getattr(self, thread_name).run()


# if __name__ == "__main__":
#     Mei = Puppy(name='Mei')
#     # Mei.creat_thread('jump')
#     print(Mei.jump)
