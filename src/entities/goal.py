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

        # Create castle-style goal sprite (Mario Bros inspired)
        self.image = self._create_castle_sprite()

        # Position the goal - x is center, y is bottom
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def _create_castle_sprite(self):
        """
        Create a Mario Bros-style castle sprite.
        Features castle walls, battlements, door, and flag.

        Returns:
            pygame.Surface: Castle sprite image
        """
        # Create surface with transparency
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent background

        # Castle color palette
        stone_gray = (150, 150, 150)  # Main castle walls
        dark_gray = (100, 100, 100)  # Shadows and details
        door_brown = (101, 67, 33)  # Wooden door
        flag_green = (0, 200, 0)  # Victory flag (keeping green theme)
        flag_pole = (64, 64, 64)  # Flag pole

        # Draw main castle tower (rectangular stone structure)
        tower_width = self.width - 4
        tower_height = int(self.height * 0.7)
        tower_x = 2
        tower_y = self.height - tower_height
        pygame.draw.rect(surface, stone_gray, (tower_x, tower_y, tower_width, tower_height))

        # Draw castle door (arched at top)
        door_width = int(self.width * 0.5)
        door_height = int(self.height * 0.35)
        door_x = (self.width - door_width) // 2
        door_y = self.height - door_height
        # Draw door rectangle
        pygame.draw.rect(surface, door_brown, (door_x, door_y, door_width, door_height))
        # Draw arch top (semi-circle)
        pygame.draw.circle(surface, door_brown, (door_x + door_width // 2, door_y), door_width // 2)
        # Draw door details (vertical lines for wooden planks)
        pygame.draw.line(surface, dark_gray,
                        (door_x + door_width // 3, door_y),
                        (door_x + door_width // 3, door_y + door_height), 1)
        pygame.draw.line(surface, dark_gray,
                        (door_x + 2 * door_width // 3, door_y),
                        (door_x + 2 * door_width // 3, door_y + door_height), 1)

        # Draw battlements/crenellations on top (castle roof pattern)
        battlement_height = 6
        battlement_width = 6
        num_battlements = 3
        for i in range(num_battlements):
            if i % 2 == 0:  # Draw raised battlements
                batt_x = tower_x + i * (tower_width // num_battlements)
                batt_width = tower_width // num_battlements
                pygame.draw.rect(surface, stone_gray,
                               (batt_x, tower_y - battlement_height, batt_width, battlement_height))
                # Add shadow to battlements
                pygame.draw.line(surface, dark_gray,
                               (batt_x, tower_y - battlement_height),
                               (batt_x, tower_y), 1)

        # Draw stone texture/bricks on castle walls
        for y in range(tower_y + 5, tower_y + tower_height - door_height - 5, 8):
            # Horizontal mortar lines
            pygame.draw.line(surface, dark_gray, (tower_x, y), (tower_x + tower_width, y), 1)

        # Draw flag on top of castle
        flag_pole_x = self.width // 2
        flag_pole_y_start = tower_y - battlement_height - 15
        flag_pole_y_end = tower_y - battlement_height
        # Flag pole
        pygame.draw.line(surface, flag_pole,
                        (flag_pole_x, flag_pole_y_start),
                        (flag_pole_x, flag_pole_y_end), 2)
        # Flag (triangle)
        flag_points = [
            (flag_pole_x, flag_pole_y_start),
            (flag_pole_x + 12, flag_pole_y_start + 4),
            (flag_pole_x, flag_pole_y_start + 8)
        ]
        pygame.draw.polygon(surface, flag_green, flag_points)

        # Draw windows (small dark rectangles)
        window_size = 4
        window_y1 = tower_y + 10
        window_y2 = tower_y + 22
        # Left window (top)
        pygame.draw.rect(surface, dark_gray,
                        (tower_x + 6, window_y1, window_size, window_size))
        # Right window (top)
        pygame.draw.rect(surface, dark_gray,
                        (tower_x + tower_width - 6 - window_size, window_y1, window_size, window_size))
        # Left window (middle)
        pygame.draw.rect(surface, dark_gray,
                        (tower_x + 6, window_y2, window_size, window_size))
        # Right window (middle)
        pygame.draw.rect(surface, dark_gray,
                        (tower_x + tower_width - 6 - window_size, window_y2, window_size, window_size))

        return surface
