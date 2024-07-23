import json
import socket
from game_tool import Tool
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from play import play
from puppys.llm.open_ai import open_ai_chat
from puppys.tools.defaultTools import talk_with_human, llm


def fetch_state_from_server():
    host = 'localhost'
    port = 5555
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'GET_STATE')
        response = s.recv(4096)
        state = json.loads(response.decode('utf-8'))
    return state


def update_state_on_server(data):
    host = 'localhost'
    port = 5555
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        serialized_data = json.dumps(data).encode('utf-8')
        s.sendall(serialized_data)
        response = s.recv(1024)
        print("Server response:", response.decode('utf-8'))




def move_agent(action, steps):
    """
Functionality:  
This function moves the agent on the game grid based on the specified direction and number of steps. It updates the agent's position.

Parameters:
- `action` (str): Direction to move the agent. Valid values are 'left', 'right', 'up', and 'down'.
- `steps` (int): Number of grid spaces the agent should move in the specified direction.

Return Value:  
None.

Example Usage:
# Move the agent 2 steps to the left
move_agent(action='left', steps=2)

# Move the agent 1 step downward
move_agent(action='down', steps=1)
    """
    state = fetch_state_from_server()
    agent_x, agent_y = state['agent_position']
    grid_size = state['grid_size']

    if action == 'left':
        agent_x = max(0, agent_x - steps)
    elif action == 'right':
        agent_x = min(grid_size - 1, agent_x + steps)
    elif action == 'up':
        agent_y = max(0, agent_y - steps)
    elif action == 'down':
        agent_y = min(grid_size - 1, agent_y + steps)

    update_state_on_server({'action': 'move', 'dx': agent_x, 'dy': agent_y})



def pick_up_tool():
    """
Functionality:  
Checks the agent's current location for available tools. If a tool is present, it picks up the tool, updating the agent's inventory and the game state on the server.

Parameters: None.

Return Value: None.

Example Usage:
# Take the tool at the agent's current location
pick_up_tool()
    """
    state = fetch_state_from_server()
    agent_pos = state['agent_position']
    tool_at_position = state['grid'][agent_pos[1]][agent_pos[0]]

    if isinstance(tool_at_position, Tool) and not tool_at_position.taken:
        tool_at_position.take_tool()
        update_state_on_server({'action': 'pick_up', 'position': agent_pos})
    else:
        print("No tool available at this position.")


def find_subtools(tool_name):
    """
Functionality:  
Fetches all subtools associated with a specified tool from the game's current state.

Parameters:
- `tool_name` (str): Name of the tool for which subtools are to be listed.

Return Value:  
list: Names of all subtools under the specified tool.

Example Usage:
# Find all subtools under the 'box' tool
subtools = find_subtools(tool_name='box')
print(subtools)  # Output might be ['Key', 'Toy', 'Cup']
    """
    state = fetch_state_from_server()
    tool = next((t for t in state['tools'] if t['name'] == tool_name), None)
    if tool and tool.subtools:
        return [subtool.name for subtool in tool.subtools]
    return []


def pick_subtool(tool_name, subtool_name):
    """
Functionality:  
Allows the agent to pick a specific subtool from a tool if available, updating the game state on the server.

Parameters:
- `tool_name` (str): Name of the main tool.
- `subtool_name` (str): Name of the subtool to be picked up.

Return Value:  
None.

Example Usage:
# Pick the 'House Key' subtool from the 'Keychain' tool
pick_subtool(tool_name='Keychain', subtool_name='House Key')
    """
    state = fetch_state_from_server()
    tools = state['tools']
    for tool in tools:
        if tool['name'] == tool_name:
            for subtool in tool['subtools']:
                if subtool['name'] == subtool_name and not subtool['taken']:
                    subtool['taken'] = True
                    update_state_on_server({'action': 'pick_subtool', 'tool_name': tool_name, 'subtool_name': subtool_name})
                    print(f"Subtool {subtool_name} picked from {tool_name}.")
                    return
    print("Subtool not available or already taken.")




