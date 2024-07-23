from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.pp.actions.explore import explore


def play(
    puppy_instance, 
    action_name: str, 
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

You default function is writing python code, it's good at any task that python packages can achieve. But make sure that you write code to import the given package.
You are also allowed to use the customized functions below, use them by just writing code as the example. the description shows how to use them. You are not allowed to call functions that out of the given range and python popular package:
{explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"])}

The current game map is ().
The block on your left is ().
The block on your right is ().
The block on your top is ().
The block on your bottom is ().
The tools you've taken are: ().
Now you write code to achieve your action(Note that the tools after@ is recommended tools, if it exists): {action_name}

For this action, you have already tried following code, but not finish yet. Think about it, You need to keep writing it.
maybe you should use a different function or try a new way to achieve the action, don't repeat the same code:
{puppy_instance.actionflow.current_action_code}

Try to understand the meaning of each function and its parameter, and decide the best function and use the function for this step to accomplish the action. 
You are only allowed to generate code that replace self.play(\"{action_name}\") part.

For example: (current actionflow: Go to the drawer and get the key.)
Response:
# To go to the drawer, I first got the location of the tool named drawer in the game map, it's in the (1,2) location to the agent.
# Move the agent 1 step to the right
move_agent(action='right', steps=1)
# Move the agent 2 steps to the upward
move_agent(action='up', steps=2)
# Take the tool
pick_up_tool()
# Use the tool
# Use the drawer tool to open the layers
all_layers = use_tool(tool_name='drawer', action_name='openlayers')
# all_layers now contains all the subtools inside, including the key.
all_layers = use_tool(tool_name='key', action_name='openlayers')

Now generate your answer as code: 
"""}]

    # Prompt Finished *****************************************************************************************

    action = Action(
        puppy_instance, 
        action_name, 
        model, 
        show_prompt, 
        show_response, 
        retries = 0
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
