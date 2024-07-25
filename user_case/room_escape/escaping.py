from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.llm.open_ai import open_ai_chat
from puppys.pp.actions.explore import explore


def escaping(
    puppy_instance, 
    game_state: dict,
    target_usefulness: float,
    model: str = "gpt-4-turbo",
    # model: str = "gpt-4o",
    show_prompt: bool = False,
    show_response: bool = False, 
    ) -> str:
    agent_x = game_state.get("agent_x")
    agent_y = game_state.get("agent_y")
    available_tools = game_state.get("available_tools")
    door_dict = game_state.get("door_dict")
    grid_string = game_state.get("grid_string")
    usefulness = game_state.get("usefulness")

    history_codes = "\n".join(puppy_instance.actionflow.history_codes)
    # print("history_codes: ", history_codes)
    

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
- The grid will be provided in a descriptive string format, containing the dimension of the map grid (dimension=5 means the map is a 5 * 5 grid, 25 squares inside), and the object contained in each square (the empty square will not be described).
- Agent: You control the agent who can move around to collect tools and navigate towards the exit door.
- Tools: Each tool has a name, description, and usefulness score. Tools can be collected by moving the agent onto their respective squares.

6. About the movement:
- The tools are only available to use if the agent (you) has moved to the square where the tool is located, meaning that the agent picked up the tool. Otherwise, the agent won't be able to use it.
- Note: If the tool is on the left of 1 step to the agent, but the agent go left for 2 steps, the game will consider the agent has ignored the tool.

7. Rules for Escaping (win/end the game):
- Collect tools to reach or exactly match a given target usefulness score. Can use one tool that matches the target score or multiple tools to sum up to the target score.
- If the usefulness score has exceeded the target score, the agent can give up using some tools to decrease the usefulness.
- The escape is successful when the agent is standing in the same location as the door.

8. Game Mechanics:
    1. Analyze the Current State:
    - Compare the current usefulness score with the target usefulness score to determine how much more usefulness is needed and which tools are needed to be the best choice.
    - Identify which tools are still available on the grid that can help achieve the remaining usefulness score.
    - e.g. current tools are 1, the target is 1.3, there is another tool with 0.1, the agent can collect that tool and use it 3 times.

    2. Planning and Movement:
    - Plan a route to move towards the target tools based on their locations on the grid.
    - Navigate the grid by calculating the optimal steps and direction to reach each tool without skipping them.

    3. Tool Collection and Escape Successfully:
    - Collect tools by moving onto their grid positions.
    - Once the target usefulness is met, plan a route to the square adjacent to the door.
    - Use the collected tools to escape.

9. Additional Notes:
- If multiple useful tools are aligned in one direction, plan consecutive moves in that direction to collect them sequentially without additional commands.
- The game HAS TO be played in multiple rounds, so make sure you write the code for the next step ONLY, the rest steps can be performed in the following rounds.
- The agent CANNOT stand on or move over the wall, instead, plan the route to avoid the wall. Movements resulting in stand on or move over the wall will be rejected and the agent will be stay in the same position.

Ensure each part of your response contains Python code actions for the next step, following the example provided, with concise and clear logic comments embedded in the code.
Your response should be similar with the following example(ONLY CODE) and NOTHING ELSE.
"""},
        # 2. Provide the current var and usable tools
        {"role": "user",
         "content": f"""
Your formally-defined parameters and their previewing are as follows: 
{puppy_instance.puppy_vars.preview()}

The historical codes are: {history_codes}
Note that, if you see multiple same codes in the historical codes, it might be the case that the movements were trying to reach the square where it's not empty (has the door or wall), and those actions were rejected! So do not repeat the same actions again!

Check if the undefined or unspecific variables are in the above preview and historical codes, if so, use them when needed in your code.

Your default function is writing python dictionaries.
You are also allowed to use the customized functions below, use them by just writing code as the example. the description shows how to use them. You are not allowed to call functions that out of the given range and python popular package:
{explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"])}

The current game map: 
{grid_string}.

The agent's current location is: ({agent_y}, {agent_x}).
The door status is: {door_dict}.
The tools you've taken are: {available_tools}.
The target usefulness score is: {target_usefulness}.
The current usefulness score is: {usefulness}.

You are only allowed to generate code that replace self.escaping(...) part, write code to control the agent to escape the room for the next step ONLY.


# Example codes for using all the tools available:
available_tools = get_all_available_tools(connection)
for tool_name in available_tools:
    use_tool(tool_name=tool_name, target_usefulness=self.target_usefulness)

# Example that reach the usefulness score and ready to escape:
## Agent is at (1, 2), the door is at (3, 5), so move down for 2 steps and right for 3 steps to reach the door.
move_agent(direction="down", step=2)
move_agent(direction="right", step=3)
## The agent now next to the door, so can use the tool to open the door.
use_tool(tool_name='Key', target_usefulness=target_usefulness)

# Example that need to adjust the usefulness score to match the target:
## The agent has reached the door and has 3 tools with usefulness scores: Tool 1 (0.3), Tool 2 (0.7), Tool 3 (1).
## The target usefulness score is 1.5, it is clear that the 3 tools are not good enough to reach the target.
## As there is no more tools with usefulness score 0.2, the agent can give up Tool 1 and Tool 2 and collect other tools instead.
give_up_tool(tool_name='Tool 1')
give_up_tool(tool_name='Tool 2')
## However, there are more tools that are not collected yet, so the agent can leave the door first and collect more tools.
move_agent(direction="left", step=2)
move_agent(direction="up", step=3) # Get another tool, with usefulness score 0.5.
## Now, the agent can use the tool with score 1 and 0.5 to escape.
use_tool(tool_name='Tool 3', target_usefulness=1.5)
use_tool(tool_name='Tool 4', target_usefulness=1.5)
----------
## Alternatively, the agent can keep searching for the tool with usefulness score 0.1 and use it twice.
move_agent(direction="right", step=1) # Get another tool, with usefulness score 0.1.
use_tool(tool_name='Tool 5', target_usefulness=1.5)
use_tool(tool_name='Tool 5', target_usefulness=1.5)
use_tool(tool_name='Tool 1', target_usefulness=1.5)
use_tool(tool_name='Tool 3', target_usefulness=1.5)
## Now, the usefulness score is 0.1+0.1+0.3+1=1.5, the agent can escape.


Now, write your code to control the agent to escape the room:
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
        action_type="escaping",
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

