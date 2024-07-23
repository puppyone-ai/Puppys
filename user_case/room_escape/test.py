import random

class Cell:
    def __init__(self, content=None):
        self.content = content

    def __str__(self):
        return self.content.symbol if self.content else ' '

class Tool:
    def __init__(self, name, description, action_guide, useful=False):
        self.name = name
        self.description = description
        self.action_guide = action_guide
        self.useful = useful
        self.symbol = 'T'

class Agent:
    def __init__(self, location):
        self.location = location
        self.inventory = []
        self.symbol = 'A'

    def move(self, direction, grid):
        x, y = self.location
        if direction == 'up' and x > 0:
            new_loc = (x-1, y)
        elif direction == 'down' and x < len(grid)-1:
            new_loc = (x+1, y)
        elif direction == 'left' and y > 0:
            new_loc = (x, y-1)
        elif direction == 'right' and y < len(grid[0])-1:
            new_loc = (x, y+1)
        else:
            return False  # Invalid move
        if isinstance(grid[new_loc[0]][new_loc[1]].content, Tool) or grid[new_loc[0]][new_loc[1]].content is None:
            self.location = new_loc
            return True
        return False

    def interact(self, grid):
        cell = grid[self.location[0]][self.location[1]]
        if isinstance(cell.content, Tool):
            tool = cell.content
            print(f"Interacting with {tool.name}: {tool.description}")
            if tool.useful:
                print(tool.action_guide)
                self.inventory.append(tool)
                cell.content = None  # Remove the tool from the map
                return True
            else:
                print("This tool is not useful.")
        return False

class Game:
    def __init__(self, dimension):
        self.dimension = dimension
        self.grid = [[Cell() for _ in range(dimension)] for _ in range(dimension)]
        self.agent = Agent((0, 0))  # Start at top-left corner
        self.setup_game()

    def setup_game(self):
        # Place the agent
        self.grid[0][0].content = self.agent
        # Place the exit
        self.grid[-1][-1].content = Cell('Exit')
        # Randomly place tools
        num_tools = random.randint(1, self.dimension)  # At least one tool must be useful
        for _ in range(num_tools):
            x, y = random.randint(0, self.dimension-1), random.randint(0, self.dimension-1)
            if self.grid[x][y].content is None:  # Only place a tool if the cell is empty
                self.grid[x][y].content = Tool("Key", "A key to open the door", "Use this key at the door to escape.", useful=True)

    def display_map(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))

    def play(self):
        while True:
            self.display_map()
            command = input("Enter command (up, down, left, right, interact, quit): ")
            if command in ['up', 'down', 'left', 'right']:
                self.agent.move(command, self.grid)
            elif command == 'interact':
                self.agent.interact(self.grid)
            elif command == 'quit':
                break

# Example of how to start the game
game = Game(5)
game.play()
