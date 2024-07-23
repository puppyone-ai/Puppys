import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
TILE_SIZE = 64
GRID_SIZE = 5
SCREEN_WIDTH = SCREEN_HEIGHT = TILE_SIZE * GRID_SIZE
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Font
font = pygame.font.Font(None, 36)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Room Escape Game")
clock = pygame.time.Clock()

def generate_grid():
    """ Generate the game grid with obstacles, doors, tools, and the agent's start position. """
    grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Randomly place walls
    num_walls = random.randint(1, 5)
    for _ in range(num_walls):
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        grid[y][x] = 'W'

    # Place the door
    while True:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[y][x] == ' ':
            grid[y][x] = 'D'
            break

    # Place tools
    for _ in range(random.randint(1, 3)):  # at least one tool must be useful
        while True:
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if grid[y][x] == ' ':
                grid[y][x] = 'T'
                break

    # Place the agent
    while True:
        x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if grid[y][x] == ' ':
            grid[y][x] = 'A'
            return grid, x, y

def draw_grid(grid, agent_x, agent_y):
    """ Draw the grid on the screen using text. """
    screen.fill(BLACK)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = WHITE if (x, y) == (agent_x, agent_y) else GRAY
            pygame.draw.rect(screen, color, rect, 1)  # Draw the tile
            text = font.render(grid[y][x], True, WHITE)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

grid, agent_x, agent_y = generate_grid()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key in (K_UP, K_w) and agent_y > 0:
                if grid[agent_y - 1][agent_x] == ' ':
                    grid[agent_y][agent_x], agent_y = ' ', agent_y - 1
            elif event.key in (K_DOWN, K_s) and agent_y < GRID_SIZE - 1:
                if grid[agent_y + 1][agent_x] == ' ':
                    grid[agent_y][agent_x], agent_y = ' ', agent_y + 1
            elif event.key in (K_LEFT, K_a) and agent_x > 0:
                if grid[agent_y][agent_x - 1] == ' ':
                    grid[agent_y][agent_x], agent_x = ' ', agent_x - 1
            elif event.key in (K_RIGHT, K_d) and agent_x < GRID_SIZE - 1:
                if grid[agent_y][agent_x + 1] == ' ':
                    grid[agent_y][agent_x], agent_x = ' ', agent_x + 1
            grid[agent_y][agent_x] = 'A'

    draw_grid(grid, agent_x, agent_y)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
