"""
Level Name Display System
Displays the level name at the start of each level with fade-in/fade-out animation.
"""

import pygame


class LevelNameDisplay:
    """
    Displays level name and number at the start of a level.
    Features fade-in and fade-out animations.
    """

    def __init__(self, level_number, level_name):
        """
        Initialize the level name display.

        Args:
            level_number (int): The level number (e.g., 1, 2, 3)
            level_name (str): The level name (e.g., "Coffee Hills")
        """
        self.level_number = level_number
        self.level_name = level_name
        self.is_active = True
        self.timer = 0

        # Animation timing (in frames at 60 FPS)
        self.fade_in_duration = 30  # 0.5 seconds
        self.display_duration = 120  # 2 seconds (after fade-in)
        self.fade_out_duration = 30  # 0.5 seconds
        self.total_duration = self.fade_in_duration + self.display_duration + self.fade_out_duration  # 180 frames = 3 seconds

        # Create the text surface
        self.font = pygame.font.Font(None, 60)  # Large, readable font
        self.text = f"Level {level_number} - {level_name}"

        # Pre-render the text at full opacity
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()

        # Current alpha value for fade effect
        self.alpha = 0

    def update(self):
        """
        Update the display animation.
        Handles fade-in, display, and fade-out timing.
        """
        if not self.is_active:
            return

        self.timer += 1

        # Calculate alpha based on current phase
        if self.timer <= self.fade_in_duration:
            # Fade in: 0 -> 255
            progress = self.timer / self.fade_in_duration
            self.alpha = int(255 * progress)
        elif self.timer <= self.fade_in_duration + self.display_duration:
            # Full display: alpha = 255
            self.alpha = 255
        elif self.timer <= self.total_duration:
            # Fade out: 255 -> 0
            fade_out_progress = (self.timer - self.fade_in_duration - self.display_duration) / self.fade_out_duration
            self.alpha = int(255 * (1 - fade_out_progress))
        else:
            # Animation complete
            self.is_active = False
            self.alpha = 0

    def draw(self, screen):
        """
        Draw the level name display on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        if not self.is_active or self.alpha <= 0:
            return

        # Create a copy of the text surface with current alpha
        text_with_alpha = self.text_surface.copy()
        text_with_alpha.set_alpha(self.alpha)

        # Center the text on the screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.text_rect.center = (screen_width // 2, screen_height // 3)

        # Draw the text
        screen.blit(text_with_alpha, self.text_rect)
