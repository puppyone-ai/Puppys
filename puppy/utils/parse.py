from puppy.pp.actionflow.action import Action
import textwrap

import json
from puppy.llm.openAI import open_ai_chat
from openai import OpenAI


# soft decoder
def parse_code2list2(source_code: str) -> list:
    """
    Load the action from source code through LLM

    input: source_code
    output: list
    """

    prompt = [
        # 1.define the type of this agent
        {
            "role": "system",
            "content": """
            You are a helpful assistant designed to output python list composed of serval python dictionary objects such as [{"name":"You","code":"print"}, {"name":"Me","code":"print"}].
            """
        },

        # 2.provide examples
        {
            "role": "system",
            "content": """
            You are provided an example as belows:
            <example>:
            User's input:
            ## welcome the User
            print("Hello, can I help you?\n")


            ## give user your identity
            for i in range(5):
                print("I am AI\n")
                for i in range(5):
                    puppy.do()
            "

            your output:
            [
            {"name":"welcome the User",
            "code":
            "## welcome the User
             print("Hello, can I help you?\n")"},
            {"name":"give user your identity",
            "code":
            "## give user your identity
             for i in range(5):
                print("I am AI\n")
                for i in range(5):
                    puppy.do()"}
            ]
            </example>
            """
        },

        # 3.tell llm to output
        {
            "role": "user",
            "content": source_code
        }

    ]

    medium = open_ai_chat(prompt=prompt,
                          model="gpt-4-turbo",
                          temperature=0.3,
                          api_key=os.environ["OPENAI_API_KEY"],
                          max_tokens=4096,
                          printing=True, stream=True)

    medium = eval(medium)  # [{"name":action1.name,"code":action1.code},{"name":action2.name,"code":action2.code},...]

    action_list = []

    for action in medium:
        action_list.append(Action())
        action_list[-1].name = action["name"]
        action_list[-1].code = action["code"]

    for action in action_list:
        print(action.code)
        _check_status(action)

    return action_list

# TODO: abstract the parser to convert the source code to diverse properties
def parse_code2list(source_code: str) -> list:

    """
    Load the action from source code so that we could trigger it in actionflow
    """

    # clean source code
    lines = source_code.split('\n')
    striped_lines = []

    for line in lines[2:]:  # [2:] filter decorator and function name
        if line.strip():
            striped_lines.append(line)

    # load source code to action list sequentially

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
        _check_status(action)

    return action_list


# verify the status of the action
def _check_status(action) -> None:

    if ".do()" in action.do:

        if not action.do:
            action.status = "changeable"
        else:
            action.status = "semi-fixed"

    else:
        action.status = "fixed"
