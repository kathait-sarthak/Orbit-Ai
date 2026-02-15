import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Orbit Defender")

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player properties
PLAYER_SIZE = 50
PLAYER_SPEED = 5
player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
player_y = SCREEN_HEIGHT - PLAYER_SIZE - 10
player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

# Bullet properties
BULLET_SIZE = 10
BULLET_SPEED = 10
bullets = [] # List to hold active bullets

# Target properties
TARGET_SIZE = 40
TARGET_SPEED = 3
TARGET_SPAWN_RATE = 1000 # milliseconds
targets = [] # List to hold active targets
last_target_spawn_time = pygame.time.get_ticks()

# Game variables
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a new bullet at the player's center
                bullet_rect = pygame.Rect(
                    player_rect.centerx - BULLET_SIZE // 2,
                    player_rect.top,
                    BULLET_SIZE,
                    BULLET_SIZE
                )
                bullets.append(bullet_rect)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
        player_rect.x += PLAYER_SPEED

    # Bullet movement and removal
    for bullet in bullets:
        bullet.y -= BULLET_SPEED
    bullets = [bullet for bullet in bullets if bullet.bottom > 0]

    # Target spawning
    current_time = pygame.time.get_ticks()
    if current_time - last_target_spawn_time > TARGET_SPAWN_RATE:
        target_x = random.randint(0, SCREEN_WIDTH - TARGET_SIZE)
        target_y = -TARGET_SIZE # Start above the screen
        target_rect = pygame.Rect(target_x, target_y, TARGET_SIZE, TARGET_SIZE)
        targets.append(target_rect)
        last_target_spawn_time = current_time

    # Target movement and removal
    for target in targets:
        target.y += TARGET_SPEED
    targets = [target for target in targets if target.top < SCREEN_HEIGHT]

    # Collision detection (bullet-target)
    bullets_to_remove = []
    targets_to_remove = []

    for bullet in bullets:
        for target in targets:
            if bullet.colliderect(target):
                bullets_to_remove.append(bullet)
                targets_to_remove.append(target)
                score += 10 # Increase score on hit
        
    # Remove hit bullets and targets
    bullets = [b for b in bullets if b not in bullets_to_remove]
    targets = [t for t in targets if t not in targets_to_remove]

    # Drawing
    SCREEN.fill(BLACK) # Clear the screen

    # Draw player
    pygame.draw.rect(SCREEN, BLUE, player_rect)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(SCREEN, WHITE, bullet)

    # Draw targets
    for target in targets:
        pygame.draw.rect(SCREEN, RED, target)

    # Draw score
    score_text = font.render(f"Score: {score}", True, GREEN)
    SCREEN.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
