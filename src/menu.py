"""
Coffee Bros - Main Menu System
Displays menu screen with navigation options.
"""

import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, YELLOW, GREEN, RED, GOLD


class MainMenu:
    """Main menu screen with Colombian-themed background and navigation"""

    def __init__(self):
        """Initialize the main menu"""
        # Menu options
        self.options = ["Start Game", "Settings", "Controls", "Quit"]
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
                elif selected_option == "Controls":
                    return "controls"
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

        # Draw game title "Coffee Bros"
        title_text = self.title_font.render("Coffee Bros", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        # Add shadow effect for title
        shadow_text = self.title_font.render("Coffee Bros", True, (50, 50, 50))
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


class GameOverMenu:
    """Game over screen displayed when player runs out of lives (US-036)"""

    def __init__(self):
        """Initialize the game over menu"""
        # Menu options
        self.options = ["Retry Level", "Return to Menu"]
        self.selected_index = 0  # Currently selected option (0 = Retry Level)

        # Fonts
        self.title_font = pygame.font.Font(None, 96)  # Large font for "GAME OVER"
        self.score_font = pygame.font.Font(None, 48)  # Medium font for score display
        self.option_font = pygame.font.Font(None, 48)  # Medium font for options

        # Colors
        self.title_color = RED  # Red for "GAME OVER" title
        self.score_color = (255, 255, 255)  # White for score
        self.selected_color = GOLD  # Gold for selected option
        self.unselected_color = (200, 200, 200)  # Light gray for unselected options

        # Input delay timer (prevents accidental immediate retry)
        self.input_delay = 60  # 60 frames = 1 second at 60 FPS
        self.delay_timer = 0

    def reset(self):
        """Reset the game over menu state (call when entering game over state)"""
        self.selected_index = 0
        self.delay_timer = 0

    def handle_input(self, event):
        """
        Handle keyboard input for game over menu navigation.
        Returns: 'retry', 'menu', or None
        """
        # Don't accept input during delay period
        if self.delay_timer < self.input_delay:
            return None

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

                if selected_option == "Retry Level":
                    return "retry"
                elif selected_option == "Return to Menu":
                    return "menu"

        return None

    def update(self):
        """Update game over menu (increment delay timer)"""
        if self.delay_timer < self.input_delay:
            self.delay_timer += 1

    def draw(self, screen, final_score):
        """Draw the game over menu to the screen"""
        # Create semi-transparent dark overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)  # Mostly opaque for clear game over screen
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Draw "GAME OVER" title
        title_text = self.title_font.render("GAME OVER", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        # Add shadow effect for title
        shadow_text = self.title_font.render("GAME OVER", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, 120 + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)

        # Draw final score
        score_text = self.score_font.render(f"Final Score: {final_score}", True, self.score_color)
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 220))
        screen.blit(score_text, score_rect)

        # Draw menu options (centered vertically in lower half of screen)
        start_y = 340  # Starting y position for first option
        option_spacing = 80  # Vertical spacing between options

        for i, option in enumerate(self.options):
            # Determine color based on selection and delay
            if self.delay_timer < self.input_delay:
                # During delay, show all options in dim color
                color = (100, 100, 100)  # Dark gray during delay
            elif i == self.selected_index:
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


