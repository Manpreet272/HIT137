import pygame

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 80)
        self.health = 50

    def update(self):
        # Simple AI: move left
        self.rect.x -= 2

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
