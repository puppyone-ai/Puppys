import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import socket
from collections import Counter
from puppys.env.env import Env
from puppys.pp.main import Puppy
from puppys.env.func_env import FuncEnv
from escaping import escaping


class ServerConnection:
    def __init__(self, host: str = "localhost", port: int = 5555):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def fetch_state(self) -> dict:
        try:
            self.socket.sendall(b"GET_STATE")
            response = self.socket.recv(4096)
            return json.loads(response.decode("utf-8"))
        except ConnectionResetError:
            print("The server has closed!!!")
            return {}

    def update_state(self, data: dict) -> None:
        serialized_data = json.dumps(data).encode("utf-8")
        self.socket.sendall(serialized_data)
        response = self.socket.recv(1024)
        print("Server response:", response.decode("utf-8"))

    def close(self):
        self.socket.close()


def move_agent(connection: ServerConnection, direction: str, step: int) -> None:
    """
`move_agent` moves the agent on the game grid based on the specified direction and number of steps. It updates the agent"s position. If the agent encounters a key during the move, the key is added to the agent"s list of available keys.

Parameters:
- `direction` (str): Direction to move the agent. Valid values are "up", "down", "left", "right".
- `step` (int): Number of grid spaces the agent should move in the specified direction.

Return Value: None.

Note: You HAVE TO write the positional arguments when writing code to call the function.

# Examples on Move to collect key:
## Agent is at (1, 2) (row 1, column 2) and the key is at (4, 3) (row 4, column 3).
move_agent(direction="down", step=3)
move_agent(direction="right", step=1)

# Examples on Move to collect multiple keys:
## Agent is at (1, 2) (row 1, column 2) and the keys are at (4, 2) (row 4, column 2) and (4, 3) (row 4, column 3) respectively.
move_agent(direction="down", step=3) # Get one key first, not enough yet
move_agent(direction="left", step=1) # Get the other key

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
    available_keys = game_state.get("available_keys")
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

    if isinstance(grid[new_y][new_x], str) and grid[new_y][new_x].startswith("Wall"):
        return

    if isinstance(grid[new_y][new_x], dict):
        available_keys.append(grid[new_y][new_x])
        key_name = grid[new_y][new_x].get("name")
        current_action_string += f"\nTaking key `{key_name}`."

    # Update the game state
    if grid[new_y][new_x] == "Door":
        grid[agent_y][agent_x], grid[new_y][new_x] = " ", "D&A"
    elif grid[agent_y][agent_x] == "D&A":
        grid[agent_y][agent_x], grid[new_y][new_x] = "Door", "Agent"
    else:
        grid[agent_y][agent_x], grid[new_y][new_x] = " ", "Agent"

    game_state["grid"] = grid
    game_state["agent_x"] = new_x
    game_state["agent_y"] = new_y
    game_state["available_keys"] = available_keys
    game_state["current_action_string"] = current_action_string

    connection.update_state(game_state)

def use_key(connection: ServerConnection, key_name: str) -> None:
    """
`use_key` controls the agent to use a given key by adding the key_name to the used_keys list. If the used_keys list exactly matches the target_keys list, the door status is updated to open in the game state, and wins the game.

The function is only useful when the agent is standing on the door, otherwise, it does nothing.

Parameters: `key_name` (str): The name of the key the agent intends to use.

Return Value: None.

Note: You HAVE TO write the positional arguments when writing code to call the function.

