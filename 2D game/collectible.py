import pygame

class Collectible:
    def __init__(self, x, y, kind):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.kind = kind  # 'health', 'life', etc.

    def update(self):
        pass

    def draw(self, screen):
        color = (0, 255, 0) if self.kind == 'health' else (255, 255, 0)
        pygame.draw.rect(screen, color, self.rect)
