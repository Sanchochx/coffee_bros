"""
Sancho Bros - Main Menu System
Displays menu screen with navigation options.
"""

import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, YELLOW, GREEN, RED, GOLD


class MainMenu:
    """Main menu screen with Colombian-themed background and navigation"""

    def __init__(self):
        """Initialize the main menu"""
        # Menu options
        self.options = ["Start Game", "Settings", "Quit"]
        self.selected_index = 0  # Currently selected option (0 = Start Game)

        # Fonts
        self.title_font = pygame.font.Font(None, 96)  # Large font for title
        self.option_font = pygame.font.Font(None, 48)  # Medium font for options
        self.subtitle_font = pygame.font.Font(None, 32)  # Small font for subtitle

        # Colors (Colombian theme)
        self.title_color = YELLOW  # Colombian yellow for title
        self.selected_color = GOLD  # Gold for selected option
        self.unselected_color = (200, 200, 200)  # Light gray for unselected options
        self.subtitle_color = (150, 150, 150)  # Gray for subtitle

        # Background colors (Colombian flag-inspired gradient simulation)
        # We'll use multiple horizontal bands to simulate the Colombian flag
        self.bg_yellow = YELLOW  # Top portion
        self.bg_blue = (0, 56, 168)  # Middle portion (Colombian blue)
        self.bg_red = (206, 17, 38)  # Bottom portion (Colombian red)

        # Background decoration animation
        self.animation_offset = 0  # For animated background elements

    def handle_input(self, event):
        """
        Handle keyboard input for menu navigation.
        Returns: 'start', 'settings', 'quit', or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                # Move selection up
                self.selected_index = (self.selected_index - 1) % len(self.options)
                # TODO (US-041): Play menu navigation sound effect (audio system in Epic 7)

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # Move selection down
                self.selected_index = (self.selected_index + 1) % len(self.options)
                # TODO (US-041): Play menu navigation sound effect (audio system in Epic 7)

            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Select current option
                # TODO (US-041): Play menu selection sound effect (audio system in Epic 7)
                selected_option = self.options[self.selected_index]

                if selected_option == "Start Game":
                    return "start"
                elif selected_option == "Settings":
                    return "settings"
                elif selected_option == "Quit":
                    return "quit"

            elif event.key == pygame.K_ESCAPE:
                # ESC key quits from main menu
                return "quit"

        return None

    def update(self):
        """Update menu animations"""
        # Animate background decoration offset for visual interest
        self.animation_offset = (self.animation_offset + 1) % 360

    def draw(self, screen):
        """Draw the main menu to the screen"""
        # Draw Colombian-themed background (flag-inspired bands)
        # Yellow band (top 50% of screen - Colombian flag has large yellow band)
        yellow_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT // 2)
        pygame.draw.rect(screen, self.bg_yellow, yellow_rect)

        # Blue band (middle 25% of screen)
        blue_rect = pygame.Rect(0, WINDOW_HEIGHT // 2, WINDOW_WIDTH, WINDOW_HEIGHT // 4)
        pygame.draw.rect(screen, self.bg_blue, blue_rect)

        # Red band (bottom 25% of screen)
        red_rect = pygame.Rect(0, WINDOW_HEIGHT * 3 // 4, WINDOW_WIDTH, WINDOW_HEIGHT // 4)
        pygame.draw.rect(screen, self.bg_red, red_rect)

        # Add semi-transparent overlay for better text readability
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(150)  # Semi-transparent
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Draw game title "Sancho Bros"
        title_text = self.title_font.render("Sancho Bros", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        # Add shadow effect for title
        shadow_text = self.title_font.render("Sancho Bros", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, 120 + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle_text = self.subtitle_font.render("A Colombian Coffee Adventure", True, self.subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 190))
        screen.blit(subtitle_text, subtitle_rect)

        # Draw menu options (centered vertically in lower half of screen)
        start_y = 300  # Starting y position for first option
        option_spacing = 80  # Vertical spacing between options

        for i, option in enumerate(self.options):
            # Determine color based on selection
            if i == self.selected_index:
                color = self.selected_color
                # Add selection indicator (arrow)
                arrow_text = self.option_font.render(">", True, color)
                arrow_rect = arrow_text.get_rect()
                arrow_rect.midright = (WINDOW_WIDTH // 2 - 150, start_y + i * option_spacing)
                screen.blit(arrow_text, arrow_rect)
            else:
                color = self.unselected_color

            # Render option text
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * option_spacing))
            screen.blit(option_text, option_rect)

        # Draw controls hint at bottom
        controls_text = self.subtitle_font.render("Use Arrow Keys or W/S to navigate, Enter to select", True, self.subtitle_color)
        controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(controls_text, controls_rect)

        # TODO (US-047): Play menu background music (audio system in Epic 7)
