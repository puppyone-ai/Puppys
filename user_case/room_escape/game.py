import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

class GameSettings:
    """ Game settings that can be modified based on game requirements. """
    def __init__(self, grid_size, tile_size = 64, info_height = 100, fps = 30):
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
        """ Places a door randomly on the boundary of the grid. """
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
            self.grid[y][x] = 'D'
        else:
            # Recurse if initial random placement is not empty
            self.place_door()
    
    def place_tools(self):
        for _ in range(random.randint(1, 3)):
            while True:
                x, y = random.randint(0, self.settings.grid_size-1), random.randint(0, self.settings.grid_size-1)
                if self.grid[y][x] == ' ':
                    self.grid[y][x] = 'T'  # Placeholder, should create tool objects
                    break


    def populate_grid(self):
        # Randomly place walls
        self.place_walls()

        # Place the door
        self.place_door()

        # Place tools
        self.place_tools()
       

    def get_start_position(self):
        # Place the agent
        while True:
            x, y = random.randint(0, self.settings.grid_size-1), random.randint(0, self.settings.grid_size-1)
            if self.grid[y][x] == ' ':
                self.grid[y][x] = 'A'
                return x, y

class Game:
    def __init__(self, grid_size, font_size = 36, info_font_size = 20):
        self.grid_size = grid_size
        self.settings = GameSettings(grid_size)
        self.grid = Grid(self.settings)
        self.agent_x, self.agent_y = self.grid.get_start_position()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height + self.settings.info_height))
        pygame.display.set_caption("Room Escape Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, font_size)
        self.info_font = pygame.font.Font(None, info_font_size)
        self.current_action = "Welcome to the Room Escape Game!"
        self.run_game()
    
    def generate_grid(self):
        # Initialization, return an empty grid and a default position
        return [[' ' for _ in range(self.grid_size)] for _ in range(self.grid_size)], 0, 0

    def handle_keypress(self, event):
        # Adjust agent movement based on key press and update current_action accordingly
        if event.key in (K_UP, K_w) and self.agent_y > 0:
            self.try_move(0, -1, "Moving up.")
        elif event.key in (K_DOWN, K_s) and self.agent_y < self.grid_size - 1:
            self.try_move(0, 1, "Moving down.")
        elif event.key in (K_LEFT, K_a) and self.agent_x > 0:
            self.try_move(-1, 0, "Moving left.")
        elif event.key in (K_RIGHT, K_d) and self.agent_x < self.grid_size - 1:
            self.try_move(1, 0, "Moving right.")

    def try_move(self, dx, dy, action):
        # Check if the next position is empty or contains a tool
        next_x = self.agent_x + dx
        next_y = self.agent_y + dy
        if self.grid.grid[next_y][next_x] == ' ':
            self.update_position(next_x, next_y)
            self.current_action = action
        elif self.grid.grid[next_y][next_x] == 'T':
            self.update_position(next_x, next_y)
            self.current_action = action + ", taking the tool."

    def update_position(self, new_x, new_y):
        # Move the agent on the grid
        self.grid.grid[self.agent_y][self.agent_x] = ' '
        self.grid.grid[new_y][new_x] = 'A'
        self.agent_x = new_x
        self.agent_y = new_y

    def draw_grid(self):
        self.screen.fill((0, 0, 0))
        for y in range(self.settings.grid_size):
            for x in range(self.settings.grid_size):
                rect = pygame.Rect(x*self.settings.tile_size, y*self.settings.tile_size, self.settings.tile_size, self.settings.tile_size)
                color = (255, 255, 255) if (x, y) == (self.agent_x, self.agent_y) else (200, 200, 200)
                pygame.draw.rect(self.screen, color, rect, 1)
                text = self.font.render(self.grid.grid[y][x], True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
        
        # Display the current action message
        action_rect = pygame.Rect(0, self.settings.screen_height, self.settings.screen_width, self.settings.info_height)
        pygame.draw.rect(self.screen, (173, 216, 230), action_rect)
        action_text = self.info_font.render(self.current_action, True, (0, 0, 0))
        action_text_rect = action_text.get_rect(center=action_rect.center)
        self.screen.blit(action_text, action_text_rect)

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    self.handle_keypress(event)
                elif event.type == TEXTINPUT:
                    continue
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(self.settings.fps)
        pygame.quit()


# Usage
if __name__ == "__main__":
    Game(5)
