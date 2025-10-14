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

    def update(self):
        """
        Update laser position and check if it should be removed.
        """
        # Move laser horizontally
        self.rect.x += self.speed * self.direction

        # Remove laser if it goes off screen
        if self.rect.right < 0 or self.rect.left > WINDOW_WIDTH:
            self.kill()  # Remove from sprite groups
