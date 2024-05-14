from puppy.thread.actionflow.action import Action
import textwrap


# TODO: abstract the parser to convert the source code to diverse properties
def parse_code2list(source_code: str) -> list:

    """
    Load the action from source code so that we could trigger it in actionflow
    """

    # clean source code

    # clean source code
    lines = source_code.split('\n')
    striped_lines = []

    for line in lines[2:]:  # [2:] filter decorator and function name
        if line.strip():
            striped_lines.append(line)

    # load source code to action list sequentially
    import textwrap

    action_list = []
    current_indent = 0

    for line in striped_lines:
        if '##' in line:
            # Calculate the current line's indentation
            current_indent = len(line) - len(line.lstrip())

            action_list.append(Action())
            action_list[-1].name = line.split('##', 1)[1].strip()
            action_list[-1].code += f'{line.lstrip()}\n'
        else:
            # Remove the current indent from the line
            line_without_indent = line[current_indent:] if line.startswith(' ' * current_indent) else line.lstrip()
            action_list[-1].code += line_without_indent + '\n'

    for action in action_list:
        print(action.code)
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
