import pygame
from projectile import Projectile

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 80)
        self.vel_y = 0
        self.on_ground = False
        self.health = 100
        self.lives = 3

    def handle_input(self, keys):
        # Left/right movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        # Jump
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = -15
            self.on_ground = False

    def update(self):
        # Gravity
        self.vel_y += 1
        self.rect.y += self.vel_y
        if self.rect.y >= 520:  # Ground level
            self.rect.y = 520
            self.vel_y = 0
            self.on_ground = True

    def shoot(self):
        return Projectile(self.rect.right, self.rect.centery, 10)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
