import tkinter as tk
import random
from collections import namedtuple

Tool = namedtuple('Tool', ['name', 'description', 'usage', 'x', 'y', 'actions'])
Action = namedtuple('Action', ['name', 'description', 'control'])

class GameMap:
    def __init__(self, dimension):
        self.dimension = dimension
        self.grid = [[' ' for _ in range(dimension)] for _ in range(dimension)]
        self.tools = []
        self.doors = []

    def place_object(self, symbol, x, y):
        self.grid[y][x] = symbol

    def add_tool(self, tool):
        self.tools.append(tool)
        self.place_object('T', tool.x, tool.y)

    def add_door(self, x, y):
        self.doors.append((x, y))
        self.place_object('D', x, y)

    def is_position_empty(self, x, y):
        return self.grid[y][x] == ' '

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []

    def move(self, dx, dy, game_map):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < game_map.dimension and 0 <= new_y < game_map.dimension and game_map.is_position_empty(new_x, new_y):
            game_map.grid[self.y][self.x] = ' '
            self.x = new_x
            self.y = new_y
            return True
        return False

    def pick_up(self, tool):
        self.inventory.append(tool)

class Game:
    def __init__(self, dimension):
        self.dimension = dimension
        self.root = tk.Tk()
        self.root.title("Room Escape Game")
        self.game_map = GameMap(dimension)
        self.agent = Agent(dimension // 2, dimension // 2)
        self.setup_game(dimension)
        self.cells = [[tk.Button for _ in range(dimension)] for _ in range(dimension)]
        self.init_ui()

    def setup_game(self, dimension):
        self.game_map.place_object('A', self.agent.x, self.agent.y)
        num_doors = random.randint(1, 3)
        for _ in range(num_doors):
            x, y = self.random_empty_position()
            self.game_map.add_door(x, y)

        num_tools = random.randint(1, 5)  # At least one useful tool
        for _ in range(num_tools):
            x, y = self.random_empty_position()
            if _ == 0:  # Ensure at least one useful tool
                tool_type = 'useful'
            else:
                tool_type = random.choice(['useful', 'confusing'])
            tool = self.generate_tool(x, y, tool_type)
            self.game_map.add_tool(tool)

    def generate_tool(self, x, y, tool_type):
        name = 'Key' if tool_type == 'useful' else 'Fake Key'
        description = 'Opens a door' if tool_type == 'useful' else 'Looks like a key but does nothing'
        usage = 'Unlock' if tool_type == 'useful' else 'Try to unlock'
        actions = [Action('Pick Up', 'Pick up the tool', 'click'), Action('Drop', 'Leave the tool', 'click')]
        return Tool(name, description, usage, x, y, actions)

    def random_empty_position(self):
        while True:
            x, y = random.randint(0, self.dimension - 1), random.randint(0, self.dimension - 1)
            if self.game_map.is_position_empty(x, y):
                return x, y

    def init_ui(self):
        game_frame = tk.Frame(self.root)
        game_frame.pack()

        for y in range(self.dimension):
            for x in range(self.dimension):
                cell = tk.Button(game_frame, text=self.game_map.grid[y][x], height=3, width=5)
                cell.grid(row=y, column=x)
                self.cells[y][x] = cell

        self.root.bind("<KeyPress>", self.key_press)
        self.update_ui()

    def update_ui(self):
        for y in range(self.dimension):
            for x in range(self.dimension):
                self.cells[y][x]['text'] = self.game_map.grid[y][x]
        self.cells[self.agent.y][self.agent.x]['text'] = 'A'

    def key_press(self, event):
        if event.keysym == 'Up':
            self.agent.move(0, -1, self.game_map)
        elif event.keysym == 'Down':
            self.agent.move(0, 1, self.game_map)
        elif event.keysym == 'Left':
            self.agent.move(-1, 0, self.game_map)
        elif event.keysym == 'Right':
            self.agent.move(1, 0, self.game_map)
        self.update_ui()

    def run_game(self):
        self.root.mainloop()

if __name__ == '__main__':
    game = Game(5)
    game.run_game()
