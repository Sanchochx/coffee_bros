"""
Generate grass and stone tiles for level 1
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Tile dimensions
TILE_WIDTH = 50
TILE_HEIGHT = 50


def create_grass_tile():
    """Create a grass tile"""
    tile = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))

    # Green grass colors
    grass_green = (34, 139, 34)
    dark_green = (0, 100, 0)
    light_green = (50, 205, 50)

    # Fill with base grass color
    tile.fill(grass_green)

    # Add grass texture (small lines)
    for i in range(10):
        x = i * 5 + 2
        pygame.draw.line(tile, light_green, (x, 5), (x, 15), 1)
        pygame.draw.line(tile, dark_green, (x + 2, 10), (x + 2, 20), 1)

    # Add dirt at bottom
    dirt_color = (139, 90, 43)
    pygame.draw.rect(tile, dirt_color, (0, 35, TILE_WIDTH, 15))

    # Tile border
    pygame.draw.rect(tile, dark_green, (0, 0, TILE_WIDTH, TILE_HEIGHT), 2)

    return tile


def create_stone_tile():
    """Create a stone tile"""
    tile = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))

    # Stone colors
    stone_gray = (128, 128, 128)
    dark_gray = (80, 80, 80)
    light_gray = (170, 170, 170)

    # Fill with base stone color
    tile.fill(stone_gray)

    # Add stone texture (cracks and variations)
    pygame.draw.line(tile, dark_gray, (10, 15), (40, 12), 2)
    pygame.draw.line(tile, dark_gray, (5, 30), (45, 35), 2)
    pygame.draw.line(tile, light_gray, (20, 40), (35, 25), 1)
    pygame.draw.line(tile, light_gray, (15, 20), (30, 45), 1)

    # Tile border
    pygame.draw.rect(tile, dark_gray, (0, 0, TILE_WIDTH, TILE_HEIGHT), 2)

    return tile


def main():
    """Generate and save grass and stone tiles"""
    tile_dir = "assets/images/tiles"
    os.makedirs(tile_dir, exist_ok=True)

    print("Generating grass and stone tiles...")

    # Create grass tiles
    grass_tile = create_grass_tile()
    pygame.image.save(grass_tile, os.path.join(tile_dir, "grass_left.png"))
    pygame.image.save(grass_tile, os.path.join(tile_dir, "grass_middle.png"))
    pygame.image.save(grass_tile, os.path.join(tile_dir, "grass_right.png"))
    print("Created grass tiles (50x50)")

    # Create stone tiles
    stone_tile = create_stone_tile()
    pygame.image.save(stone_tile, os.path.join(tile_dir, "stone_left.png"))
    pygame.image.save(stone_tile, os.path.join(tile_dir, "stone_middle.png"))
    pygame.image.save(stone_tile, os.path.join(tile_dir, "stone_right.png"))
    print("Created stone tiles (50x50)")

    print("\nTiles saved!")
    print("Level 1 is ready to play!")


if __name__ == "__main__":
    main()
