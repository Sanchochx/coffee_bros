"""
Mermelada (purple jam) projectile thrown by the Corruption Boss
Damages player on contact
"""

import pygame
import math


class Mermelada(pygame.sprite.Sprite):
    """
    Purple mermelada projectile thrown by boss
    Shoots in any direction (angle-based for circular patterns)
    """

    def __init__(self, x, y, angle):
        """
        Initialize mermelada projectile

        Args:
            x: Starting x position
            y: Starting y position
            angle: Angle in radians (for circular pattern shooting)
        """
        super().__init__()

        # Create purple mermelada sprite
        self.width = 20
        self.height = 20
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw purple mermelada blob
        purple = (150, 50, 150)
        purple_dark = (100, 30, 100)
        purple_light = (180, 80, 180)

        # Main blob
        pygame.draw.circle(self.image, purple, (10, 10), 10)
        # Highlight
        pygame.draw.circle(self.image, purple_light, (7, 7), 3)
        # Dark spot
        pygame.draw.circle(self.image, purple_dark, (13, 13), 2)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Physics - shoot in direction of angle (arcade-style)
        speed = 5  # Constant speed in all directions
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.gravity = 0  # No gravity for arcade-style straight shots

        # Lifetime
        self.alive = True

    def update(self, level_width):
        """
        Update mermelada position (straight line, arcade-style)

        Args:
            level_width: Width of the level for boundary checking
        """
        # Update position (no gravity, straight line)
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Remove if off screen
        if self.rect.top > 700 or self.rect.bottom < -100:  # Below or above screen
            self.kill()
        if self.rect.right < -100 or self.rect.left > level_width + 100:
            self.kill()
