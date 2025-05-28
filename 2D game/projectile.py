import pygame

class Projectile:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