def use_tool(tool_name, action_name):
    """
Functionality:  
Uses a specified tool from the agent's inventory to perform an action. It returns the result of the action based on the tool's capabilities and effects.

Parameters:
- `tool_name` (str): Name of the tool to be used.
- `action_name` (str): Specific action to perform with the tool.

Return Value:  
`str`: The result of the action, which could be a message indicating the outcome or a failure message if the tool or action is not available.

Example Usage:
# Use the key tool to unlock a door
result = use_tool(tool_name='Key', action_name='unlock')
print(result)  # Prints the outcome of the unlock attempt
    """
    state = fetch_state_from_server()
    tool = next((t for t in state['tools'] if t['name'] == tool_name), None)

    if tool and action_name in tool['actions']:
        result = tool['actions'][action_name]()
        print("Action result:", result)
        update_state_on_server({'action': 'use_tool', 'tool_name': tool_name, 'action_name': action_name})
        return result
    return "Action not possible or tool not found."


def check_action_result(action_result):
    """
Functionality:  
Evaluates the result of an action to determine the state of the game element (like a door). This function uses a language model to interpret the results and updates the game state on the server if necessary.

Parameters:
- `action_result` (str): Description of the action result to be evaluated by the language model.

Return Value:  
None. The function will directly print the status of the door and may end the game if conditions are met.

Example Usage:
# Check if the action result of using a key has opened the door
check_action_result(action_result="The key turns smoothly, the lock clicks open.")
    """
    # Fetch current state from server
    current_state = fetch_state_from_server()
    
    system_prompt = """
You are in a room escape game.
Your task is to determine the status of a door in the game scenario based on the described outcome of an action. 
You MUST decide if the door is "open" or "closed" based solely on the description of the actions and the tool used. 
Please ensure your response is either "open" or "closed" without any additional explanation or text.

### Examples
Example 1:
- Action Result: "The key fits perfectly, and as it turns, you hear a loud click."
- Expected Output: "open"

Example 2:
- Action Result: "The key turns, but the lock doesn't release."
- Expected Output: "closed"

Example 3:
- Action Result: "You use the key, and the door swings open effortlessly."
- Expected Output: "open"

Example 4:
- Action Result: "The handle jiggles, but the door remains firmly shut."
- Expected Output: "closed"
    """
    
    user_prompt = f"""
    Based on the following action result: {action_result}, is the door open or closed?
    """
    
    # Construct prompt for the LLM
    prompt = [{"role": "system", "content": system_prompt},
              {"role": "user", "content": user_prompt}]

    # Call the OpenAI chat api
    result = open_ai_chat(
        prompt = prompt,
        model = "gpt-4o",
        temperature = 0.7,
        max_tokens = 10,
        printing = True, 
        stream = True
    )

    if result.lower() == 'open':
        update_state_on_server({'action': 'update_door_status', 'status': 'open'})





class Escaper(Puppy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Escaper"
        self.description = "A puppys that could play the game `room escape`."
        self.version = "0.0.1"

        # The first tool
        self.llm = FuncEnv(
            value=llm,
            name=llm.__name__,
            description=llm.__doc__
        )

        # The second tool
        self.talk_with_human = FuncEnv(
            value=talk_with_human,
            name=talk_with_human.__name__,
            description=talk_with_human.__doc__,
            fixed_params={"puppy": self}
        )
        
        # Game tools
        self.move_agent = FuncEnv(
            value=move_agent,
            name=move_agent.__name__,
            description=move_agent.__doc__,
            fixed_params={"puppy": self},
            free_params=["action", "steps"]
        )
        self.pick_up_tool = FuncEnv(
            value=pick_up_tool,
            name=pick_up_tool.__name__,
            description=pick_up_tool.__doc__,
            fixed_params={"puppy": self},
            free_params=[]
        )
        self.use_tool = FuncEnv(
            value=use_tool,
            name=use_tool.__name__,
            description=use_tool.__doc__,
            fixed_params={"puppy": self},
            free_params=["tool_name", "action_name"]
        )
        self.check_action_result = FuncEnv(
            value=check_action_result,
            name=check_action_result.__name__,
            description=check_action_result.__doc__,
            fixed_params={"puppy": self},
            free_params=["action_result"]
        )

    def play(self, *args, **kwargs):
        return play(self, *args, **kwargs)