Example Usages:
# The agent is now at the door and the has all the target keys available.
use_key(key_name="yellow")
use_key(key_name="blue")
    """

    game_state = connection.fetch_state()

    grid = game_state.get("grid")
    agent_x = game_state.get("agent_x")
    agent_y = game_state.get("agent_y")
    available_keys = game_state.get("available_keys")
    used_keys = game_state.get("used_keys")
    target_keys = game_state.get("target_keys")

    # Check if the agent is currently at the door
    if grid[agent_y][agent_x] != "D&A":
        return

    for key in available_keys:
        current_key_name = key.get("name")
        if current_key_name == key_name:
            game_state["current_action_string"] = f"Using key `{current_key_name}`."
            used_keys.append(current_key_name)
            if Counter(used_keys) == Counter(target_keys):
                game_state["door_dict"]["open"] = True

    # Update the game state
    game_state["used_keys"] = used_keys

    connection.update_state(game_state)

def get_all_available_keys(connection: ServerConnection) -> list:
    """
    Retrieves the names of all keys currently available on the game grid. 
    It scans the entire grid and collects the names of all key objects.

    Parameters: None.

    Return Value: `list`: A list of strings, each a name of an available key.

    Example Usages:
    available_keys = get_all_available_keys()
    print(available_keys)  # Output might be ["yellow", "blue"]
    """

    game_state = connection.fetch_state()
    available_keys = game_state.get("available_keys")

    return [key.get("name") for key in available_keys if key.get("name")]

def give_up_key(connection: ServerConnection, key_name: str) -> None:
    """
    Give up using a key by removing the key from the used_keys list. If the key is not in the list of used keys, nothing happens.

    Parameters: `key_name` (str): The name of the tool to give up.

    Return Value: None.

    Example Usages:
    give_up_key(key_name='blue')
    """

    game_state = connection.fetch_state()
    used_keys = game_state.get("used_keys")

    game_state["used_keys"] = [key for key in used_keys if key.get("name") != key_name]
    game_state["current_action_string"] = f"Giving up key `{key_name}`."

    connection.update_state(game_state)


class Escaper(Puppy):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.name = "Escaper"
        self.description = "A puppys that could play the game `room escape`."
        self.version = "0.0.1"

        self.connection = ServerConnection()
        self.game_map = self.get_game_env()

        self.move_agent = FuncEnv(
            value=move_agent,
            name=move_agent.__name__,
            description=move_agent.__doc__,
            fixed_params={"connection": self.connection},
            free_params=["direction", "step"]
        )

        self.use_key = FuncEnv(
            value=use_key,
            name=use_key.__name__,
            description=use_key.__doc__,
            fixed_params={"connection": self.connection},
            free_params=["key_name"]
        )

        self.get_all_available_keys = FuncEnv(
            value=get_all_available_keys,
            name=get_all_available_keys.__name__,
            description=get_all_available_keys.__doc__,
            fixed_params={"connection": self.connection},
        )

        self.give_up_key = FuncEnv(
            value=give_up_key,
            name=give_up_key.__name__,
            description=give_up_key.__doc__,
            fixed_params={"connection": self.connection},
            free_params=["key_name"]
        )

    def get_game_env(self) -> Env:
        game_state = self.connection.fetch_state()

        agent_x = game_state.get("agent_x")
        agent_y = game_state.get("agent_y")
        available_keys = game_state.get("available_keys")
        door_dict = game_state.get("door_dict")
        grid_string = game_state.get("grid_string")
        used_keys = game_state.get("used_keys")
        target_keys = game_state.get("target_keys")

        game_map = Env(
            name="The current game map", 
            description=grid_string
        )
        game_map.agent_location = Env(
            name="The agent's current location", 
            description=f"({agent_y}, {agent_x})."
        )
        game_map.door_status = Env(
            name="The door status", 
            description=door_dict
        )
        game_map.available_keys = Env(
            name="The keys you've taken", 
            description=available_keys
        )
        game_map.used_keys = Env(
            name="The current keys", 
            description=used_keys
        )
        game_map.target_keys = Env(
            name="The target keys", 
            description=target_keys
        )

        return game_map

    def escaping(self, *args, **kwargs):
        return escaping(self, *args, **kwargs)


def decision_tree(self, target_keys):
    import time
    self.target_keys = [keys.lower() for keys in target_keys]
    self.connection.update_state({"target_keys": target_keys})
    while True:
        self.game_state = self.connection.fetch_state()
        if self.game_state.get("door_dict", {}).get("open") or not self.game_state:
            self.connection.close()
            break
        self.escaping(show_response=True)
        self.game_map = self.get_game_env()
        time.sleep(2)

escaper = Escaper(decision_tree)
# Note: The target keys must include yellow or blue, cause other colors are not guaranteed to be in the game.
escaper.run(target_keys=["yellow", "blue"])
