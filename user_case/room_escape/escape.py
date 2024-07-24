from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.llm.open_ai import open_ai_chat
from puppys.pp.actions.explore import explore


def escape(
    puppy_instance, 
    game_state: dict,
    target_usefulness: float,
    model: str = "gpt-4-turbo",
    show_prompt: bool = False,
    show_response: bool = False, 
    ) -> str:
    agent_x = game_state.get("agent_x")
    agent_y = game_state.get("agent_y")
    available_tools = game_state.get("available_tools")
    door_dict = game_state.get("door_dict")
    grid_string = game_state.get("grid_string")
    usefulness = game_state.get("usefulness")
    
    # print("game_state: ", game_state)
    # print("grid_string: ", grid_string)
    history_codes = "\n".join(puppy_instance.actionflow.history_codes)
    future_codes = "\n".join(puppy_instance.actionflow.future_codes)
    # print("history_codes: ", history_codes)
    # print("current_code: ", puppy_instance.actionflow.current_code)
    # print("future_codes: ", future_codes)

    prompt = [
        {"role": "system",
         "content": """
Objective: As an AI code agent, your goal is to help the agent escape the room by collecting tools with specific usefulness scores and using them to open the exit door. You need to write Python codes to achieve these.

1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
you can show your thinking and reason in the comment.
 For example: # Hello, I am an agent. 

2. Your code will be run immediately after you write it. If you assume any hypothetical function, the the system will crash. 

3. Your response cannot only be comment. You HAVE to write codes

4. Make sure that the parameter in your respond code follow the type of the parameter in the function instruction. 

5. About the Game:
- Grid: The room is represented as a grid (e.g., 5x5) with single objects per square: tools, a door, walls, or empty space. All other squares are empty and are the spaces for you (the agent) to move around.
- The grid will be provided in a descriptive string format, containing the dimension of the map grid (dimension=5 means the map is a 5 * 5 grid, 25 squares inside), and the object contained in each square (ONLY one object is allowed in one square and the empty square will not be described).
- Agent: You control the agent who can move around to collect tools and navigate towards the exit door.
- Tools: Each tool has a name, description, and usefulness score. Tools can be collected by moving the agent onto their respective squares.

6. About the movement:
- The tools are only available to use if the agent (you) has moved to the square where the tool is located, meaning that the agent picked up the tool. Otherwise, the agent can only know the existence of the tool but cannot use it.
- Note that, if the tool is on the left of 1 step to the agent, but the agent go left for 2 steps, the game will consider the agent has ignored the tool, just normal movement, not picking up the tool.

7. Rules for Escaping (win/end the game):
- Collect tools to reach or exactly match a given target usefulness score. Can use one tool that matches the target score or multiple tools to sum up to the target score.
- The escape is successful when the agent is adjacent to the exit door and the sum of collected tool scores matches the target score.

7. Game Mechanics:
    1. Analyze the Current State:
    - Compare the current usefulness score with the target usefulness score to determine how much more usefulness is needed.
    - Identify which tools are still available on the grid that can help achieve the remaining usefulness score.

    2. Planning and Movement:
    - Plan a route to move towards the target tools based on their locations on the grid.
    - Navigate the grid by calculating the optimal steps and direction to reach each tool without skipping them.

    3. Tool Collection and Door Opening:
    - Collect tools by moving onto their grid positions.
    - Once the target usefulness is met or exceeded, plan a route to the door.
    - Use the collected tools to try opening the door if adjacent to it.

8. Additional Notes:
- Ensure that movements are planned so that the agent lands exactly on the tool to pick it up; overshooting will result in just moving past the tool.
- If multiple useful tools are aligned in one direction, plan consecutive moves in that direction to collect them sequentially without additional commands.
- The game HAS TO be played in multiple rounds, so make sure you write the code for the next step ONLY, the rest steps can be performed in the following rounds.

Ensure each part of your response contains Python code actions for the next step, following the example provided, with concise and clear logic comments embedded in the code.
Your response should be similar with the following example(ONLY CODE) and NOTHING ELSE.
"""},
        # 2. Provide the current var and usable tools
        {"role": "user",
         "content": f"""
Your formally-defined parameters and their previewing are as follows: 
{puppy_instance.puppy_vars.preview()}

The historical codes are: {history_codes}
The current code: {puppy_instance.actionflow.current_code}
The future codes are: {future_codes}
Note: The future codes are for referencing the next steps, you DO NOT need to write code and replace them!

Check if the undefined or unspecific variables are in the above preview and historical codes, if so, use them when needed in your code.

Your default function is writing python dictionaries.
You are also allowed to use the customized functions below, use them by just writing code as the example. the description shows how to use them. You are not allowed to call functions that out of the given range and python popular package:
{explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"])}

The current game map: {grid_string}.

The agent's current location is: ({agent_x}, {agent_y}).
The door status is: {door_dict}.
The tools you've taken are: {available_tools}.
The target usefulness score is: {target_usefulness}.
The current usefulness score is: {usefulness}.

You are only allowed to generate code that replace self.escape(...) part, write code to control the agent to escape the room for the next step ONLY.


# Examples on planning the route to reach a target object:
- Example 1: Navigate to collect the 'Key'
  - Grid situation: The agent is at (1, 2) (row 1, column 2), and the 'Key' is at (4, 3) (row 4, column 3) with a usefulness score of 1.
  - Planned Route: Move down 3 steps, then right 1 step.
  - Command: `move_agent(direction="down", step=3)`, followed by `move_agent(direction="right", step=1)`.

- Example 2: Navigate to use the 'Key' at the door
  - Grid situation: The agent, now with the 'Key', is at (4, 3) (row 4, column 3), and the door is at (0, 1) (row 0, column 1).
  - Planned Route: Move up 4 steps, then left 2 steps.
  - Command: `move_agent(direction="up", step=4)`, followed by `move_agent(direction="left", step=2)`.

- Example 3: Immediate tool collection
  - Grid situation: The agent is at (1, 2) (row 1, column 2), and the 'Hammer' is directly left at (1, 1) (row 1, column 1) with a usefulness score of 0.5.
  - Planned Route: Move left 1 step to collect the 'Hammer'.
  - Command: `move_agent(direction="left", step=1)`.


# Example codes for using the tool:
## Use the tool 'Key' to open the door with the target usefulness score 1
use_tool(tool_name='Key', target_usefulness=1)

## Use the tool 'Hammer' to open the door with the target usefulness score 0.5
use_tool(tool_name='Hammer', target_usefulness=0.5)

## Use all the tools available
available_tools = get_all_available_tools(connection)
for tool_name in available_tools:
    use_tool(tool_name=tool_name, target_usefulness=self.target_usefulness)

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
        action_type="escape",
        prompt=prompt,
        prompt_action="escaping"
    )
    
    new_code = open_ai_chat(
        prompt=prompt, 
        model=model, 
        printing=show_response, 
        stream=True
    )

    new_code = action.clean_llm_code(new_code, add_code=True)

    action.replace_action_code(new_code)
    
    # Run the code
    try:
        return action.run_without_errors(new_code)

    # Handle errors
    except Exception as e:
        error_details = action.run_with_errors(e)
        print(error_details)