class SettingsMenu:
    """Settings menu screen for adjusting game options (US-060, US-061)"""

    def __init__(self, audio_manager, settings_manager=None):
        """Initialize the settings menu

        Args:
            audio_manager (AudioManager): Audio manager to control volumes
            settings_manager (SettingsManager): Settings manager for persistence
        """
        # Store audio manager and settings manager references
        self.audio_manager = audio_manager
        self.settings_manager = settings_manager

        # Menu options - settings items
        self.options = [
            "Music Volume",
            "Sound Effects Volume",
            "Back"
        ]
        self.selected_index = 0  # Currently selected option

        # Volume settings (0.0 to 1.0) - load from settings manager or use defaults
        if self.settings_manager:
            self.music_volume = self.settings_manager.get_music_volume()
            self.sfx_volume = self.settings_manager.get_sfx_volume()
        else:
            self.music_volume = 0.7  # Default 70%
            self.sfx_volume = 0.7    # Default 70%

        # Initialize audio manager volumes
        if self.audio_manager:
            self.audio_manager.set_music_volume(self.music_volume)
            self.audio_manager.set_sfx_volume(self.sfx_volume)

        # Track where we came from (for returning to correct menu)
        self.return_to = "menu"  # Can be "menu" or "pause"

        # Fonts
        self.title_font = pygame.font.Font(None, 96)
        self.option_font = pygame.font.Font(None, 48)
        self.value_font = pygame.font.Font(None, 36)

        # Colors
        self.title_color = YELLOW
        self.selected_color = GOLD
        self.unselected_color = (200, 200, 200)
        self.value_color = (150, 255, 150)  # Light green for values

    def set_return_to(self, return_to):
        """Set where the settings menu should return to

        Args:
            return_to (str): "menu" or "pause"
        """
        self.return_to = return_to

    def handle_input(self, event):
        """
        Handle keyboard input for settings menu navigation.
        Returns: 'back' when user exits, or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                # Move selection up
                self.selected_index = (self.selected_index - 1) % len(self.options)

            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # Move selection down
                self.selected_index = (self.selected_index + 1) % len(self.options)

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # Decrease volume for selected setting
                if self.options[self.selected_index] == "Music Volume":
                    self.music_volume = max(0.0, self.music_volume - 0.1)
                    if self.audio_manager:
                        self.audio_manager.set_music_volume(self.music_volume)
                    if self.settings_manager:
                        self.settings_manager.set_music_volume(self.music_volume)
                elif self.options[self.selected_index] == "Sound Effects Volume":
                    self.sfx_volume = max(0.0, self.sfx_volume - 0.1)
                    if self.audio_manager:
                        self.audio_manager.set_sfx_volume(self.sfx_volume)
                    if self.settings_manager:
                        self.settings_manager.set_sfx_volume(self.sfx_volume)

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # Increase volume for selected setting
                if self.options[self.selected_index] == "Music Volume":
                    self.music_volume = min(1.0, self.music_volume + 0.1)
                    if self.audio_manager:
                        self.audio_manager.set_music_volume(self.music_volume)
                    if self.settings_manager:
                        self.settings_manager.set_music_volume(self.music_volume)
                elif self.options[self.selected_index] == "Sound Effects Volume":
                    self.sfx_volume = min(1.0, self.sfx_volume + 0.1)
                    if self.audio_manager:
                        self.audio_manager.set_sfx_volume(self.sfx_volume)
                    if self.settings_manager:
                        self.settings_manager.set_sfx_volume(self.sfx_volume)

            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Select current option
                if self.options[self.selected_index] == "Back":
                    return "back"

            elif event.key == pygame.K_ESCAPE:
                # ESC returns to previous menu
                return "back"

        return None

    def draw(self, screen):
        """Draw the settings menu to the screen"""
        # Fill with black background
        screen.fill(BLACK)

        # Draw "SETTINGS" title
        title_text = self.title_font.render("SETTINGS", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 100))
        # Add shadow effect for title
        shadow_text = self.title_font.render("SETTINGS", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, 100 + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)

        # Draw menu options
        start_y = 250
        option_spacing = 100

        for i, option in enumerate(self.options):
            # Determine color based on selection
            if i == self.selected_index:
                color = self.selected_color
                # Add selection indicator (arrow)
                arrow_text = self.option_font.render(">", True, color)
                arrow_rect = arrow_text.get_rect()
                arrow_rect.midright = (120, start_y + i * option_spacing)
                screen.blit(arrow_text, arrow_rect)
            else:
                color = self.unselected_color

            # Render option text
            option_text = self.option_font.render(option, True, color)
            option_rect = option_text.get_rect()
            option_rect.midleft = (150, start_y + i * option_spacing)
            screen.blit(option_text, option_rect)

            # Draw volume sliders and values
            if option == "Music Volume":
                self._draw_volume_slider(screen, self.music_volume, start_y + i * option_spacing)
            elif option == "Sound Effects Volume":
                self._draw_volume_slider(screen, self.sfx_volume, start_y + i * option_spacing)

        # Draw controls hint at bottom
        controls_font = pygame.font.Font(None, 28)
        controls_text = controls_font.render("Use Arrow Keys to navigate, Left/Right to adjust, Enter/ESC to go back", True, (150, 150, 150))
        controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(controls_text, controls_rect)

    def _draw_volume_slider(self, screen, volume, y_pos):
        """Draw a visual volume slider bar

        Args:
            screen: Pygame screen surface
            volume (float): Volume level 0.0 to 1.0
            y_pos (int): Y position for slider
        """
        # Slider dimensions
        slider_x = 500
        slider_y = y_pos - 15
        slider_width = 200
        slider_height = 30

        # Draw slider background (empty bar)
        pygame.draw.rect(screen, (80, 80, 80), (slider_x, slider_y, slider_width, slider_height))

        # Draw filled portion (current volume level)
        filled_width = int(slider_width * volume)
        if filled_width > 0:
            pygame.draw.rect(screen, self.value_color, (slider_x, slider_y, filled_width, slider_height))

        # Draw slider border
        pygame.draw.rect(screen, self.unselected_color, (slider_x, slider_y, slider_width, slider_height), 2)

        # Draw percentage value
        percentage = int(volume * 100)
        value_text = self.value_font.render(f"{percentage}%", True, self.value_color)
        value_rect = value_text.get_rect()
        value_rect.midleft = (slider_x + slider_width + 20, y_pos)
        screen.blit(value_text, value_rect)


class ControlsMenu:
    """Controls display screen showing keyboard controls (US-062)"""

    def __init__(self):
        """Initialize the controls display screen"""
        # Control scheme - list of (action, keys) tuples
        self.controls = [
            ("Move Left", "A or Left Arrow"),
            ("Move Right", "D or Right Arrow"),
            ("Jump", "W, Up Arrow, or Space"),
            ("Shoot Laser", "X or J (when powered up)"),
            ("Pause Game", "ESC (during gameplay)"),
            ("Menu Navigation", "W/S or Up/Down Arrows"),
            ("Menu Select", "Enter or Space"),
        ]

        # Track where we came from (for returning to correct menu)
        self.return_to = "menu"  # Can be "menu" or "pause"

        # Fonts
        self.title_font = pygame.font.Font(None, 96)  # Large font for title
        self.section_font = pygame.font.Font(None, 48)  # Medium font for section headers
        self.action_font = pygame.font.Font(None, 36)  # Font for action names
        self.key_font = pygame.font.Font(None, 32)  # Font for key names

        # Colors
        self.title_color = YELLOW  # Yellow for title
        self.action_color = (255, 255, 255)  # White for action names
        self.key_color = GOLD  # Gold for key bindings
        self.hint_color = (150, 150, 150)  # Gray for hints

    def set_return_to(self, return_to):
        """Set where the controls menu should return to

        Args:
            return_to (str): "menu" or "pause"
        """
        self.return_to = return_to

    def handle_input(self, event):
        """
        Handle keyboard input for controls screen.
        Returns: 'back' when user exits, or None
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Any of these keys returns to previous menu
                return "back"

        return None

    def draw(self, screen):
        """Draw the controls display screen"""
        # Fill with black background
        screen.fill(BLACK)

        # Draw "CONTROLS" title
        title_text = self.title_font.render("CONTROLS", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        # Add shadow effect for title
        shadow_text = self.title_font.render("CONTROLS", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, 80 + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)

        # Starting position for controls list
        start_y = 180
        line_spacing = 55  # Vertical spacing between control entries

        # Draw each control entry
        for i, (action, keys) in enumerate(self.controls):
            y_pos = start_y + i * line_spacing

            # Draw action name (left-aligned)
            action_text = self.action_font.render(action + ":", True, self.action_color)
            action_rect = action_text.get_rect()
            action_rect.midleft = (100, y_pos)
            screen.blit(action_text, action_rect)

            # Draw key binding (right side, with visual key box)
            key_text = self.key_font.render(keys, True, self.key_color)
            key_rect = key_text.get_rect()
            key_rect.midleft = (400, y_pos)

            # Draw rounded rectangle box around key text for visual emphasis
            box_padding = 12
            box_rect = pygame.Rect(
                key_rect.left - box_padding,
                key_rect.top - box_padding,
                key_rect.width + box_padding * 2,
                key_rect.height + box_padding * 2
            )
            # Draw box with border
            pygame.draw.rect(screen, (60, 60, 60), box_rect, border_radius=8)  # Dark gray background
            pygame.draw.rect(screen, self.key_color, box_rect, 2, border_radius=8)  # Gold border

            # Draw key text on top of box
            screen.blit(key_text, key_rect)

        # Draw controls hint at bottom
        hint_font = pygame.font.Font(None, 28)
        hint_text = hint_font.render("Press ESC, Enter, or Space to go back", True, self.hint_color)
        hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        screen.blit(hint_text, hint_rect)


class PauseMenu:
    """Pause menu overlay displayed during gameplay (US-035)"""

    def __init__(self):
        """Initialize the pause menu"""
        # Menu options
        self.options = ["Resume", "Restart Level", "Settings", "Controls", "Return to Menu"]
        self.selected_index = 0  # Currently selected option (0 = Resume)

        # Fonts
        self.title_font = pygame.font.Font(None, 96)  # Large font for "PAUSED"
        self.option_font = pygame.font.Font(None, 48)  # Medium font for options

        # Colors
        self.title_color = YELLOW  # Yellow for "PAUSED" title
        self.selected_color = GOLD  # Gold for selected option
        self.unselected_color = (200, 200, 200)  # Light gray for unselected options

    def handle_input(self, event):
        """
        Handle keyboard input for pause menu navigation.
        Returns: 'resume', 'restart', 'settings', 'menu', or None
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

                if selected_option == "Resume":
                    return "resume"
                elif selected_option == "Restart Level":
                    return "restart"
                elif selected_option == "Settings":
                    return "settings"
                elif selected_option == "Controls":
                    return "controls"
                elif selected_option == "Return to Menu":
                    return "menu"

            elif event.key == pygame.K_ESCAPE:
                # ESC key unpauses the game (same as Resume)
                return "resume"

        return None

    def draw(self, screen):
        """Draw the pause menu overlay on top of the game"""
        # Create semi-transparent dark overlay (dims the background game)
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)  # Semi-transparent (0-255)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Draw "PAUSED" title
        title_text = self.title_font.render("PAUSED", True, self.title_color)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        # Add shadow effect for title
        shadow_text = self.title_font.render("PAUSED", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + 3, 150 + 3))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)

        # Draw menu options (centered vertically)
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
