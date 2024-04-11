from .base import ThreadBase


class Actions:
    def __init__(self, **kwargs):

        if "thread_instance" in kwargs:
            thread_instance = kwargs["thread_instance"]
            self.thread_instance = thread_instance

        self.name = ""
        self.status = ""
        self.code = ""

        # could consider introduce the func_name indexing in the future
    def __str__(self):
        return f'{self.name} : {self.status} /n {self.code}'

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)


# TODO: abstract the parser to convert the source code to diverse properties
def parse_func_code(source_code: str, thread_instance: ThreadBase = None) -> []:

    """
    Load the action from source code so that we could trigger it in actionflow
    """

    # clean source code

    lines = source_code.split('\n')

    striped_lines = []

    for line in lines[2:]:  # [2:]filter decorator and function name
        line = line.strip()
        if line:
            striped_lines.append(line)

    # print('striped_lines:')
    # print(striped_lines)

    # load source code to action list sequentially

    actions_list = []

    for line in striped_lines:

        if '##' in line:
            if thread_instance:
                actions_list.append(Actions(thread_instance=thread_instance))
            else:
                actions_list.append(Actions())

            actions_list[-1]["name"] = line.split('##', 1)[1].strip()
            actions_list[-1]["code"] += f'{line}\n'

        else:

            actions_list[-1]["code"] += line + '\n'

    for actions in actions_list:
        _check_status(actions)

    return actions_list


# verify the status of the action
def _check_status(actions) -> None:

        if ".do()" in actions["code"]:

            if not actions["name"]:
                actions["status"] = "changeable"
            else:
                actions["status"] = "semi-fixed"

        else:
            actions["status"] = "fixed"
