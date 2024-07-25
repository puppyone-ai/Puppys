import json
import socket
import pygame
import random
import time
# from pygame.locals import *
from escape_tools import Key, Hammer, Cup

# Initialize Pygame
pygame.init()

class GameSettings:
    """ Set the Game settings. """
    def __init__(self, grid_size, tile_size=64, info_height=100, fps=30):
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.screen_width = self.screen_height = self.tile_size * self.grid_size
        self.info_height = info_height
        self.fps = fps

class Grid:
    """ Define the game grid and game objects like tools and doors. """
    def __init__(self, settings):
        self.settings = settings
        self.grid = [[' ' for _ in range(self.settings.grid_size)] for _ in range(self.settings.grid_size)]
        self.door_dict = {}
        self.populate_grid()
    
    def place_walls(self):
        num_walls = random.randint(1, min(5, self.settings.grid_size//2))
        for _ in range(num_walls):
            x, y = random.randint(0, self.settings.grid_size-1), random.randint(0, self.settings.grid_size-1)
            self.grid[y][x] = 'W'
    
    def place_door(self):
        """ Places a door randomly on the boundary of the grid with a status (True for open, False for closed). """
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            x = random.randint(0, self.settings.grid_size - 1)
            y = 0
        elif edge == 'bottom':
            x = random.randint(0, self.settings.grid_size - 1)
            y = self.settings.grid_size - 1
        elif edge == 'left':
            x = 0
            y = random.randint(0, self.settings.grid_size - 1)
        elif edge == 'right':
            x = self.settings.grid_size - 1
            y = random.randint(0, self.settings.grid_size - 1)

        # Check if selected boundary cell is empty before placing the door
        if self.grid[y][x] == ' ':
            self.door_dict = {"x": x, "y": y, "open": False}
            self.grid[y][x] = 'D'
        else:
            # Recurse if initial random placement is not empty
            self.place_door()
    
    def place_tools(self, number = 3):
        # Fixed number of tools with specific properties
        tool_positions = random.sample([(x, y) for x in range(self.settings.grid_size) for y in range(self.settings.grid_size) if self.grid[y][x] == ' '], number)
        self.grid[tool_positions[0][1]][tool_positions[0][0]] = Key.serialize()
        self.grid[tool_positions[1][1]][tool_positions[1][0]] = Hammer.serialize()
        self.grid[tool_positions[2][1]][tool_positions[2][0]] = Cup.serialize()

    def populate_grid(self):
        self.place_walls()
        self.place_door()
        self.place_tools()

    def get_start_position(self):
        while True:
            x, y = random.randint(0, self.settings.grid_size-1), random.randint(0, self.settings.grid_size-1)
            if self.grid[y][x] == ' ':
                self.grid[y][x] = 'A'
                return x, y

class Game:
    def __init__(self, grid_size, font_size=36, info_font_size=20, port=5555):
        self.grid_size = grid_size
        self.settings = GameSettings(grid_size)
        self.grid = Grid(self.settings)
        self.agent_x, self.agent_y = self.grid.get_start_position()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height + self.settings.info_height))
        self.font = pygame.font.Font(None, font_size)
        self.info_font = pygame.font.Font(None, info_font_size)
        self.available_tools = []
        self.usefulness = 0
        self.target_usefulness = 0
        self.current_action_string = ""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(1)
        print(f"Server started on port {port}")

    def run_game(self):
        # Initialize the display with the initial state
        self.draw_grid()
        self.draw_messages()
        pygame.display.flip()

        # Establish a connection
        connection, address = self.server_socket.accept()
        print(f"Connected by {connection}, {address}")

        # Main game loop
        running = True
        while running:
            # Receive and process data from the client
            data = connection.recv(4096).decode('utf-8')
            running = self.handle_client_data(data, connection)

            # Update display
            self.draw_grid()
            self.draw_messages()
            pygame.display.flip()
            
            # # Process all pygame events
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False
            
            time.sleep(2)

        # Clean up and close the game
        connection.close()
        pygame.quit()
    
    def print_grid(self):
        grid_string = f"The dimension of the grid: {self.grid_size}\n"
        for y in range(self.settings.grid_size):
            for x in range(self.settings.grid_size):
                cell = self.grid.grid[y][x]
                if cell != ' ':
                    grid_string += f"In row {y} and column {x}: "
                    if isinstance(cell, dict):
                        name, description, usefulness = cell.get("name", ""), cell.get("description", ""), cell.get("usefulness", 0)
                        tool_info = f"`{name}` - {description}; Usefulness Score: {usefulness}"
                        grid_string += "tool " + tool_info
                    elif cell == 'D':
                        grid_string += "door"
                    elif cell == "A":
                        grid_string += "agent"
                    elif cell == "W":
                        grid_string += "wall"
                    grid_string += "\n"
        return grid_string
    
    def draw_grid(self):
        """Draw the game grid."""
        self.screen.fill((0, 0, 0))
        for y in range(self.settings.grid_size):
            for x in range(self.settings.grid_size):
                rect = pygame.Rect(x * self.settings.tile_size, y * self.settings.tile_size, self.settings.tile_size, self.settings.tile_size)
                color = (255, 255, 255) if (x, y) == (self.agent_x, self.agent_y) else (200, 200, 200)
                pygame.draw.rect(self.screen, color, rect, 1)

                cell = self.grid.grid[y][x]
                text_representation = cell

                if isinstance(cell, dict):
                    text_representation = 'T'

                text = self.font.render(text_representation, True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
    
    def draw_messages(self):
        # Define starting position for text rendering with a downward offset
        offset = 30
        start_y = self.settings.screen_height + offset
        line_height = 20

        # Display the current action message
        action_rect = pygame.Rect(0, start_y - offset, self.settings.screen_width, self.settings.info_height + offset)
        pygame.draw.rect(self.screen, (0, 0, 0), action_rect)

        # Append additional info to current action string
        self.current_action_string += f"\nCurrent Usefulness: {self.usefulness}\nTarget Usefulness: {self.target_usefulness}"

        # Split the message into lines
        lines = self.current_action_string.split('\n')

        for i, line in enumerate(lines):
            action_text = self.info_font.render(line, True, (255, 253, 208))
            action_text_rect = action_text.get_rect(center=(self.settings.screen_width // 2, start_y + i * line_height))
            self.screen.blit(action_text, action_text_rect)

        # Reset the current action string after displaying
        self.current_action_string = ""
    
    def print_available_tools(self):
        tools_string = ""
        for tool in self.available_tools:
            if isinstance(tool, dict):
                name, description, usefulness = tool.get("name", ""), tool.get("description", ""), tool.get("usefulness", 0)
                tool_info = f"`{name}` - {description}; Usefulness Score: {usefulness}"
                tools_string += tool_info + "\n"
        return tools_string

    def handle_client_data(self, data, connection):
        # Check if data is empty
        if not data:
            print("No data received.")
            return True

        if data == "GET_STATE":
            self.handle_get_state(connection)
            return True

        return self.handle_push_state(connection, data)

    def handle_get_state(self, connection):
        # Send the current game state as a serialized JSON
        shared_info = {
            "grid": self.grid.grid, 
            "agent_x": self.agent_x,
            "agent_y": self.agent_y,
            "available_tools": self.available_tools,
            "door_dict": self.grid.door_dict,
            "grid_string": self.print_grid(),
            "tools": self.print_available_tools(),
            "usefulness": self.usefulness
        }
        state_info = json.dumps(shared_info)
        connection.sendall(state_info.encode())
    
    def handle_push_state(self, connection, data):
        try:
            # Update the game state based on client data
            shared_info = json.loads(data)
            print("shared_info: ", shared_info)
            
            connection.sendall(b"State updated.")
            # The first time the client sends message
            if "target_usefulness" in shared_info:
                self.target_usefulness = shared_info.get("target_usefulness")
            # Normal update when agent moves or uses a tool
            else:
                # print("else")
                self.grid.door_dict = shared_info.get("door_dict")
                # Exit the game if the door is open
                if self.grid.door_dict["open"]:
                    self.win()
                    return False
                else:
                    self.grid.grid = shared_info.get("grid")
                    self.agent_x = shared_info.get("agent_x")
                    self.agent_y = shared_info.get("agent_y")
                    self.available_tools = shared_info.get("available_tools")
                    self.current_action_string = shared_info.get("current_action_string")
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON data: {e}")
        
        return True
            

    def win(self):
        win_rect = pygame.Rect(0, self.settings.screen_height, self.settings.screen_width, self.settings.info_height)
        win_font = pygame.font.Font(None, 40)
        win_message = "Congratulations! You've escaped the room!"
        win_text = win_font.render(win_message, True, (0, 0, 0))
        win_text_rect = win_text.get_rect(center=win_rect.center)
        self.screen.blit(win_text, win_text_rect)


# Running the server
if __name__ == "__main__":
    Game(5).run_game()
