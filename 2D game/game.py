import pygame
from player import Player
from enemy import Enemy
from projectile import Projectile
from collectible import Collectible
from level import Level

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Scroller Game")
clock = pygame.time.Clock()

# Game variables
level_num = 1
score = 0
running = True

# Create player, level, etc.
player = Player(100, HEIGHT - 150)
level = Level(level_num)
enemies = level.spawn_enemies()
collectibles = level.spawn_collectibles()
projectiles = []

def reset_level():
    global player, level, enemies, collectibles, projectiles
    player = Player(100, HEIGHT - 150)
    level = Level(level_num)
    enemies = level.spawn_enemies()
    collectibles = level.spawn_collectibles()
    projectiles = []

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle shooting
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(player.shoot())

    # Handle input
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    # Update
    player.update()
    for enemy in enemies:
        enemy.update()
    for proj in projectiles:
        proj.update()
    for c in collectibles:
        c.update()

    # Collision detection, scoring, health, etc. (to be implemented)

    # Draw everything
    screen.fill((135, 206, 235))  # Sky blue background
    level.draw(screen)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for proj in projectiles:
        proj.draw(screen)
    for c in collectibles:
        c.draw(screen)

    # Draw UI (score, health, lives)
    # ...

    pygame.display.flip()

pygame.quit()
