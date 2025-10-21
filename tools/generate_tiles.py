"""
Tile sprite generator for Coffee Bros
Generates platform tile graphics with proper textures
"""

import pygame
import os

# Initialize pygame for surface creation
pygame.init()

# Tile size
TILE_SIZE = 50

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'tiles')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_grass_tile():
    """Create a grass/earth ground tile (50x50)"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))

    # Earth brown base
    BROWN = (101, 67, 33)
    DARK_BROWN = (80, 50, 20)
    LIGHT_BROWN = (120, 80, 40)

    tile.fill(BROWN)

    # Add texture with random dirt spots
    for i in range(20):
        x = (i * 17) % TILE_SIZE
        y = ((i * 23) % (TILE_SIZE - 10)) + 10
        color = DARK_BROWN if i % 2 == 0 else LIGHT_BROWN
        pygame.draw.circle(tile, color, (x, y), 2)

    # Add grass on top (green layer)
    GREEN = (34, 139, 34)
    DARK_GREEN = (20, 100, 20)
    pygame.draw.rect(tile, GREEN, (0, 0, TILE_SIZE, 8))

    # Add grass blades
    for i in range(8):
        x = i * 6 + 3
        pygame.draw.line(tile, DARK_GREEN, (x, 5), (x, 0), 1)

    return tile


def create_stone_tile():
    """Create a stone tile for floating platforms (50x50)"""
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE))

    # Gray stone base
    GRAY = (128, 128, 128)
    DARK_GRAY = (100, 100, 100)
    LIGHT_GRAY = (150, 150, 150)

    tile.fill(GRAY)

    # Add stone texture with cracks and variations
    # Horizontal lines
    for y in [10, 25, 40]:
        pygame.draw.line(tile, DARK_GRAY, (0, y), (TILE_SIZE, y), 1)

    # Vertical lines
    for x in [15, 35]:
        pygame.draw.line(tile, DARK_GRAY, (x, 0), (x, TILE_SIZE), 1)

    # Add some highlights
    for i in range(15):
        x = (i * 19) % TILE_SIZE
        y = (i * 13) % TILE_SIZE
        color = LIGHT_GRAY if i % 3 == 0 else DARK_GRAY
        pygame.draw.circle(tile, color, (x, y), 1)

    # Add border for definition
    pygame.draw.rect(tile, DARK_GRAY, (0, 0, TILE_SIZE, TILE_SIZE), 1)

    return tile


def create_grass_left_edge():
    """Create left edge tile for grass platforms"""
    tile = create_grass_tile()

    # Add darker edge on left
    DARK_BROWN = (60, 40, 15)
    pygame.draw.rect(tile, DARK_BROWN, (0, 8, 3, TILE_SIZE - 8))

    return tile


def create_grass_right_edge():
    """Create right edge tile for grass platforms"""
    tile = create_grass_tile()

    # Add darker edge on right
    DARK_BROWN = (60, 40, 15)
    pygame.draw.rect(tile, DARK_BROWN, (TILE_SIZE - 3, 8, 3, TILE_SIZE - 8))

    return tile


def create_stone_left_edge():
    """Create left edge tile for stone platforms"""
    tile = create_stone_tile()

    # Add darker edge on left
    DARK_GRAY = (80, 80, 80)
    pygame.draw.rect(tile, DARK_GRAY, (0, 0, 3, TILE_SIZE))

    return tile


def create_stone_right_edge():
    """Create right edge tile for stone platforms"""
    tile = create_stone_tile()

    # Add darker edge on right
    DARK_GRAY = (80, 80, 80)
    pygame.draw.rect(tile, DARK_GRAY, (TILE_SIZE - 3, 0, 3, TILE_SIZE))

    return tile


def main():
    """Generate all tile sprites"""
    print("Generating platform tiles...")

    # Grass tiles
    grass_tile = create_grass_tile()
    pygame.image.save(grass_tile, os.path.join(OUTPUT_DIR, 'grass_middle.png'))
    print("Created: grass_middle.png")

    grass_left = create_grass_left_edge()
    pygame.image.save(grass_left, os.path.join(OUTPUT_DIR, 'grass_left.png'))
    print("Created: grass_left.png")

    grass_right = create_grass_right_edge()
    pygame.image.save(grass_right, os.path.join(OUTPUT_DIR, 'grass_right.png'))
    print("Created: grass_right.png")

    # Stone tiles
    stone_tile = create_stone_tile()
    pygame.image.save(stone_tile, os.path.join(OUTPUT_DIR, 'stone_middle.png'))
    print("Created: stone_middle.png")

    stone_left = create_stone_left_edge()
    pygame.image.save(stone_left, os.path.join(OUTPUT_DIR, 'stone_left.png'))
    print("Created: stone_left.png")

    stone_right = create_stone_right_edge()
    pygame.image.save(stone_right, os.path.join(OUTPUT_DIR, 'stone_right.png'))
    print("Created: stone_right.png")

    print("\nAll tiles generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
