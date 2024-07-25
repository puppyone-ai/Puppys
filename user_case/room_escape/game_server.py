import time
import json
import socket
import pygame
import random

# Initialize Pygame
pygame.init()

class GameSettings:
    """ Set the Game settings. """
    def __init__(self, grid_size: int, tile_size: int = 64, info_height: int = 100, fps: int = 30):
        self.tile_size = tile_size
        self.grid_size = grid_size
        self.screen_width = self.screen_height = self.tile_size * self.grid_size
        self.info_height = info_height
        self.fps = fps

class Grid:
    """ Define the game grid and game objects like tools and doors. """
    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.grid = [[' ' for _ in range(self.settings.grid_size)] for _ in range(self.settings.grid_size)]
        self.door_dict = {}
        self.populate_grid()
    
    def place_walls(self) -> None:
        num_walls = random.randint(1, min(5, self.settings.grid_size//2))
        for _ in range(num_walls):
            x, y = random.randint(0, self.settings.grid_size-1), random.randint(0, self.settings.grid_size-1)
            self.grid[y][x] = 'Wall'
    
    def place_door(self) -> None:
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
            self.grid[y][x] = 'Door'
        else:
            # Recurse if initial random placement is not empty
            self.place_door()

    def place_tools(self) -> None:
        num_tools = random.randint(2, self.settings.grid_size)
        tool_positions = random.sample([(x, y) for x in range(self.settings.grid_size) for y in range(self.settings.grid_size) if self.grid[y][x] == ' '], num_tools)
        possible_usefulness = [0, 0.1, 0.5, 1]
        self.grid[tool_positions[0][1]][tool_positions[0][0]] = {'name': 'Tool 1', 'usefulness': 0.1}
        for i in range(1, num_tools):
            self.grid[tool_positions[i][1]][tool_positions[i][0]] = {'name': f"Tool {i + 1}", 'usefulness': random.choice(possible_usefulness)}

    def populate_grid(self) -> None:
        self.place_walls()
        self.place_door()
        self.place_tools()

    def get_start_position(self) -> tuple:
        while True:
            x, y = random.randint(0, self.settings.grid_size-1), random.randint(0, self.settings.grid_size-1)
            if self.grid[y][x] == ' ':
                self.grid[y][x] = 'Agent'
                return x, y

class Game:
    def __init__(self, grid_size: int, font_size: int = 30, info_font_size: int = 22, tool_info_width: int = 150, port: int = 5555):
        self.grid_size = grid_size
        self.settings = GameSettings(grid_size)
        self.grid = Grid(self.settings)
        self.agent_x, self.agent_y = self.grid.get_start_position()
        self.tool_info_width = tool_info_width
        self.screen = pygame.display.set_mode((self.settings.screen_width + self.tool_info_width, self.settings.screen_height + self.settings.info_height))
        self._load_emoji_images()
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

    def run_game(self) -> None:
        # Initialize the display with the initial state
        self._draw_grid()
        pygame.display.flip()
        
        # Establish a connection
        connection, address = self.server_socket.accept()
        print(f"Connected by {connection}, {address}")

        # Main game loop
        running = True
        
        while running:
            # Check for Pygame events before blocking operations
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

            # Non-blocking check if a client is connected
            try:
                connection.settimeout(0.1)
                data = connection.recv(4096).decode('utf-8')
                if data:
                    running = self._handle_client_data(data, connection)
            except socket.timeout:
                time.sleep(1)
            except ConnectionResetError:
                connection.close()
                try:
                    connection, address = self.server_socket.accept()
                    print(f"Reconnected by {address}")
                except socket.timeout:
                    print("Waiting for new client connections...")
                    time.sleep(1)

            # Update display
            self._draw_grid()
            pygame.display.flip()

        # Clean up and close the game
        time.sleep(2)
        connection.close()
        pygame.quit()

    def _load_emoji_images(self):
        size = (self.settings.tile_size - 10, self.settings.tile_size - 10)
        self.emoji_images = {
            'Agent': pygame.transform.scale(pygame.image.load('user_case/room_escape/assets/agent.png'), size),
            'Wall': pygame.transform.scale(pygame.image.load('user_case/room_escape/assets/wall.png'), size),
            'Door': pygame.transform.scale(pygame.image.load('user_case/room_escape/assets/door.png'), size),
            'Tool': pygame.transform.scale(pygame.image.load('user_case/room_escape/assets/tool.png'), size),
            'D&A': pygame.transform.scale(pygame.image.load('user_case/room_escape/assets/agentatdoor.png'), size)
        }

    def _draw_grid(self) -> None:
        self.screen.fill((0, 0, 0))
        for y in range(self.settings.grid_size):
            for x in range(self.settings.grid_size):
                rect = pygame.Rect(x * self.settings.tile_size, y * self.settings.tile_size, self.settings.tile_size, self.settings.tile_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)

                cell = self.grid.grid[y][x]
                # Determine which image to use based on the cell content
                if isinstance(cell, dict):
                    image = self.emoji_images['Tool']
                else:
                    image = self.emoji_images.get(cell, None)

                if image:
                    # Center the image in the rectangle
                    image_rect = image.get_rect(center=rect.center)
                    self.screen.blit(image, image_rect)
        
        self._draw_tool_info()
        self._draw_messages()

    def _draw_tool_info(self) -> None:
        start_x = self.settings.screen_width + 0
        start_y = 10
        width = self.tool_info_width
        height = self.settings.screen_height

        # Define the tool info rectangle and draw it
        tool_info_rect = pygame.Rect(start_x, start_y, width, height)
        pygame.draw.rect(self.screen, (0, 0, 0), tool_info_rect)

        # Display the title for the tool section
        title_text = self.info_font.render("Tools: Usefulness", True, (255, 167, 61))
        title_rect = title_text.get_rect(center=(start_x + width // 2, start_y + 20))
        self.screen.blit(title_text, title_rect)

        # Display each available tool and its usefulness
        line_height = 30
        for index, tool in enumerate(self.available_tools):
            tool_name = tool.get("name", "Unknown")
            usefulness_score = tool.get("usefulness", 0)
            tool_text = self.info_font.render(f"{tool_name}: {usefulness_score}", True, (69, 153, 223))
            tool_text_rect = tool_text.get_rect(center=(start_x + width // 2, start_y + 50 + index * line_height))
            self.screen.blit(tool_text, tool_text_rect)

    def _draw_messages(self) -> None:
        # Define starting position for text rendering with a downward offset
        offset = 30
        start_y = self.settings.screen_height + offset
        line_height = 20

        # Display the current action message
        action_rect = pygame.Rect(0, start_y - offset, self.settings.screen_width, self.settings.info_height + offset)
        pygame.draw.rect(self.screen, (0, 0, 0), action_rect)

        # Split the message into lines
        lines = self.current_action_string.split('\n')

        for i, line in enumerate(lines):
            action_text = self.info_font.render(line, True, (69, 153, 223))
            action_text_rect = action_text.get_rect(center=(self.settings.screen_width // 2, start_y + i * line_height))
            self.screen.blit(action_text, action_text_rect)

    def _handle_client_data(self, data: any, connection: socket) -> bool:
        # Check if data is empty
        if not data:
            print("No data received.")
            return True

        if isinstance(data, str) and data == "GET_STATE":
            self._handle_get_state(connection)
            return True

        return self._handle_push_state(connection, data)

    def _handle_get_state(self, connection: socket) -> None:
        # Send the current game state as a serialized JSON
        shared_info = {
            "grid": self.grid.grid, 
            "agent_x": self.agent_x,
            "agent_y": self.agent_y,
            "available_tools": self.available_tools,
            "door_dict": self.grid.door_dict,
            "grid_string": self._print_grid(),
            "tools": self._print_available_tools(),
            "usefulness": self.usefulness
        }
        state_info = json.dumps(shared_info)
        connection.sendall(state_info.encode())

    def _handle_push_state(self, connection: socket, data: dict) -> bool:
        try:
            # Update the game state based on client data
            shared_info = json.loads(data)
            print("Updated data: ", shared_info)
            connection.sendall(b"State updated.")
            # The first time the client sends message
            if "target_usefulness" in shared_info:
                self.target_usefulness = shared_info.get("target_usefulness")
            # Normal update when agent moves or uses a tool
            else:
                self.grid.door_dict = shared_info.get("door_dict")
                # Exit the game if the door is open
                if self.grid.door_dict["open"]:
                    self.current_action_string = "Congratulations! You've escaped the room!"
                    return False
                else:
                    self.grid.grid = shared_info.get("grid")
                    self.agent_x = shared_info.get("agent_x")
                    self.agent_y = shared_info.get("agent_y")
                    self.available_tools = shared_info.get("available_tools")
                    self.usefulness = shared_info.get("usefulness")
                    self.current_action_string = shared_info.get("current_action_string")
                    self.current_action_string += f"\nCurrent Usefulness: {shared_info.get('usefulness')}\nTarget Usefulness: {self.target_usefulness}"
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON data: {e}")

        return True

    def _print_grid(self) -> str:
        grid_string = f"Grid Dimension: {self.grid_size}\n"
        for y in range(self.settings.grid_size):
            for x in range(self.settings.grid_size):
                cell = self.grid.grid[y][x]
                if cell != ' ':
                    grid_string += f"In row {y} and column {x}: "
                    if isinstance(cell, dict):
                        name, usefulness = cell.get("name", ""), cell.get("usefulness", 0)
                        grid_string += f"Tool `{name}`; Usefulness: {usefulness}"
                    elif cell == 'D&A':
                        grid_string += "Both Agent and Door"
                    else:
                        grid_string += cell
                    grid_string += "\n"
        return grid_string

    def _print_available_tools(self) -> str:
        tools_string = ""
        for tool in self.available_tools:
            if isinstance(tool, dict):
                name, usefulness = tool.get("name", ""), tool.get("usefulness", 0)
                tools_string += f"`{name}`; Usefulness: {usefulness}\n"
        return tools_string


# Running the server
if __name__ == "__main__":
    Game(7).run_game()
