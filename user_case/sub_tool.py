from puppy.pp.main import Puppy
from puppy.pp.actions import do_check, check, do
from puppy.env.func_env import FuncEnv
from puppy.pp.actions.load_env import load_env, unload_env

class Test_Agent(Puppy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Mei"
        self.description = "A puppy that could help to intelligent your code"
        self.version = "0.0.1"

    def do_check(self, *args, **kwargs):
        return do_check(self, *args, **kwargs)

    def check(self, *args, **kwargs):
        return check(self, *args, **kwargs)

    def do(self, *args, **kwargs):
        return do(self, *args, **kwargs)


def test_sub_tool_decesiontree(self):
    self.do("create a block of a database that contains the number of 12345678", show_response=True)


Test_Agent=Test_Agent(value=test_sub_tool_decesiontree)

def create_block(puppy_instance, query):
    puppy_instance.env_node=puppy_instance.tool_create
    load_env(puppy_instance=puppy_instance, env_node=puppy_instance.tool_create)
    unload_env(puppy_instance=puppy_instance, env_node=puppy_instance)
    puppy_instance.do(query, show_response=True, show_prompt=True)

def create_block_todo(puppy_instance, query):
    puppy_instance.env_node=puppy_instance.tool_create.create_type_todo
    print("create_block_todo completed for", query)

def create_block_table(puppy_instance, query):
    puppy_instance.env_node = puppy_instance.tool_create.create_type_table
    print("create_block_table completed for", query)

def delete_block(puppy_instance, query):
    puppy_instance.env_node = puppy_instance.delete_block
    print("delete_block completed for", query)


Test_Agent.tool_create=FuncEnv(name="create_block",
                                 description="create a block, for example: create_block(query='create a block that can XXX') ",
                                 value=create_block,
                                 fixed_params={"puppy_instance": Test_Agent},
                               free_params=["query"])

Test_Agent.tool_create.create_type_todo=FuncEnv(name="create_type_todo",
                                                description="create a block type of todo, for example usage: create_block_todo(query=XXX)",
                                                value=create_block_todo,
                                                fixed_params={"puppy_instance": Test_Agent},
                                                free_params=["query"])

Test_Agent.tool_create.create_type_table=FuncEnv(name="create_type_table",
                                                description="create a block type of table, for example usage: create_block_table(query=XXX)",
                                                value=create_block_table,
                                                fixed_params={"puppy_instance": Test_Agent},
                                                 free_params=["query"])

Test_Agent.tool_delete=FuncEnv(name="delete_block",
                                 description="delete a block",
                                 value=delete_block,
                                 fixed_params={"puppy_instance": Test_Agent},
                                free_params=["query"])


Test_Agent.run()