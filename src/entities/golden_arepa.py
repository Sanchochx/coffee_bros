"""
Golden Arepa Power-up Entity
A collectible power-up that floats in the game world.
"""
import pygame
import math
from config import GOLD, POWERUP_FLOAT_AMPLITUDE, POWERUP_FLOAT_SPEED


class GoldenArepa(pygame.sprite.Sprite):
    """
    Golden Arepa power-up sprite.
    Floats with a sine wave animation and can be collected by the player.
    """

    def __init__(self, x, y):
        """
        Initialize the Golden Arepa power-up.

        Args:
            x (int): X-coordinate of the power-up's center position
            y (int): Y-coordinate of the power-up's base position (center of float range)
        """
        super().__init__()

        # Power-up dimensions (30x30 pixels as per technical notes)
        self.width = 30
        self.height = 30

        # Create the power-up sprite (golden/yellow square)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GOLD)

        # Set up the rect for positioning and collision
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Store the base y position (center of the floating motion)
        self.base_y = y

        # Animation timer for sine wave motion
        self.float_timer = 0

    def update(self):
        """
        Update the power-up's floating animation.
        Uses a sine wave to create smooth up and down motion.
        """
        # Increment the float timer
        self.float_timer += POWERUP_FLOAT_SPEED

        # Calculate the floating offset using sine wave
        # sin() returns value between -1 and 1, multiply by amplitude to get pixel offset
        float_offset = math.sin(self.float_timer) * POWERUP_FLOAT_AMPLITUDE

        # Update the y position based on base position and floating offset
        self.rect.centery = self.base_y + float_offset
