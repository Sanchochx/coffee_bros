"""
Platform entity module for Sancho Bros
Contains the Platform sprite class for ground and floating platforms.
"""

import pygame
from config import GREEN


class Platform(pygame.sprite.Sprite):
    """Platform class for ground and floating platforms"""

    def __init__(self, x, y, width, height):
        """
        Initialize a platform

        Args:
            x (int): Platform x position (left edge)
            y (int): Platform y position (top edge)
            width (int): Platform width in pixels
            height (int): Platform height in pixels
        """
        super().__init__()

        # Create platform surface
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)

        # Get rect for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
