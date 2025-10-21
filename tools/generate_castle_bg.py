"""
Generate castle interior background for boss fight level
Dark, gothic castle interior atmosphere
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Background dimensions
BG_WIDTH = 800
BG_HEIGHT = 600

def create_castle_interior_background():
    """Create a dark castle interior background"""
    surface = pygame.Surface((BG_WIDTH, BG_HEIGHT))

    # Dark stone wall colors
    dark_stone = (50, 45, 55)
    medium_stone = (70, 65, 75)
    light_stone = (90, 85, 95)

    # Fill with base dark stone
    surface.fill(dark_stone)

    # Draw stone brick pattern
    brick_width = 60
    brick_height = 40

    for row in range(0, BG_HEIGHT, brick_height):
        offset = brick_width // 2 if (row // brick_height) % 2 else 0
        for col in range(-brick_width, BG_WIDTH + brick_width, brick_width):
            x = col + offset
            # Draw brick outline
            rect = pygame.Rect(x, row, brick_width - 4, brick_height - 4)
            pygame.draw.rect(surface, medium_stone, rect)
            # Draw brick highlight
            pygame.draw.line(surface, light_stone, (x, row), (x + brick_width - 5, row), 2)
            pygame.draw.line(surface, light_stone, (x, row), (x, row + brick_height - 5), 2)

    # Add gothic windows/arches at the top (letting in ominous light)
    window_color = (100, 90, 120)  # Purplish glow
    # Left window
    pygame.draw.circle(surface, window_color, (150, 100), 40)
    pygame.draw.rect(surface, window_color, (110, 100, 80, 80))
    # Right window
    pygame.draw.circle(surface, window_color, (650, 100), 40)
    pygame.draw.rect(surface, window_color, (610, 100, 80, 80))

    # Add torch lighting effects (reddish glow on sides)
    torch_glow = pygame.Surface((100, 150), pygame.SRCALPHA)
    pygame.draw.circle(torch_glow, (255, 100, 0, 50), (50, 75), 60)
    surface.blit(torch_glow, (0, 200))
    surface.blit(torch_glow, (700, 200))

    # Add darker shadows at corners
    shadow = pygame.Surface((200, 600), pygame.SRCALPHA)
    shadow.fill((0, 0, 0, 100))
    surface.blit(shadow, (0, 0))
    surface.blit(shadow, (600, 0))

    # Add floor texture (darker at bottom)
    floor_color = (40, 35, 45)
    pygame.draw.rect(surface, floor_color, (0, BG_HEIGHT - 150, BG_WIDTH, 150))

    # Add floor tile lines
    for x in range(0, BG_WIDTH, 50):
        pygame.draw.line(surface, (50, 45, 55), (x, BG_HEIGHT - 150), (x, BG_HEIGHT), 1)

    return surface


def create_castle_tileset():
    """Create castle floor/platform tiles"""
    tile_size = 50

    # Dark castle stone tile
    tile = pygame.Surface((tile_size, tile_size))
    dark_gray = (60, 55, 65)
    med_gray = (80, 75, 85)
    light_gray = (100, 95, 105)

    tile.fill(dark_gray)

    # Add stone texture
    pygame.draw.rect(tile, med_gray, (2, 2, tile_size - 4, tile_size - 4))

    # Add highlights and shadows for 3D effect
    pygame.draw.line(tile, light_gray, (0, 0), (tile_size, 0), 2)
    pygame.draw.line(tile, light_gray, (0, 0), (0, tile_size), 2)
    pygame.draw.line(tile, (40, 35, 45), (tile_size - 1, 0), (tile_size - 1, tile_size), 2)
    pygame.draw.line(tile, (40, 35, 45), (0, tile_size - 1), (tile_size, tile_size - 1), 2)

    # Add cracks for detail
    pygame.draw.line(tile, (50, 45, 55), (10, 15), (40, 12), 1)
    pygame.draw.line(tile, (50, 45, 55), (30, 30), (45, 38), 1)

    return tile


def main():
    """Generate and save castle graphics"""
    # Create output directories
    bg_dir = "assets/images/backgrounds"
    tile_dir = "assets/images/tiles"
    os.makedirs(bg_dir, exist_ok=True)
    os.makedirs(tile_dir, exist_ok=True)

    print("Generating Castle Interior graphics...")

    # Create castle background
    castle_bg = create_castle_interior_background()
    pygame.image.save(castle_bg, os.path.join(bg_dir, "castle_interior.png"))
    print(f"Created castle_interior.png ({BG_WIDTH}x{BG_HEIGHT})")

    # Create castle tile variants (left, middle, right for platform system)
    castle_tile = create_castle_tileset()
    pygame.image.save(castle_tile, os.path.join(tile_dir, "castle_tile.png"))
    pygame.image.save(castle_tile, os.path.join(tile_dir, "castle_tile_left.png"))
    pygame.image.save(castle_tile, os.path.join(tile_dir, "castle_tile_middle.png"))
    pygame.image.save(castle_tile, os.path.join(tile_dir, "castle_tile_right.png"))
    print(f"Created castle_tile variants (50x50)")

    print(f"\nCastle graphics saved!")
    print("The boss arena is ready!")


if __name__ == "__main__":
    main()
