from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.pp.actions.explore import explore


def escape(
    puppy_instance, 
    grid_string: str, 
    available_tools: str, 
    target_usefulness: float,
    model: str = "gpt-4-turbo",
    show_prompt: bool = False, 
    show_response: bool = False, 
    ) -> str:
    prompt = [
        {"role": "system",
         "content": """
You are an AI code agent playing the game 'room escape'.

1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
you can show your thinking and reason in the comment.
 For example: # Hello, I am an agent. 

2. Your code will be run immediately after you write it. If you assume any hypothetical function, the the system will crash. 

3. Your response cannot only be comment. You HAVE to write codes

4. Make sure that the parameter in your respond code follow the type of the parameter in the function instruction. 

5. Your ultimate goal is to escape the room by writing code to achieve the action. 
 The game map will be provided, in the map, the agent (you) is represented as 'A'; the available tools that could help escape the room are represented as 'T'; the exit door is represented as 'D'; the walls are represented as 'W'; the empty space is represented as ''.
 The available tools are either useful or confusing, you need to figure out which tool is useful and which is not.
 Each tool has a specific name, description, use guide, and a set of actions and action results.
 You HAVE TO analysis those information and decide which tool to use and how to use it to escape the room.
 The game will be finished when you reach the exit door 'D' and successfully opened it.
 All your actions will be recorded, you can check the history to help you decide the next action.
 All the actions, including the movements, take the tool, use the tool, are encapsulated in python functions, you just need to write python code to call them and process the return results.

 Your response should be similar with the following example(ONLY CODE) and NOTHING ELSE.
"""},
        # 2. Provide the current var and usable tools
        {"role": "user",
         "content": f"""
Your formally-defined parameters and their previewing are as follows: 
{puppy_instance.puppy_vars.preview()}

Your default function is writing python dictionaries.
You are also allowed to use the customized functions below, use them by just writing code as the example. the description shows how to use them. You are not allowed to call functions that out of the given range and python popular package:
{explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"])}

The current game map: {grid_string}.
The tools you've taken are: {available_tools}.
The target usefulness score is: {target_usefulness}.
Now, write code to control the agent to escape the room for the next step ONLY.

You are only allowed to generate code that replace self.escape(...) part.

The code you generate CAN ONLY BE PYTHON DICTIONARY!
The dictionary MUST contains the fields:
 - 'direction' (str value): The direction to move the agent. The value should be one of 'up', 'down', 'left', 'right', NO CAPITALIZATION, and NO OTHER VALUES! It's a re1quired field.
 - 'step' (int value): The steps to move the agent. The value should be an positive integer, and NO OTHER VALUES! It's a required field.
 - 'use_tool' (str value): The name of the tool to use. The value should be one of the tools you've taken, and NO OTHER VALUES! It's a required field, if you don't want to use any tool, just set it to an empty string.

If you don't want to move the agent, just set the 'direction' to an empty string, and set the 'step' to 0.

Dictionary Format:
{{
    'direction': 'up',
    'step': 1,
    'use_tool': 'key'
}}

You MUST use an variable named 'escape_dict' to store the dictionary.
Always write code as the following template:
escape_dict = {{
    'direction': '<direction to replace>',
    'step': <step to replace>,
    'use_tool': '<tool name to replace>'
}}

Examples:
# Based on the current game map, the agent should move up for 1 step and use the tool key.
escape_dict = {{
    'direction': 'up',
    'step': 1,
    'use_tool': 'key'
}}

# Based on the current game map, the agent should move right for 2 steps and not using any tools.
escape_dict = {{
    'direction': 'right',
    'step': 2,
    'use_tool': ''
}}

# Based on the current game map, the agent should not move and use the tool hammer.
escape_dict = {{
    'direction': '',
    'step': 0,
    'use_tool': 'hammer'
}}

# Based on the current game map, the agent should move down for 3 step, not picking up any tool, ignore the tool 'toy' 1 step downwards, as the this tool is useless.
escape_dict = {{
    'direction': 'down',
    'step': 3,
    'use_tool': ''
}}


Now, write your code to control the agent to escape the room for the next step ONLY:
"""}]

    # Prompt Finished *****************************************************************************************

    action = Action(
        puppy_instance, 
        action_name="", 
        model=model,
        show_prompt=show_prompt, 
        show_response=show_response, 
        retries=0
    )

    action.highlighting(
        action_type="playing_action", 
        prompt=prompt, 
        prompt_action="playing"
    )

    new_code = action.llm_api_call(prompt)

    new_code = action.clean_llm_code(new_code, add_code=True)

    puppy_instance = action.get_puppy_instance()

    # Run the code
    return action.run_without_errors(new_code)
