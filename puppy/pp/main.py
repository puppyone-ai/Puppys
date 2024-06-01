from .base import PuppyBase
from puppy.pp.actionflow.actionflow import Actionflow
from contextlib import redirect_stdout, redirect_stderr
from puppy.llm.openAI import open_ai_chat
import os

from puppy.tools.usable_tools import UsableTools
import threading
import inspect
import textwrap

from puppy.pp.do_and_check import do_check, do, check



class Puppy(PuppyBase):
    def __init__(self , name ="default_puppy", decisiontree = None,  print_mode='terminal', **kwargs):

        super().__init__()

        self.name = name
        self.args = kwargs

        # add exec_environment for the pp
        self.global_var_dict = globals()
        self.runtime_vars_dict = {}
        self.runtime_vars_dict.update({'self': self})
        self.trigger = threading.Event()


        # cache print from exec_environment
        import io
        import sys

        self.output_buffer = sys.__stdout__
        self.error_buffer = sys.__stderr__

        if print_mode == 'buffer':
            self.output_buffer = io.StringIO()
            self.error_buffer = io.StringIO()

        # set the env of actionflow
        self.actionflow = Actionflow(thread_instance=self)

        # set the env of tool_box
        self.tool_box = UsableTools(thread_instance=self)
        # load tools

        # set the decisiontree
        self._decisiontree= decisiontree


    def decisiontree(self):
        return self._decisiontree(self, **self.args)

    @property
    def vars_preview(self, characters_num=300):
        dict_temp = {}

        for key, value in self.runtime_vars_dict.items():
            string_data = str(value)
            preview_info = string_data[:characters_num]
            dict_temp.update({key: {"type: ": type(value), "preview:": preview_info}})

        return dict_temp

    # execute the code as the pp mode
    def puppy_exec(self, code):
        # redirect the stdout and stderr to the buffer
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            # execute the code
            exec(code, self.global_var_dict, self.runtime_vars_dict)


    def run(self) -> None:

        # 获取函数的参数
        signature = inspect.signature(self._decisiontree)

        # 或者使用 getfullargspec 来获取更详细的参数信息
        args_spec = inspect.getfullargspec(self._decisiontree)

        # 获取函数的完整源代码
        full_source_code = inspect.getsource(self._decisiontree)

        # 去除第一行（函数定义行）
        source_code_without_def = '\n'.join(full_source_code.splitlines()[1:])

        # 使用 textwrap.dedent() 去除因为 def 引起的缩进
        dedented_source_code = textwrap.dedent(source_code_without_def)

        self.actionflow.all_code = dedented_source_code

        # set the env of tool_box
        self.tool_box = UsableTools(thread_instance=self)

        for tool in self.tool_box.default_tools:
            self.tool_box.load_tool(tool)


        self.decisiontree()


    def do_check(self, *args, **kwargs):
        return do_check(self, *args, **kwargs)

    def check(self, *args, **kwargs):
        return check(self, *args, **kwargs)

    def do(self, *args, **kwargs):
        return do(self, *args, **kwargs)


def puppy_run(Puppy_list:list):
    threads = []

    # 为列表中的每个线程对象创建一个线程
    for puppy in Puppy_list:
        thread = threading.Thread(target=puppy.run)  # 注意这里传递的是方法引用，不是方法调用
        thread.daemon = False
        threads.append(thread)
        thread.start()  # 启动线程

    # 等待所有线程完成
    for thread in threads:
        thread.join()

