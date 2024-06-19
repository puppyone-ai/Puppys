from contextlib import redirect_stdout, redirect_stderr

import threading
import inspect
import textwrap

from .actions import explore
from puppy.env import Env, FuncEnv


class Puppy(Env):

    def __init__(self, *args,  print_mode='terminal', **kwargs):

        super().__init__(*args, **kwargs)

        self.name = "default_puppy"

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

        # set the decisiontree
        self._decisiontree = self.value

        self.all_code = ""
        self.current_code = ""

    def decisiontree(self):
        return self._decisiontree(self
                                  # , **self.args
                                  )

    @staticmethod
    def explore(*args, **kwargs):
        return explore(*args, **kwargs)

    @property
    def vars_preview(self, characters_num=300):

        dict_temp = {}

        for key, value in self.runtime_vars_dict.items():
            string_data = str(value)
            preview_info = string_data[:characters_num]
            dict_temp.update({key: {"type": type(value), "preview": preview_info}})

        return dict_temp

    # execute the code as the pp mode
    def puppy_exec(self, code):

        # redirect the stdout and stderr to the buffer
        with redirect_stdout(self.output_buffer), redirect_stderr(self.error_buffer):
            local_vars = locals()

            self.runtime_vars_dict.update(local_vars)

            # execute the code
            exec(code, self.global_var_dict, self.runtime_vars_dict)

    def run(self) -> None:

        tools_dict = explore(self, target=FuncEnv, sub_only=True)

        self.runtime_vars_dict.update(tools_dict)

        # 获取函数的参数
        signature = inspect.signature(self._decisiontree)

        # 或者使用 getfullargspec 来获取更详细的参数信息
        args_spec = inspect.getfullargspec(self._decisiontree)

        # 获取函数的完整源代码
        full_source_code = inspect.getsource(self._decisiontree)

        # 去除第一行（函数定义行）
        source_code_without_def = '\n'.join(full_source_code.splitlines()[1:])

        # 使用 textwrap.dedent() 去除因为 def 引起的缩进
        dedent_source_code = textwrap.dedent(source_code_without_def)

        self.all_code = dedent_source_code

        self.decisiontree()

    # def puppy_env_update(self, vars_dict):
    #     self.runtime_vars_dict.update(vars_dict)


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

