import socket
import pygame
import random
from pygame.locals import *
from game_tool import Tool

# Initialize Pygame
pygame.init()

class GameSettings:
    """ Game settings that can be modified based on game requirements. """
    def __init__(self, grid_size, tile_size=64, info_height=100, fps=30):
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.screen_width = self.screen_height = self.tile_size * self.grid_size
        self.info_height = info_height
        self.fps = fps

class Grid:
    """ Class to handle the game grid and game objects like tools and doors. """
    def __init__(self, settings):
        self.settings = settings
        self.grid = [[' ' for _ in range(self.settings.grid_size)] for _ in range(self.settings.grid_size)]
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
            self.grid[y][x] = {'type': 'D', 'open': False}  # Door object with status
        else:
            # Recurse if initial random placement is not empty
            self.place_door()
    
    def place_tools(self):
        # Fixed number of tools with specific properties
        tool1 = Tool("Key", "A key to open doors", "Use this key to unlock doors", True)
        tool2 = Tool("Fake Key", "Looks like a key but does nothing", "Just a decoy", False)
        tool3 = Tool("Note", "A note with confusing instructions", "It says to look under the rug", False)
        tool_positions = random.sample([(x, y) for x in range(self.settings.grid_size) for y in range(self.settings.grid_size) if self.grid[y][x] == ' '], 3)
        self.grid[tool_positions[0][1]][tool_positions[0][0]] = tool1
        self.grid[tool_positions[1][1]][tool_positions[1][0]] = tool2
        self.grid[tool_positions[2][1]][tool_positions[2][0]] = tool3

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
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', port))
        self.server_socket.listen(1)
        print(f"Server started on port {port}")
    
    def run_game(self):
        # Render the initial state before entering the main loop
        self.draw_grid()
        pygame.display.flip()

        connection, address = self.server_socket.accept()
        print("connection, address: ", connection, address)
        print(f"Connected by {address}")
        running = True
        while running:
            for event in pygame.event.get():  # Handle Pygame events to prevent GUI freeze
                if event.type == pygame.QUIT:
                    running = False

            data = connection.recv(1024).decode()
            if data == 'QUIT':
                running = False
            else:
                self.handle_client_data(data, connection)
            self.draw_grid()
            pygame.display.flip()  # Update the display to reflect changes in the grid

        connection.close()
        pygame.quit()
    
    def draw_grid(self):
        """Draw the game grid."""
        self.screen.fill((0, 0, 0))
        for y in range(self.settings.grid_size):
            for x in range(self.settings.grid_size):
                rect = pygame.Rect(x * self.settings.tile_size, y * self.settings.tile_size, self.settings.tile_size, self.settings.tile_size)
                color = (255, 255, 255) if (x, y) == (self.agent_x, self.agent_y) else (200, 200, 200)
                pygame.draw.rect(self.screen, color, rect, 1)
                
                cell = self.grid.grid[y][x]
                text_representation = ' '  # Default empty representation

                if isinstance(cell, Tool):
                    text_representation = 'T'  # Represent tools with 'T'
                elif isinstance(cell, dict) and 'type' in cell:
                    if cell['type'] == 'D':
                        text_representation = 'D'
                elif isinstance(cell, str):
                    text_representation = cell  # Normal cells are just strings like 'W' for walls or ' ' for empty
                
                text = self.font.render(text_representation, True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

    
    def handle_client_data(self, data, connection):
        if data == "GET_STATE":
            # Send the current game state as a serialized JSON
            import json
            state_info = json.dumps(self.get_state_info())
            connection.sendall(state_info.encode())
        else:
            # Assume data is a JSON string with command details
            try:
                command_details = json.loads(data)
                action = command_details['action']
                if action == 'move':
                    dx, dy = command_details['dx'], command_details['dy']
                    self.try_move(dx, dy)
                elif action == 'open':
                    self.try_open_door()
                # Respond with updated state info
                state_info = json.dumps(self.get_state_info())
                connection.sendall(state_info.encode())
            except json.JSONDecodeError:
                connection.sendall(b'Error processing request')


    def try_move(self, dx, dy):
        next_x = self.agent_x + dx
        next_y = self.agent_y + dy
        if self.grid.grid[next_y][next_x] == ' ':
            self.update_position(next_x, next_y)
        elif isinstance(self.grid.grid[next_y][next_x], dict) and self.grid.grid[next_y][next_x]['type'] == 'D' and self.grid.grid[next_y][next_x]['open']:
            self.update_position(next_x, next_y)
            print("Congratulations! You have escaped the room.")
            pygame.quit()  # Ending the game

    def update_position(self, new_x, new_y):
        self.grid.grid[self.agent_y][self.agent_x] = ' '
        self.grid.grid[new_y][new_x] = 'A'
        self.agent_x = new_x
        self.agent_y = new_y

    def try_open_door(self):
        # Check adjacent cells for doors to open
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = self.agent_x + dx, self.agent_y + dy
            if isinstance(self.grid.grid[ny][nx], dict) and self.grid.grid[ny][nx]['type'] == 'D':
                self.grid.grid[ny][nx]['open'] = True
                print("Door opened.")

    def get_state_info(self):
        info = "Agent's current status:\n"
        # Collect data on surrounding cells
        directions = {'North': (-1, 0), 'South': (1, 0), 'East': (0, 1), 'West': (0, -1)}
        for direction, (dx, dy) in directions.items():
            nx, ny = self.agent_x + dx, self.agent_y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                cell = self.grid.grid[ny][nx]
                if isinstance(cell, dict):
                    info += f"{direction}: {cell['type']} - {cell['name']} ({cell['description']})\n"
                else:
                    info += f"{direction}: {cell}\n"
        return info

# Running the server
if __name__ == "__main__":
    Game(5).run_game()
