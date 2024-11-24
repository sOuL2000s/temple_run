import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Temple Run 2D")

# Load assets
runner_image = pygame.image.load(r"D:\72 projects of python\temple_run\runner.png")  # Replace with your runner sprite
obstacle_image = pygame.image.load(r"D:\72 projects of python\temple_run\obstacle.png")  # Replace with an obstacle sprite
coin_image = pygame.image.load(r"D:\72 projects of python\temple_run\coin.png")  # Replace with a coin sprite

# Scale images
runner_image = pygame.transform.scale(runner_image, (50, 80))
obstacle_image = pygame.transform.scale(obstacle_image, (30, 30))  # Make the obstacle smaller
coin_image = pygame.transform.scale(coin_image, (30, 30))

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
scroll_speed = 5
runner_x, runner_y = WIDTH // 5, HEIGHT - 150
runner_width, runner_height = runner_image.get_width(), runner_image.get_height()
gravity = 1
jump_height = -15
velocity_y = 0
ground_y = HEIGHT - 100
score = 0
game_over = False

# Obstacles and coins
obstacles = []
coins = []
obstacle_spawn_time = 0
coin_spawn_time = 0

# Runner hitbox
runner_rect = pygame.Rect(runner_x, runner_y, runner_width, runner_height)


def spawn_obstacle():
    """Spawns a new obstacle."""
    x = WIDTH
    y = ground_y - obstacle_image.get_height()
    obstacles.append(pygame.Rect(x, y, obstacle_image.get_width(), obstacle_image.get_height()))


def spawn_coin():
    """Spawns a new coin."""
    x = WIDTH
    y = random.randint(ground_y - 200, ground_y - 50)
    coins.append(pygame.Rect(x, y, coin_image.get_width(), coin_image.get_height()))


def draw_game():
    """Draws all game elements on the screen."""
    screen.fill(WHITE)

    # Draw ground
    pygame.draw.rect(screen, GREEN, (0, ground_y, WIDTH, HEIGHT - ground_y))

    # Draw runner
    screen.blit(runner_image, (runner_x, runner_y))

    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))

    # Draw coins
    for coin in coins:
        screen.blit(coin_image, (coin.x, coin.y))

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Game Over
    if game_over:
        over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(over_text, (WIDTH // 4, HEIGHT // 2))


# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_r:
                # Restart the game
                game_over = False
                runner_y = HEIGHT - 150
                velocity_y = 0
                obstacles.clear()
                coins.clear()
                score = 0

    # Check for input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and runner_y == ground_y - runner_height:
        velocity_y = jump_height

    # Apply gravity
    velocity_y += gravity
    runner_y += velocity_y

    # Prevent falling below the ground
    if runner_y >= ground_y - runner_height:
        runner_y = ground_y - runner_height

    # Update runner hitbox
    runner_rect.topleft = (runner_x, runner_y)

    # Spawn obstacles and coins
    obstacle_spawn_time += 1
    coin_spawn_time += 1

    if obstacle_spawn_time > 90:  # Adjust spawn frequency
        spawn_obstacle()
        obstacle_spawn_time = 0

    if coin_spawn_time > 120:  # Adjust spawn frequency
        spawn_coin()
        coin_spawn_time = 0

    # Move obstacles
    for obstacle in obstacles[:]:
        obstacle.x -= scroll_speed
        if obstacle.x + obstacle.width < 0:
            obstacles.remove(obstacle)

    # Move coins
    for coin in coins[:]:
        coin.x -= scroll_speed
        if coin.x + coin.width < 0:
            coins.remove(coin)

    # Check for collisions with obstacles
    for obstacle in obstacles:
        if runner_rect.colliderect(obstacle):
            game_over = True

    # Check for collisions with coins
    for coin in coins[:]:
        if runner_rect.colliderect(coin):
            score += 10
            coins.remove(coin)

    # Draw everything
    draw_game()

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)
