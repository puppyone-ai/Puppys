from .base import ThreadBase
from puppy.thread.actionflow.actionflow import Actionflow
from contextlib import redirect_stdout, redirect_stderr

from puppy.tools.usable_tools import UsableTools
import threading


class Thread(ThreadBase):
    def __init__(self , decisiontree , goal='', print_mode='terminal', **kwargs):

        super().__init__()

        # naming the thread
        self.name = kwargs['name'] if 'name' in kwargs else "Default Thread"
        print(f'Created a thread as {self.name}! ')


        # add exec_environment for the thread
        self.global_var_dict = globals()
        self.runtime_vars_dict = {}
        self.runtime_vars_dict.update({'self': self})


        # cache print from exec_environment
        import io
        import sys

        self.output_buffer = sys.__stdout__
        self.error_buffer = sys.__stderr__

        if 'print_mode' in kwargs:
            if kwargs['print_mode'] == 'buffer':
                self.output_buffer = io.StringIO()
                self.error_buffer = io.StringIO()

        # set the env of actionflow
        self.actionflow = Actionflow(thread_instance=self)

        # set the env of tool_box
        self.tool_box = UsableTools(thread_instance=self)
        # load tools

        # set the env of the goal in the thread
        self.goal = ''

        # set the decisiontree
        self.decisiontree= decisiontree

    @property
    def vars_preview(self, characters_num=300):
        dict_temp = {}

        for key, value in self.runtime_vars_dict.items():
            string_data = str(value)
            preview_info = string_data[:characters_num]
            dict_temp.update({key: {"type: ": type(value), "preview:": preview_info}})

        return dict_temp

    # execute the code as the thread mode
    def thread_exec(self, code):
        # redirect the stdout and stderr to the buffer
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            exec(code, self.global_var_dict, self.runtime_vars_dict)


    def run(self) -> None:
        self.decisiontree(self)


def thread_run(Thread_list:list):
    threads = []

    # 为列表中的每个线程对象创建一个线程
    for Thread in Thread_list:
        thread = threading.Thread(target=Thread.run)  # 注意这里传递的是方法引用，不是方法调用
        thread.daemon = False
        threads.append(thread)
        thread.start()  # 启动线程

    # 等待所有线程完成
    for thread in threads:
        thread.join()
