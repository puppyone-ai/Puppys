import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import socket
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from escape import escape


class ServerConnection:
    def __init__(self, host='localhost', port=5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def fetch_state(self):
        self.socket.sendall(b'GET_STATE')
        response = self.socket.recv(4096)
        return json.loads(response.decode('utf-8'))

    def update_state(self, data):
        serialized_data = json.dumps(data).encode('utf-8')
        self.socket.sendall(serialized_data)
        response = self.socket.recv(1024)
        print("Server response:", response.decode('utf-8'))

    def close(self):
        self.socket.close()


def move_agent(connection, direction, step):
    """
`move_agent` moves the agent on the game grid based on the specified direction and number of steps. It updates the agent's position. If the agent encounters a tool during the move, the tool is added to the agent's list of available tools.

Parameters:
- `connection` (ServerConnection): The connection object to communicate with the server. This param will be provided, you don't need to create any object for this, just looking for the pre-defined variable and directly use it to be the param value.
- `direction` (str): Direction to move the agent. Valid values are 'up', 'down', 'left', 'right'.
- `step` (int): Number of grid spaces the agent should move in the specified direction.

Return Value: None.

Note: You HAVE TO write the positional arguments when writing code to call the function.

Example Usages:
move_agent(connection=connection, direction='left', step=2)

# Move the agent 1 step upward
move_agent(connection=connection, direction='up', step=1)
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
        current_action_string = f"Moving up for {step} steps."
    elif direction == "down":
        new_y = min(len(grid) - 1, agent_y + step)
        current_action_string = f"Moving down for {step} steps."
    elif direction == "left":
        new_x = max(0, agent_x - step)
        current_action_string = f"Moving left for {step} steps."
    elif direction == "right":
        new_x = min(len(grid[0]) - 1, agent_x + step)
        current_action_string = f"Moving right for {step} steps."
    
    if grid[new_y][new_x] in ['D', 'W']:
        return

    if isinstance(grid[new_y][new_x], dict):
        available_tools.append(grid[new_y][new_x])
        tool_name = grid[new_y][new_x].get("name")
        current_action_string += f"\nPicking up the tool `{tool_name}`."
    
    # Update the game state
    grid[agent_y][agent_x], grid[new_y][new_x] = ' ', 'A'
    game_state["grid"] = grid
    game_state["agent_x"] = new_x
    game_state["agent_y"] = new_y
    game_state["available_tools"] = available_tools
    game_state["current_action_string"] = current_action_string

    connection.update_state(game_state)


def use_tool(connection, tool_name, target_usefulness):
    """
`use_tool` controls the agent to use a given tool by adding the usefulness score to the current total usefulness score.
If the door is next to the agent's current position and the current total usefulness is exactly equal to the target usefulness, the door status is updated to open in the game state and the agent wins the game!

The function is only useful when the agent is next to the door, otherwise, it does nothing.

Parameters:
- `connection` (ServerConnection): The connection object to communicate with the server. This param will be provided, you don't need to create any object for this, just looking for the pre-defined variable and directly use it to be the param value.
- `tool_name` (str): The name of the tool the agent intends to use.
- `target_usefulness` (int): The target usefulness value required to open the door.

Return Value: None.

Note: You HAVE TO write the positional arguments when writing code to call the function.

Example Usages:
# The agent is now just one step left to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(connection=connection, tool_name='Key', target_usefulness=1)

# The agent is now just one step right to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(connection=connection, tool_name='Key', target_usefulness=1)

# The agent is now just one step up to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(connection=connection, tool_name='Key', target_usefulness=1)

# The agent is now just one step down to the door and the target usefulness score has reached, so can use the tool to open the door.
use_tool(connection=connection, tool_name='Key', target_usefulness=1)
    """

    game_state = connection.fetch_state()

    grid = game_state.get("grid")
    agent_x = game_state.get("agent_x")
    agent_y = game_state.get("agent_y")
    available_tools = game_state.get("available_tools")
    usefulness = game_state.get("usefulness")

    # Check if the agent is next to the door
    next_to_door = False
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = agent_x + dx, agent_y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == 'D':
            next_to_door = True
            break

    if not next_to_door:
        return

    for tool in available_tools:
        current_tool_name = tool.get("name")
        if current_tool_name == tool_name:
            game_state["current_action_string"] = f"Using the tool {current_tool_name}."
            usefulness += tool.get("usefulness", 0)
            if usefulness == target_usefulness:
                game_state["door_dict"]["open"] = True

    # Update the game state
    game_state["usefulness"] = usefulness

    connection.update_state(game_state)


def get_all_available_tools(connection):
    """
    Retrieves the names of all tools currently available on the game grid. 
    It scans the entire grid and collects the names of all tool objects.

    Parameters: `connection` (ServerConnection): The connection object to communicate with the server.

    Return Value: `list`: A list of strings, each a name of an available tool.

    Example Usage:
    available_tools = get_all_available_tools(connection)
    print(available_tools)  # Output might be ['Key', 'Hammer', 'Screwdriver']
    """

    game_state = connection.fetch_state()
    available_tools = game_state.get("available_tools")

    return [tool.get("name") for tool in available_tools if tool.get("name")]



class Escaper(Puppy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Escaper"
        self.description = "A puppys that could play the game `room escape`."
        self.version = "0.0.1"
        
        # self.connection = ServerConnection()

        self.move_agent = FuncEnv(
            value=move_agent,
            name=move_agent.__name__,
            description=move_agent.__doc__,
            free_params=["connection", "direction", "step"]
            # fixed_params={"connection": self.connection},
            # free_params=["direction", "step"]
        )

        self.use_tool = FuncEnv(
            value=use_tool,
            name=use_tool.__name__,
            description=use_tool.__doc__,
            free_params=["connection", "tool_name", "target_usefulness"]
            # fixed_params={"connection": self.connection},
            # free_params=["tool_name", "target_usefulness"]
        )

        self.get_all_available_tools = FuncEnv(
            value=get_all_available_tools,
            name=get_all_available_tools.__name__,
            description=get_all_available_tools.__doc__,
            free_params=["connection"]
            # fixed_params={"connection": self.connection},
        )

    def escape(self, *args, **kwargs):
        return escape(self, *args, **kwargs)


def decision_tree(self, target_usefulness, connection):
    import time
    self.target_usefulness = target_usefulness
    self.connection = connection
    self.connection.update_state({"target_usefulness": target_usefulness})
    while True:
        self.game_state = self.connection.fetch_state()
        if self.game_state.get("door_dict", {}).get("open"):
            break
        self.escape(self.game_state, self.target_usefulness, show_response=True)
        # time.sleep(2)
    self.connection.close()


escaper = Escaper(decision_tree)
escaper.run(target_usefulness=1, connection=ServerConnection())

# connection = ServerConnection()
# move_agent(connection=connection, direction="right", step=1)
# connection.close()
