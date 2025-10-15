"""
Laser projectile entity - projectile fired by powered-up player.
"""
import pygame
from config import LASER_WIDTH, LASER_HEIGHT, LASER_SPEED, CYAN, WINDOW_WIDTH


class Laser(pygame.sprite.Sprite):
    """
    Laser projectile that travels horizontally across the screen.
    Fired by the player when powered up.
    """

    def __init__(self, x, y, direction):
        """
        Initialize a laser projectile.

        Args:
            x: Starting x position (center of laser)
            y: Starting y position (center of laser)
            direction: Direction to travel (1 for right, -1 for left)
        """
        super().__init__()

        self.width = LASER_WIDTH
        self.height = LASER_HEIGHT

        # Create laser sprite (cyan rectangle)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(CYAN)

        # Position the laser
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Movement properties
        self.direction = direction  # 1 = right, -1 = left
        self.speed = LASER_SPEED

    def update(self, level_width=None):
        """
        Update laser position and check if it should be removed.

        Args:
            level_width (int, optional): Width of the level. If None, uses WINDOW_WIDTH.
        """
        # Move laser horizontally
        self.rect.x += self.speed * self.direction

        # Remove laser if it goes way off screen (give it a large buffer)
        # Use level_width if provided, otherwise use a very large default
        max_width = level_width if level_width else 10000
        if self.rect.right < -100 or self.rect.left > max_width + 100:
            self.kill()  # Remove from sprite groups
