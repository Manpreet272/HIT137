import pygame
from enemy import Enemy
from collectible import Collectible
from projectile import Projectile

class Level:
    def __init__(self, num):
        self.num = num

    def spawn_enemies(self):
        # Add more enemies for higher levels
        return [Enemy(600, 520), Enemy(900, 520)] if self.num == 1 else [Enemy(600, 520), Enemy(900, 520), Enemy(1200, 520)]

    def spawn_collectibles(self):
        return [Collectible(400, 550, 'health'), Collectible(800, 550, 'life')]

    def draw(self, screen):
        # Draw ground
        pygame.draw.rect(screen, (139, 69, 19), (0, 600-50, 800, 50))
