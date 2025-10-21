"""
Drawing utility functions for Coffee Bros
Helper functions for rendering backgrounds, HUD elements, etc.
"""

import pygame
import os


# Heart sprite cache (loaded once)
_heart_image = None


def load_heart_image():
    """Load and cache the heart sprite for lives display"""
    global _heart_image
    if _heart_image is None:
        heart_path = os.path.join('assets', 'images', 'heart.png')
        try:
            _heart_image = pygame.image.load(heart_path).convert_alpha()
        except pygame.error as e:
            print(f"Warning: Could not load heart image: {e}")
            # Create fallback heart if image not found
            _heart_image = create_fallback_heart()
    return _heart_image


def create_fallback_heart():
    """Create a simple fallback heart if image file is missing"""
    heart = pygame.Surface((20, 20), pygame.SRCALPHA)
    RED = (255, 50, 50)
    pygame.draw.circle(heart, RED, (7, 7), 5)
    pygame.draw.circle(heart, RED, (13, 7), 5)
    points = [(2, 9), (18, 9), (10, 18)]
    pygame.draw.polygon(heart, RED, points)
    return heart


def draw_tiled_background(screen, background_image, camera_x, level_width, window_width, window_height):
    """
    Draw a background image tiled across the entire level width

    Args:
        screen: Pygame screen surface to draw on
        background_image: Background image surface
        camera_x: Current camera x position
        level_width: Total width of the level
        window_width: Width of the game window
        window_height: Height of the game window
    """
    if not background_image:
        return

    bg_width = background_image.get_width()
    bg_height = background_image.get_height()

    # Calculate how many tiles we need to cover the visible area
    # We draw from slightly before the camera to slightly after
    start_x = (camera_x // bg_width) * bg_width
    end_x = camera_x + window_width + bg_width

    # Draw tiles
    for tile_x in range(int(start_x), int(end_x), bg_width):
        # Calculate draw position on screen (with camera offset)
        screen_x = tile_x - camera_x

        # Only draw if visible on screen
        if screen_x + bg_width >= 0 and screen_x < window_width:
            # If the background is taller/shorter than window, scale it
            if bg_height != window_height:
                scaled_bg = pygame.transform.scale(background_image, (bg_width, window_height))
                screen.blit(scaled_bg, (screen_x, 0))
            else:
                screen.blit(background_image, (screen_x, 0))


def draw_hearts(screen, lives, x, y, spacing=5):
    """
    Draw heart icons to represent player lives

    Args:
        screen: Pygame screen surface to draw on
        lives: Number of lives to display
        x: Starting x position (right edge)
        y: Starting y position (top edge)
        spacing: Space between hearts in pixels

    Returns:
        The leftmost x position of the drawn hearts
    """
    heart_image = load_heart_image()
    heart_width = heart_image.get_width()
    heart_height = heart_image.get_height()

    # Draw hearts from right to left
    current_x = x
    for i in range(lives):
        heart_x = current_x - heart_width
        screen.blit(heart_image, (heart_x, y))
        current_x = heart_x - spacing

    return current_x
