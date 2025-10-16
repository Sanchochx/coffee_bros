"""
Golden Arepa Power-up Entity
A collectible power-up that floats in the game world with a glowing effect.
"""
import pygame
import math
from config import GOLD, POWERUP_FLOAT_AMPLITUDE, POWERUP_FLOAT_SPEED


class GoldenArepa(pygame.sprite.Sprite):
    """
    Golden Arepa power-up sprite.
    Floats with a sine wave animation and has a pulsing glow effect.
    Can be collected by the player.
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

        # Glow dimensions (larger to create glow effect around the arepa)
        self.glow_width = 50
        self.glow_height = 50

        # Create base surfaces
        self._create_base_image()
        self._create_glow_frames()

        # Set up the rect for positioning and collision
        # Use glow dimensions - slightly larger collision area is fine
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Store the base y position (center of the floating motion)
        self.base_y = y

        # Animation timer for sine wave motion
        self.float_timer = 0

        # Glow animation variables
        self.glow_frame = 0  # Current glow frame (0-5)
        self.glow_frame_counter = 0  # Counter for cycling frames
        self.glow_frame_delay = 6  # Frames between glow updates (middle of 5-8 range)

    def _create_base_image(self):
        """Create the base arepa image (solid gold square)."""
        self.base_image = pygame.Surface((self.width, self.height))
        self.base_image.fill(GOLD)

    def _create_glow_frames(self):
        """
        Create 6 frames of glow animation with varying alpha values.
        Each frame has a different glow intensity that pulses smoothly.
        """
        self.glow_frames = []

        # Define alpha values for each of the 6 frames
        # Smoothly pulse from dim to bright and back
        alpha_values = [60, 100, 140, 180, 140, 100]

        for alpha in alpha_values:
            # Create a surface for the entire glow + arepa
            frame = pygame.Surface((self.glow_width, self.glow_height), pygame.SRCALPHA)

            # Create glow layers (3 concentric layers for smoother glow)
            glow_color = (255, 223, 0)  # Slightly different gold for glow

            # Outer glow (largest, most transparent)
            outer_glow = pygame.Surface((self.glow_width, self.glow_height), pygame.SRCALPHA)
            pygame.draw.circle(outer_glow, (*glow_color, alpha // 3),
                             (self.glow_width // 2, self.glow_height // 2),
                             self.glow_width // 2)
            frame.blit(outer_glow, (0, 0))

            # Middle glow (medium size and transparency)
            middle_glow = pygame.Surface((self.glow_width, self.glow_height), pygame.SRCALPHA)
            pygame.draw.circle(middle_glow, (*glow_color, alpha // 2),
                             (self.glow_width // 2, self.glow_height // 2),
                             self.glow_width // 3)
            frame.blit(middle_glow, (0, 0))

            # Inner glow (smallest, most opaque)
            inner_glow = pygame.Surface((self.glow_width, self.glow_height), pygame.SRCALPHA)
            pygame.draw.circle(inner_glow, (*glow_color, alpha),
                             (self.glow_width // 2, self.glow_height // 2),
                             self.width // 2 + 5)
            frame.blit(inner_glow, (0, 0))

            # Draw the solid arepa in the center
            arepa_x = (self.glow_width - self.width) // 2
            arepa_y = (self.glow_height - self.height) // 2
            frame.blit(self.base_image, (arepa_x, arepa_y))

            self.glow_frames.append(frame)

        # Set initial image to first glow frame
        self.image = self.glow_frames[0]

    def update(self):
        """
        Update the power-up's floating animation and glow effect.
        Uses a sine wave to create smooth up and down motion.
        Cycles through glow frames for pulsing effect.
        """
        # Increment the float timer
        self.float_timer += POWERUP_FLOAT_SPEED

        # Calculate the floating offset using sine wave
        # sin() returns value between -1 and 1, multiply by amplitude to get pixel offset
        float_offset = math.sin(self.float_timer) * POWERUP_FLOAT_AMPLITUDE

        # Update the y position based on base position and floating offset
        self.rect.centery = self.base_y + float_offset

        # Update glow animation
        self.glow_frame_counter += 1
        if self.glow_frame_counter >= self.glow_frame_delay:
            self.glow_frame_counter = 0
            # Move to next glow frame (loop back to 0 after frame 5)
            self.glow_frame = (self.glow_frame + 1) % 6
            # Update the image to the current glow frame
            self.image = self.glow_frames[self.glow_frame]
