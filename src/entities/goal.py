"""
Goal entity for level completion.
Represents the end goal (flag/door) that triggers level completion.
"""

import pygame
from config import GOAL_COLOR


class Goal(pygame.sprite.Sprite):
    """
    Goal sprite that triggers level completion when player touches it.
    Visually represents the end goal of a level (flag, door, etc.)
    """

    def __init__(self, x, y, width=40, height=80):
        """
        Initialize the goal sprite.

        Args:
            x: X position (center of goal)
            y: Y position (bottom of goal)
            width: Width of goal sprite (default 40)
            height: Height of goal sprite (default 80)
        """
        super().__init__()

        self.width = width
        self.height = height

        # Create goal sprite (bright green rectangle for visibility)
        # TODO (Epic 8): Replace with flag or door sprite graphic
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(GOAL_COLOR)

        # Position the goal - x is center, y is bottom
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
