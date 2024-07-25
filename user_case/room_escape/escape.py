from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.llm.open_ai import open_ai_chat
from puppys.pp.actions.explore import explore


def escape(
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
    # print("explore: ", explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"]))

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
- Note that, if the tool is on the left of 1 step to the agent, but the agent go left for 2 steps, the game will consider the agent has ignored the tool.

7. Rules for Escaping (win/end the game):
- Collect tools to reach or exactly match a given target usefulness score. Can use one tool that matches the target score or multiple tools to sum up to the target score.
- The escape is successful when the agent is **adjacent to the exit door**, i.e., one step left/right/up/down to the door, but not stand on the door!

8. Game Mechanics:
    1. Analyze the Current State:
    - Compare the current usefulness score with the target usefulness score to determine how much more usefulness is needed.
    - Identify which tools are still available on the grid that can help achieve the remaining usefulness score.

    2. Planning and Movement:
    - Plan a route to move towards the target tools based on their locations on the grid.
    - Navigate the grid by calculating the optimal steps and direction to reach each tool without skipping them.

    3. Tool Collection and Door Opening:
    - Collect tools by moving onto their grid positions.
    - Once the target usefulness is met or exceeded, plan a route to the square adjacent to the door.
    - Use the collected tools to try opening the door if adjacent to it.

9. Additional Notes:
- Ensure that movements are planned so that the agent lands exactly on the tool to pick it up; overshooting will result in just moving past the tool.
- If multiple useful tools are aligned in one direction, plan consecutive moves in that direction to collect them sequentially without additional commands.
- The game HAS TO be played in multiple rounds, so make sure you write the code for the next step ONLY, the rest steps can be performed in the following rounds.
- The agent CANNOT stand on the door or wall, so plan the final move to be next to the door to use the tool to open it, instead of keep moving. Any action resulting in the agent standing on the door or wall will be rejected and the agent will be stay in the same position.
- The agent CANNOT move over the door or wall, so plan the route to avoid these obstacles!

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

You are only allowed to generate code that replace self.escape(...) part, write code to control the agent to escape the room for the next step ONLY.


# Examples on planning the route to reach a target object:
- Example 1: Navigate to collect the 'Key'
  - Grid situation: The agent is at (1, 2) (row 1, column 2), and the 'Key' is at (4, 3) (row 4, column 3) with a usefulness score of 1.
  - Planned Route: Move down 3 steps, then right 1 step.
  - Command: `move_agent(direction="down", step=3)`, followed by `move_agent(direction="right", step=1)`.

- Example 2: Immediate tool collection
  - Grid situation: The agent is at (1, 2) (row 1, column 2), and the 'Hammer' is directly left at (1, 1) (row 1, column 1) with a usefulness score of 0.5.
  - Planned Route: Move left 1 step to collect the 'Hammer'.
  - Command: `move_agent(direction="left", step=1)`.


# Example codes for using the tool:
## Use the tool 'Key' to open the door with the target usefulness score 1
use_tool(tool_name='Key', target_usefulness=1)

## Use all the tools available
available_tools = get_all_available_tools(connection)
for tool_name in available_tools:
    use_tool(tool_name=tool_name, target_usefulness=self.target_usefulness)


# Example codes for game scenarios:
## Collecting tool when the current usefulness score is 0 and only one tool is needed to reach the target usefulness score:
## Agent is at (1, 2) and the tool 'Key' is at (4, 3).
move_agent(direction="down", step=3)
move_agent(direction="right", step=1)

## Collecting multiple tools to reach the target usefulness score:
## Agent is at (1, 2) and the tools 'Hammer' and 'Key' are at (4, 2) and (4, 3) respectively.
move_agent(direction="down", step=3) # Get the 'Hammer' first, usefulness score is not enough yet
move_agent(direction="left", step=1) # Get the 'Key' next

## Moving when there is a wall or door in the way:
## Agent is at (1, 3), the door is at (0, 1) and the wall is at (1, 1).
## CANNOT move left as there is a wall, the agent needs to move left and move up to reach the door, so move up first.
move_agent(direction="up", step=1)
move_agent(direction="left", step=1) # reach (0, 2), which is next to the door, cannot move to the door directly.

## Reach the usefulness score and ready to escape:
## Agent is at (1, 2), the door is at (3, 5).
## CANNOT move to the door but the square next to it to use the tool.
## The squares next to the door are (2, 5), (4, 5), (3, 4) and (3, 6), only (2, 5) and (3, 6) are empty.
## Among them, (2, 5) is closer to the agent's current position.
move_agent(direction="down", step=1)
move_agent(direction="right", step=3)
## The agent now next to the door, so can use the tool to open the door.
use_tool(tool_name='Key', target_usefulness=target_usefulness)


Key Rule Reminder:
- Movement: Ensure to avoid moving the agent into the door or wall squares, as this is not allowed. Only one object can occupy a square at a time.
- Escaping the Room: To escape the room, the agent must move to a square adjacent to the door (not onto the door itself) and then use the necessary tools. This is the only way to open the door and complete the game.

Now, write your code to control the agent to escape the room for the next step ONLY:
"""}]
    
    """
    ### Example Scenario for Next Step:
Grid Description:
  - The dimension of the grid: 5
  - In row 0 and column 1: door
  - In row 0 and column 4: wall
  - In row 1 and column 2: agent
  - In row 1 and column 4: tool `Hammer` - A hammer that can break the door; Usefulness Score: 0.5
  - In row 4 and column 0: wall
  - In row 4 and column 2: tool `Cup` - A cup that can be used to drink water; Usefulness Score: 0
  - In row 4 and column 3: tool `Key` - A key that can unlock the door; Usefulness Score: 1
Current Usefulness Score: 0
Target Usefulness Score: 0.5

Code for Next Step:
# Agent is at (1, 2) and needs to collect the 'Hammer' at (1, 4) to reach the target usefulness score.
# Plan: Move right 2 steps to reach the 'Hammer'.
move_agent(direction="right", step=2)

Instructions for Future Steps to Win the Game (Do not code this now, it's just for planning):
# After collecting the 'Hammer', navigate the agent to a square next to the door. The door is at (0, 1), but the agent can position itself at (0, 2) to use the tool, as directly moving to the door's square is prohibited.
# The planned moves to reach the position next to the door from the current location (after collecting the Hammer at (1, 4)) are:
# Move up 1 step to row 0.
# Move left 2 steps to column 2, just right of the door.
move_agent(direction="up", step=1)
move_agent(direction="left", step=2)

# Use the 'Hammer' to open the door once positioned correctly next to it.
use_tool(tool_name='Hammer', target_usefulness=target_usefulness)
    """

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

