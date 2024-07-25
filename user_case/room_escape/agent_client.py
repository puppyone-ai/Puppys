import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import socket
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from escaping import escaping


class ServerConnection:
    def __init__(self, host: str = 'localhost', port: int = 5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def fetch_state(self) -> dict:
        self.socket.sendall(b'GET_STATE')
        response = self.socket.recv(4096)
        return json.loads(response.decode('utf-8'))

    def update_state(self, data: dict) -> None:
        serialized_data = json.dumps(data).encode('utf-8')
        self.socket.sendall(serialized_data)
        response = self.socket.recv(1024)
        print("Server response:", response.decode('utf-8'))

    def close(self):
        self.socket.close()


def move_agent(connection: ServerConnection, direction: str, step: int) -> None:
    """
`move_agent` moves the agent on the game grid based on the specified direction and number of steps. It updates the agent's position. If the agent encounters a tool during the move, the tool is added to the agent's list of available tools.

Parameters:
- `direction` (str): Direction to move the agent. Valid values are 'up', 'down', 'left', 'right'.
- `step` (int): Number of grid spaces the agent should move in the specified direction.

Return Value: None.

Note: You HAVE TO write the positional arguments when writing code to call the function.

# Examples on Move to collect tool:
## Agent is at (1, 2) (row 1, column 2) and the tool is at (4, 3) (row 4, column 3).
move_agent(direction="down", step=3)
move_agent(direction="right", step=1)

# Examples on Move to collect multiple tools:
## Agent is at (1, 2) (row 1, column 2) and the tools are at (4, 2) (row 4, column 2) and (4, 3) (row 4, column 3) respectively.
move_agent(direction="down", step=3) # Get one tool first, usefulness score is not enough yet
move_agent(direction="left", step=1) # Get the other tool

# Example that have multiple moves in one step to reach the target position but avoid the wall:
# Agent is at (0, 4), the door (target) is at (0, 6), but there is a wall at (0, 5).
# As the agent is at row 0, there is no upward locations, so have to move downward first to avoid the wall.
move_agent(direction="down", step=1)
move_agent(direction="right", step=2)
move_agent(direction="up", step=1) # Now, the agent has reach the door.
# Although multiple lines of code has written, it can be considered as one step.
"""    

    game_state = connection.fetch_state()

    grid = game_state.get("grid")
    agent_x = game_state.get("agent_x")
    agent_y = game_state.get("agent_y")
    available_tools = game_state.get("available_tools")
    current_action_string = ""

    # Calculate new position based on direction and steps
    new_x, new_y = agent_x, agent_y
    if direction == "up":
        new_y = max(0, agent_y - step)
        current_action_string = f"Moving up, {step} steps."
    elif direction == "down":
        new_y = min(len(grid) - 1, agent_y + step)
        current_action_string = f"Moving down, {step} steps."
    elif direction == "left":
        new_x = max(0, agent_x - step)
        current_action_string = f"Moving left, {step} steps."
    elif direction == "right":
        new_x = min(len(grid[0]) - 1, agent_x + step)
        current_action_string = f"Moving right, {step} steps."

    if grid[new_y][new_x] == 'Wall':
        return

    if isinstance(grid[new_y][new_x], dict):
        available_tools.append(grid[new_y][new_x])
        tool_name = grid[new_y][new_x].get("name")
        current_action_string += f"\nTaking tool `{tool_name}`."

    # Update the game state
    if grid[new_y][new_x] == 'Door':
        grid[agent_y][agent_x], grid[new_y][new_x] = ' ', 'D&A'
    elif grid[agent_y][agent_x] == 'D&A':
        grid[agent_y][agent_x], grid[new_y][new_x] = 'Door', 'Agent'
    else:
        grid[agent_y][agent_x], grid[new_y][new_x] = ' ', 'Agent'

    game_state["grid"] = grid
    game_state["agent_x"] = new_x
    game_state["agent_y"] = new_y
    game_state["available_tools"] = available_tools
    game_state["current_action_string"] = current_action_string

    connection.update_state(game_state)

def use_tool(connection: ServerConnection, tool_name: str, target_usefulness: int) -> None:
    """
`use_tool` controls the agent to use a given tool by adding the usefulness score to the current total usefulness score.
If the door is next to the agent's current position and the current total usefulness is exactly equal to the target usefulness, the door status is updated to open in the game state and the agent wins the game!

The function is only useful when the agent is next to the door, otherwise, it does nothing.

Parameters:
- `tool_name` (str): The name of the tool the agent intends to use.
- `target_usefulness` (int): The target usefulness value required to open the door.

Return Value: None.

Note: You HAVE TO write the positional arguments when writing code to call the function.

Example Usages:
# Assume the target usefulness is 1
# The agent is now just one step left to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(tool_name='Key', target_usefulness=1)

# The agent is now just one step right to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(tool_name='Key', target_usefulness=1)

# The agent is now just one step up to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(tool_name='Key', target_usefulness=1)

# The agent is now just one step down to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(tool_name='Key', target_usefulness=1)
    """

    game_state = connection.fetch_state()

    grid = game_state.get("grid")
    agent_x = game_state.get("agent_x")
    agent_y = game_state.get("agent_y")
    available_tools = game_state.get("available_tools")
    usefulness = game_state.get("usefulness")

    # Check if the agent is currently at the door
    if grid[agent_y][agent_x] != 'D&A':
        return

    for tool in available_tools:
        current_tool_name = tool.get("name")
        if current_tool_name == tool_name:
            game_state["current_action_string"] = f"Using tool `{current_tool_name}`."
            usefulness += tool.get("usefulness", 0)
            if usefulness == target_usefulness:
                game_state["door_dict"]["open"] = True

    # Update the game state
    game_state["usefulness"] = round(usefulness, 1)

    connection.update_state(game_state)

def get_all_available_tools(connection: ServerConnection) -> list:
    """
    Retrieves the names of all tools currently available on the game grid. 
    It scans the entire grid and collects the names of all tool objects.

    Parameters: None.

    Return Value: `list`: A list of strings, each a name of an available tool.

    Example Usages:
    available_tools = get_all_available_tools()
    print(available_tools)  # Output might be ['Key', 'Hammer', 'Screwdriver']
    """

    game_state = connection.fetch_state()
    available_tools = game_state.get("available_tools")

    return [tool.get("name") for tool in available_tools if tool.get("name")]

def give_up_tool(connection: ServerConnection, tool_name: str) -> None:
    """
    Give up using a tool by decreasing the current usefulness score.
    If the tool is not in the list of available tools, nothing happens.
    The usefulness score cannot be negative, so the score will be set to 0 if it would be negative.

    Parameters:
    - `tool_name` (str): The name of the tool to give up.

    Return Value: None.

    Example Usages:
    give_up_tool(tool_name='Key')
    
    # The target usefulness is 1.5, the agent has tool1 with a usefulness of 1 and tool2 with a usefulness of 0.5. But the agent has used tool1 for twice, exceeding the target usefulness.
    # Then, the good strategy is to give up tool1 and use tool2 to reach the target usefulness.
    give_up_tool(tool_name='tool1')
    """

    game_state = connection.fetch_state()
    available_tools = game_state.get("available_tools")
    usefulness = game_state.get("usefulness")

    for tool in available_tools:
        if tool.get("name") == tool_name:
            usefulness -= tool.get("usefulness", 0)
            game_state["current_action_string"] = f"Giving up tool `{tool_name}`."
            break

    game_state["usefulness"] = usefulness if usefulness > 0 else 0
    connection.update_state(game_state)


class Escaper(Puppy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Escaper"
        self.description = "A puppys that could play the game `room escape`."
        self.version = "0.0.1"

        self.connection = ServerConnection()

        self.move_agent = FuncEnv(
            value=move_agent,
            name=move_agent.__name__,
            description=move_agent.__doc__,
            fixed_params={"connection": self.connection},
            free_params=["direction", "step"]
        )

        self.use_tool = FuncEnv(
            value=use_tool,
            name=use_tool.__name__,
            description=use_tool.__doc__,
            fixed_params={"connection": self.connection},
            free_params=["tool_name", "target_usefulness"]
        )

        self.get_all_available_tools = FuncEnv(
            value=get_all_available_tools,
            name=get_all_available_tools.__name__,
            description=get_all_available_tools.__doc__,
            fixed_params={"connection": self.connection},
        )

        self.give_up_tool = FuncEnv(
            value=give_up_tool,
            name=give_up_tool.__name__,
            description=give_up_tool.__doc__,
            fixed_params={"connection": self.connection},
            free_params=["tool_name"]
        )

    def escaping(self, *args, **kwargs):
        return escaping(self, *args, **kwargs)


def decision_tree(self, target_usefulness):
    import time
    self.target_usefulness = round(target_usefulness, 1)
    self.connection.update_state({"target_usefulness": target_usefulness})
    while True:
        self.game_state = self.connection.fetch_state()
        if self.game_state.get("door_dict", {}).get("open"):
            break
        self.escaping(self.game_state, self.target_usefulness, show_response=True)
        time.sleep(2)
    self.connection.close()

escaper = Escaper(decision_tree)
escaper.run(target_usefulness=1.5)
