"""
Laser projectile entity - projectile fired by powered-up player.
Now designed as a DBZ-style green energy ball (Ki blast).
"""
import pygame
import math
from config import LASER_SPEED, WINDOW_WIDTH


class Laser(pygame.sprite.Sprite):
    """
    Energy ball projectile (DBZ-style green Ki blast) that travels horizontally.
    Fired by the player when powered up.
    """

    def __init__(self, x, y, direction):
        """
        Initialize an energy ball projectile.

        Args:
            x: Starting x position (center of energy ball)
            y: Starting y position (center of energy ball)
            direction: Direction to travel (1 for right, -1 for left)
        """
        super().__init__()

        # Energy ball size (larger than old laser)
        self.size = 16  # Radius of energy ball
        self.width = self.size * 2
        self.height = self.size * 2

        # Animation properties
        self.animation_frame = 0
        self.animation_speed = 4  # Change animation every 4 frames
        self.animation_timer = 0

        # Generate energy ball frames
        self.energy_frames = self._generate_energy_ball_frames()

        # Set initial image
        self.image = self.energy_frames[0]

        # Position the energy ball
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Movement properties
        self.direction = direction  # 1 = right, -1 = left
        self.speed = LASER_SPEED

    def _generate_energy_ball_frames(self):
        """
        Generate DBZ-style green energy ball animation frames.
        Creates a pulsing energy sphere with glow and crackling energy.

        Returns:
            list: List of pygame.Surface objects for animation
        """
        frames = []

        # Generate 4 frames for pulsing animation
        for frame_num in range(4):
            # Create surface with transparency
            surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            surface.fill((0, 0, 0, 0))  # Transparent background

            # Animation phase for pulsing effect
            phase = frame_num / 4.0

            # Green energy colors (DBZ-style)
            energy_colors = [
                (100, 255, 100, 80),   # Light green outer glow
                (50, 255, 50, 120),    # Bright green
                (0, 255, 0, 160),      # Pure green
                (0, 220, 0, 200),      # Deep green core
            ]

            center_x = self.width // 2
            center_y = self.height // 2

            # Pulsing size variation
            pulse = math.sin(phase * math.pi * 2) * 2 + 2

            # Draw multiple layers of energy glow (from outer to inner)
            for layer in range(len(energy_colors)):
                radius = self.size - layer * 3 + int(pulse)
                if radius > 0:
                    color = energy_colors[layer]

                    # Create glow surface
                    glow_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surf, color, (center_x, center_y), radius)

                    # Blit to main surface
                    surface.blit(glow_surf, (0, 0))

            # Draw bright core
            core_radius = max(1, int(self.size * 0.4 + pulse * 0.5))
            pygame.draw.circle(surface, (200, 255, 200, 255),
                             (center_x, center_y), core_radius)

            # Add energy sparks around the ball
            num_sparks = 6
            for i in range(num_sparks):
                angle = (i / num_sparks) * math.pi * 2 + phase * math.pi * 3
                spark_dist = self.size * 0.7
                spark_x = center_x + int(math.cos(angle) * spark_dist)
                spark_y = center_y + int(math.sin(angle) * spark_dist)

                # Draw small spark
                pygame.draw.circle(surface, (150, 255, 150, 200),
                                 (spark_x, spark_y), 2)

            frames.append(surface)

        return frames

    def update(self, level_width=None):
        """
        Update energy ball position, animation, and check if it should be removed.

        Args:
            level_width (int, optional): Width of the level. If None, uses WINDOW_WIDTH.
        """
        # Move energy ball horizontally
        self.rect.x += self.speed * self.direction

        # Update animation
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % len(self.energy_frames)
            self.image = self.energy_frames[self.animation_frame]

        # Remove energy ball if it goes way off screen (give it a large buffer)
        # Use level_width if provided, otherwise use a very large default
        max_width = level_width if level_width else 10000
        if self.rect.right < -100 or self.rect.left > max_width + 100:
            self.kill()  # Remove from sprite groups
