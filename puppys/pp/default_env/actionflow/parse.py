import ast
import os
import re

from puppys.llm.open_ai import open_ai_chat


def replace_formatted_strings(line: str, local_vars: dict) -> str:
    """
    Replace formatted parts of the string with actual values from local_vars.
    """
    pattern = re.compile(r'\{(.*?)\}')
    matches = pattern.findall(line)
    
    for match in matches:
        if match in local_vars:
            line = line.replace(f'{{{match}}}', str(local_vars[match]))
    return line


def replace_function_arguments(line: str, local_vars: dict) -> str:
    """
    Replace function arguments in the line with actual values from local_vars.
    """
    # Parse the line into an AST
    tree = ast.parse(line, mode='exec')
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            for idx, arg in enumerate(node.args):
                if isinstance(arg, ast.Name) and arg.id in local_vars:
                    node.args[idx] = ast.Constant(value=local_vars[arg.id], kind=None)

    # Unparse the modified AST back into a string
    new_line = ast.unparse(tree)
    return new_line


def parse_code2str(source_code: str, local_vars: dict) -> list:
    """
    Parse the source code and extract the function body code.

    Args:
        source_code (str): The source code to parse.

    Returns:
        str: The function body code.

    """
    # Replace formatted strings with actual values from local_vars
    replaced_code = replace_formatted_strings(source_code, local_vars)
    
    # Split the source code into lines and keep the line endings
    lines = replaced_code.splitlines(keepends=True)

    # Find the first non-empty line and get its indentation
    first_non_empty_line = next(line for line in lines if line.strip())
    min_indent = len(re.match(r"^\s*", first_non_empty_line).group())

    # Remove the minimum indentation from each line
    adjusted_lines = [line[min_indent:] if len(line.strip()) > 0 else line for line in lines]

    # Recombine the adjusted lines
    adjusted_source_code = ''.join(adjusted_lines)

    # Parse the adjusted source code into an AST
    tree = ast.parse(adjusted_source_code)
    
    function_body_code = []
    # Walk through the AST and extract the function body code
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for body_node in node.body:
                # Convert each statement to source code and append to the result
                body_code_block = ast.unparse(body_node)
                body_code_block = body_code_block + "\n" if not body_code_block.endswith("\n") else body_code_block
                function_body_code.append(body_code_block)

    return function_body_code


def code_segment_json(code):
    """
    Parse the input code to extract the first layer's code units.

    Args:
        code (str): The code to parse.

    Returns:
        list: A list of dictionaries containing the type and code snippet for each code unit in the first layer.
    """
    # Parse the code to AST
    parsed_code = ast.parse(code)

    # Initialize an empty list to store the first layer's code units
    first_layer_code = []

    # Iterate through the nodes in the parsed code
    for node in parsed_code.body:
        # Get the type of the node
        node_type = type(node).__name__

        # Get the code snippet of the node
        code_snippet = ast.unparse(node)

        # Create a dictionary with the type and code of the node
        code_unit = {"type": node_type, "code": code_snippet}

        # Add the code unit to the list
        first_layer_code.append(code_unit)

    return first_layer_code


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
                    puppys.do()
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
                    puppys.do()"}
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
                          model=os.environ["OPENAI_MODEL"],
                          temperature=0.3,
                          api_key=os.environ["OPENAI_API_KEY"],
                          max_tokens=4096,
                          printing=True, stream=True)

    medium = eval(medium)  # [{"name":action1.name,"code":action1.code},{"name":action2.name,"code":action2.code},...]

    action_list = []

    for action in medium:
        #action_list.append(Action())
        action_list[-1].name = action["name"]
        action_list[-1].code = action["code"]

    for action in action_list:
        print(action.code)
        _check_status(action)

    return action_list


# TODO: abstract the parser to convert the source code to diverse properties
def parse_code2list(source_code: str) -> list:
    """
    Load the action from source code so that we could trigger it in default_env
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

            #action_list.append(Action())
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


if __name__ == '__main__':
    code = """
import random
num = 3
if random.randint(1, 100) < 10:
    num = 10
def ok():
    pass
self.do_check('choose a number from 0 to 10, and send the number to me', show_response=True)
self.do_check('go to the given url, show the HTML', show_response=True)
self.do_check('show the top 10 news @llm, and send it to me', show_response=True, show_prompt=True)
self.do_check('pick the news that related to Large Language Models, summarize all the news, and send it to me')
"""

    # Extract the desired segments from the parsed AST
    json_segments = code_segment_json(code)
    print(json_segments)
