from puppys.env.env import Env
from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.llm.open_ai import open_ai_chat
from puppys.pp.actions.explore import explore


def escaping(
    puppy_instance, 
    model: str = "gpt-4-turbo",
    show_prompt: bool = False,
    show_response: bool = False, 
    ) -> str:
    # Get the game state
    envs = explore(environment=puppy_instance.env_node, target=Env, output_content_mode="attribute", attributes=["name", "description"])
    sub_game_map = explore(environment=puppy_instance.env_node.game_map, target=Env, output_content_mode="attribute", attributes=["name", "description"])
    game_map_dict = {"game_map": envs.get("game_map")}
    game_map_dict.update(sub_game_map)
    game_map_string = ""
    for value in game_map_dict.values():
        game_map_string += f"{value['name']}: {value['description']}\n"

    prompt = [
        {"role": "system",
         "content": """
Objective: As an AI code agent, your goal is to help the agent escape the room by collecting keys with specific key_name s and using them to open the exit door. You need to write Python codes to achieve these.

1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
you can show your thinking and reason in the comment.
 For example: # Hello, I am an agent. 

2. Your code will be run immediately after you write it. If you assume any hypothetical function, the the system will crash. 

3. Your response cannot only be comment. You HAVE to write codes

4. Make sure that the parameter in your respond code follow the type of the parameter in the function instruction. 

5. About the Game:
- Grid: The room is represented as a grid (e.g., 5x5) with single objects per square: keys, a door, walls, or empty space. All other squares are empty and are the spaces for you (the agent) to move around.
- The grid will be provided in a descriptive string format, containing the dimension of the map grid (dimension=5 means the map is a 5 * 5 grid, 25 squares inside), and the object contained in each square (the empty square will not be described).
- The grid (game map) is count from 0 to n-1, n is the dimension of the grid. The position data will be provided in (row number, column number), row number count from up to down, column number count from left to right.
- Agent: You control the agent who can move around to collect keys and navigate towards the exit door.
- keys: Each key has a name, keys can be collected by moving the agent onto their respective squares.
- Boxes: Each box can either be empty or contain a key, if contains a key, the key can be collected by moving the agent onto the box, then open the box and take the key. If the box is empty, the agent can move onto the box without any action.
- The boxes and keys are all represented in dictionary, with field of `name`, `in_box`, `opened`. If the box is empty, the name will also be empty.

6. About the movement:
- The keys are only available to use if the agent (you) has moved to the square where the key is located, meaning that the agent picked up the key. Otherwise, the agent won't be able to use it.
- Note: If the key is on the left of 1 step to the agent, but the agent go left for 2 steps, the game will consider the agent has ignored the key.

7. Rules for Escaping (win/end the game):
- The door will be opened once all the target keys ahs collected, the target keys can be one or more. If there are multiple target keys, the agent (you) needs to collect all of them.
- Sometime, the target keys might be in the boxes, the agent needs to find the correct box and then open it to take the key.
- The escape is successful only if the agent is standing in the same location as the door and has all the target keys.

8. Game Mechanics:
    1. Analyze the Current State: Compare the available keys with the target keys to determine how much and which keys are still missing. If not all the target keys are in the map, part of the keys may contained in some boxes, you have to find the correct boxes which contains the target key.
    2. Planning and Movement:
    - Plan a route to move towards the missing keys based on their locations on the grid.
    - Always plan to collect the required keys, not the nearest keys.
    - Navigate the grid by calculating the optimal steps and direction to reach each key without skipping them.
    - If the key is in a box, plan to move onto the location where the box is and open it and take the key.
    3. Key Collection and Escape Successfully:
    - Once the target keys are all available, plan a route to the door.
    - Use correct keys one by one to escape.

9. Additional Notes:
- If multiple useful keys are aligned in one direction, plan consecutive moves in that direction to collect them sequentially without additional commands.
- The game HAS TO be played in multiple rounds, so make sure you write the code for the next step ONLY, the rest steps can be performed in the following rounds.
- The agent CANNOT stand on or move over the wall, instead, plan the route to avoid the wall. Movements resulting in stand on or move over the wall will be rejected and the agent will be stay in the same position.
- The agent don't have to open all the boxes, as long as the agent has all the target keys and stand onto the door, the agent can escape the room.

Ensure each part of your response contains Python code actions for the next step, following the example provided, with concise and clear logic comments embedded in the code.
Your response should be similar with the following example(ONLY CODE) and NOTHING ELSE.
"""},
        # 2. Provide the current var and usable keys
        {"role": "user",
         "content": f"""
Your formally-defined parameters and their previewing are as follows: 
{puppy_instance.puppy_vars.preview()}

Check if the undefined or unspecific variables are in the above preview, if so, use them when needed in your code.

Your default function is writing python dictionaries.
You are also allowed to use the customized functions below, use them by just writing code as the example. the description shows how to use them. You are not allowed to call functions that out of the given range and python popular package:
{explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"])}

You are only allowed to generate code that replace self.escaping(...) part, write code to control the agent to escape the room for the next step ONLY.

The current game map and all the relevant information about the current game status are included below, read them carefully to understand the current game environment and plan your next actions accordingly.
{game_map_string}

Note that you cannot move out of the game map boundary or move over the wall, such actions will be rejected and the agent will stay in the same position.
Example: The agent is at (6, 6), the game map dimension is 7 (from 0 to 6), so the agent cannot move right or down anymore.

# Example codes for using all the keys available:
available_keys = get_all_available_keys(connection)
for key_name in available_keys:
    use_key(key_name=key_name)

# Example that already have all the target keys and ready to escape:
## Agent is at (1, 2), the door is at (3, 5), so move down for 2 steps and right for 3 steps to reach the door.
move_agent(direction="down", step=2)
move_agent(direction="right", step=3)
## Target keys: yellow and blue. The agent now next to the door, so can use the keys to open the door.
use_key(key_name='yellow')
use_key(key_name='blue')

Now, write your code to control the agent to escape the room:
"""}]

    # Prompt Finished *****************************************************************************************

    action = Action(
        puppy_instance,
        action_name="",
        show_prompt=show_prompt,
        show_response=show_response,
        retries=0,
        replace_code=True
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

    # Run the code
    try:
        return action.run_without_errors(new_code)
    # Handle errors
    except Exception as e:
        error_details = action.run_with_errors(e)
        print(error_details)

