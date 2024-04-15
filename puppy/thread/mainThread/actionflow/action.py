

from puppy.thread.mainThread.base import ThreadBase


class Action:
    def __init__(self, **kwargs):

        if "thread_instance" in kwargs:
            thread_instance = kwargs["thread_instance"]
            self.thread_instance = thread_instance

        self.name = ""
        self.code = ""
        self.status = ""

        # could consider introduce the func_name indexing in the future
    def __str__(self):
        return f'({self.status}){self.name}'

    def __call__(self, *args, **kwargs):
        overall_dict = {"name": self.name,
                        "code": self.code,
                        "status": self.status}

        return overall_dict


# TODO: abstract the parser to convert the source code to diverse properties
def parse_code2list(source_code: str, thread_instance: ThreadBase = None) -> []:

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

    action_list = []

    for line in striped_lines:

        if '##' in line:
            if thread_instance:
                action_list.append(Action(thread_instance=thread_instance))
            else:
                action_list.append(Action())

            action_list[-1].name = line.split('##', 1)[1].strip()
            action_list[-1].code += f'{line}\n'

        else:

            action_list[-1].code += line + '\n'

    for action in action_list:
        _check_status(action)

    return action_list


# verify the status of the action
def _check_status(action) -> None:

    if ".do()" in action.code:

        if not action.code:
            action.status = "changeable"
        else:
            action.status = "semi-fixed"

    else:
        action.status = "fixed"
