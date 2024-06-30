from contextlib import redirect_stdout, redirect_stderr

import threading
import inspect
import textwrap

from .actions import explore
from puppy.env import Env, FuncEnv
from puppy.pp.actions.load_env import load_env
from puppy.pp.default_env.actionflow import Actionflow
from puppy.pp.default_env.puppy_vars import PuppyVars


class Puppy(Env):

    def __init__(self, value, *args,  printing_mode='terminal',  **kwargs):

        super().__init__(*args, **kwargs)

        self.name = "default_puppy"

        self.actionflow = Actionflow(self, function=value, printing_mode=printing_mode)

        self.puppy_vars = PuppyVars(self, global_dict=globals())

        self.env_node = self

    def explore(self, *args, **kwargs):
        return explore(self, *args, **kwargs)

    def load_env(self, *args, **kwargs):
        return load_env(self, *args, **kwargs)

    def run(self, **kwargs) -> None:

        # run the actionflow
        return self.actionflow.run(**kwargs)



def puppy_run(puppy_list: list):
    threads = []

    # 为列表中的每个线程对象创建一个线程
    for puppy in puppy_list:
        thread = threading.Thread(target=puppy.run)  # 注意这里传递的是方法引用，不是方法调用
        thread.daemon = False
        threads.append(thread)
        thread.start()  # 启动线程

    # 等待所有线程完成
    for thread in threads:
        thread.join()

