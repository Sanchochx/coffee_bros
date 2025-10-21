"""
Generate presidential office background for boss fight level
Colombian Casa de Nariño (Presidential House) interior with flags
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Background dimensions
BG_WIDTH = 800
BG_HEIGHT = 600

def create_presidential_office_background():
    """Create a Colombian presidential office background"""
    surface = pygame.Surface((BG_WIDTH, BG_HEIGHT))

    # Elegant office wall colors
    wall_color = (140, 120, 100)  # Brownish presidential office
    dark_wood = (80, 60, 40)

    # Fill with base wall color
    surface.fill(wall_color)

    # Draw wood paneling on walls (presidential style)
    panel_width = 100
    for x in range(0, BG_WIDTH, panel_width):
        pygame.draw.rect(surface, dark_wood, (x, 0, 4, BG_HEIGHT))  # Vertical lines

    # Draw horizontal wood trim
    pygame.draw.rect(surface, dark_wood, (0, BG_HEIGHT // 3, BG_WIDTH, 8))

    # Colombian flags on the walls
    # Colombian flag colors: Yellow (top 50%), Blue (25%), Red (25%)
    flag_yellow = (255, 209, 0)
    flag_blue = (0, 56, 168)
    flag_red = (206, 17, 38)

    # Left flag
    flag_left_x = 100
    flag_left_y = 80
    flag_width = 120
    flag_height = 80

    # Yellow band (50%)
    pygame.draw.rect(surface, flag_yellow, (flag_left_x, flag_left_y, flag_width, flag_height // 2))
    # Blue band (25%)
    pygame.draw.rect(surface, flag_blue, (flag_left_x, flag_left_y + flag_height // 2, flag_width, flag_height // 4))
    # Red band (25%)
    pygame.draw.rect(surface, flag_red, (flag_left_x, flag_left_y + 3 * flag_height // 4, flag_width, flag_height // 4))
    # Flag border
    pygame.draw.rect(surface, dark_wood, (flag_left_x, flag_left_y, flag_width, flag_height), 3)
    # Flag pole
    pygame.draw.rect(surface, dark_wood, (flag_left_x - 5, flag_left_y - 20, 5, 120))

    # Right flag
    flag_right_x = 580
    flag_right_y = 80

    # Yellow band (50%)
    pygame.draw.rect(surface, flag_yellow, (flag_right_x, flag_right_y, flag_width, flag_height // 2))
    # Blue band (25%)
    pygame.draw.rect(surface, flag_blue, (flag_right_x, flag_right_y + flag_height // 2, flag_width, flag_height // 4))
    # Red band (25%)
    pygame.draw.rect(surface, flag_red, (flag_right_x, flag_right_y + 3 * flag_height // 4, flag_width, flag_height // 4))
    # Flag border
    pygame.draw.rect(surface, dark_wood, (flag_right_x, flag_right_y, flag_width, flag_height), 3)
    # Flag pole
    pygame.draw.rect(surface, dark_wood, (flag_right_x - 5, flag_right_y - 20, 5, 120))

    # Presidential desk silhouette in background (center)
    desk_color = (60, 40, 20)
    pygame.draw.rect(surface, desk_color, (300, 400, 200, 80))
    # Desk drawers
    pygame.draw.rect(surface, (40, 25, 10), (310, 410, 35, 25), 2)
    pygame.draw.rect(surface, (40, 25, 10), (355, 410, 35, 25), 2)
    pygame.draw.rect(surface, (40, 25, 10), (410, 410, 35, 25), 2)
    pygame.draw.rect(surface, (40, 25, 10), (455, 410, 35, 25), 2)

    # Bookshelf on left side
    shelf_color = (70, 50, 30)
    pygame.draw.rect(surface, shelf_color, (20, 250, 80, 200))
    # Shelves
    for i in range(4):
        y = 270 + i * 50
        pygame.draw.rect(surface, dark_wood, (20, y, 80, 5))
    # Books (colorful rectangles)
    book_colors = [(180, 0, 0), (0, 100, 180), (0, 150, 50), (150, 100, 0)]
    for i, color in enumerate(book_colors):
        pygame.draw.rect(surface, color, (25 + i * 15, 255, 12, 30))
        pygame.draw.rect(surface, color, (25 + i * 15, 305, 12, 30))

    # Chandelier/light fixture at top center
    light_color = (255, 240, 200)
    pygame.draw.circle(surface, light_color, (BG_WIDTH // 2, 50), 30)
    pygame.draw.circle(surface, (200, 180, 100), (BG_WIDTH // 2, 50), 30, 3)

    # Carpet/floor at bottom
    carpet_red = (120, 20, 20)
    pygame.draw.rect(surface, carpet_red, (0, BG_HEIGHT - 150, BG_WIDTH, 150))

    # Carpet pattern (decorative lines)
    carpet_gold = (180, 150, 50)
    for x in range(50, BG_WIDTH, 100):
        pygame.draw.line(surface, carpet_gold, (x, BG_HEIGHT - 140), (x, BG_HEIGHT - 10), 2)

    # Add window with light (left side)
    window_color = (200, 220, 255)
    pygame.draw.rect(surface, window_color, (30, 100, 60, 100))
    pygame.draw.rect(surface, dark_wood, (30, 100, 60, 100), 4)
    pygame.draw.line(surface, dark_wood, (60, 100), (60, 200), 4)
    pygame.draw.line(surface, dark_wood, (30, 150), (90, 150), 4)

    return surface


def create_presidential_tileset():
    """Create presidential office floor tiles (marble/elegant)"""
    tile_size = 50

    # Elegant marble tile
    tile = pygame.Surface((tile_size, tile_size))
    marble_white = (220, 220, 230)
    marble_gray = (180, 180, 190)

    tile.fill(marble_white)

    # Add marble veins
    vein_color = (160, 160, 170)
    pygame.draw.line(tile, vein_color, (10, 15), (40, 12), 2)
    pygame.draw.line(tile, vein_color, (5, 30), (45, 35), 2)
    pygame.draw.line(tile, vein_color, (20, 40), (35, 25), 1)

    # Tile border
    pygame.draw.rect(tile, marble_gray, (0, 0, tile_size, tile_size), 1)

    return tile


def main():
    """Generate and save presidential office graphics"""
    # Create output directories
    bg_dir = "assets/images/backgrounds"
    tile_dir = "assets/images/tiles"
    os.makedirs(bg_dir, exist_ok=True)
    os.makedirs(tile_dir, exist_ok=True)

    print("Generating Presidential Office graphics...")

    # Create presidential office background
    office_bg = create_presidential_office_background()
    pygame.image.save(office_bg, os.path.join(bg_dir, "presidential_office.png"))
    print(f"Created presidential_office.png ({BG_WIDTH}x{BG_HEIGHT})")

    # Create marble tiles
    marble_tile = create_presidential_tileset()
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile.png"))
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile_left.png"))
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile_middle.png"))
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile_right.png"))
    print(f"Created presidential_tile variants (50x50)")

    print(f"\nPresidential office graphics saved!")
    print("The boss arena is ready for political corruption!")


if __name__ == "__main__":
    main()
