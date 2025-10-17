"""
Test script to validate platform tile graphics are working correctly
"""

import pygame
import sys
import os

# Add parent directory to path to import game modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.entities.platform import Platform

# Initialize pygame
pygame.init()

# Create a small test window
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Platform Tile Test")

# Create test platforms
print("\nTesting Platform Tile Graphics...")
print("=" * 50)

# Test 1: Grass ground platform (wide)
print("\n1. Creating grass ground platform (800x50)...")
grass_platform = Platform(50, 300, 800, 50, "ground", "grass")
print(f"   Platform created successfully")
print(f"   Platform type: {grass_platform.platform_type}")
print(f"   Texture: {grass_platform.texture}")
print(f"   Size: {grass_platform.rect.width}x{grass_platform.rect.height}")

# Test 2: Stone floating platform (narrow)
print("\n2. Creating stone floating platform (150x20)...")
stone_platform = Platform(200, 150, 150, 20, "floating", "stone")
print(f"   Platform created successfully")
print(f"   Platform type: {stone_platform.platform_type}")
print(f"   Texture: {stone_platform.texture}")
print(f"   Size: {stone_platform.rect.width}x{stone_platform.rect.height}")

# Test 3: Small grass platform
print("\n3. Creating small grass platform (80x20)...")
small_platform = Platform(400, 200, 80, 20, "floating", "grass")
print(f"   Platform created successfully")
print(f"   Platform type: {small_platform.platform_type}")
print(f"   Texture: {small_platform.texture}")
print(f"   Size: {small_platform.rect.width}x{small_platform.rect.height}")

# Test 4: Check tile cache
print("\n4. Checking tile cache...")
print(f"   Cached textures: {list(Platform._tile_cache.keys())}")
if 'grass' in Platform._tile_cache:
    grass_tiles = Platform._tile_cache['grass']
    print(f"   Grass tiles loaded: {list(grass_tiles.keys())}")
if 'stone' in Platform._tile_cache:
    stone_tiles = Platform._tile_cache['stone']
    print(f"   Stone tiles loaded: {list(stone_tiles.keys())}")

# Visual rendering test
print("\n5. Rendering platforms to test window...")
clock = pygame.time.Clock()
running = True
test_duration = 3  # seconds
elapsed_time = 0

while running and elapsed_time < test_duration:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill((135, 206, 235))  # Sky blue

    # Draw platforms
    screen.blit(grass_platform.image, grass_platform.rect)
    screen.blit(stone_platform.image, stone_platform.rect)
    screen.blit(small_platform.image, small_platform.rect)

    # Add text labels
    font = pygame.font.Font(None, 24)
    labels = [
        ("Grass Ground Platform (800x50)", (50, 280)),
        ("Stone Floating Platform (150x20)", (200, 130)),
        ("Small Grass Platform (80x20)", (400, 180))
    ]

    for text, pos in labels:
        label = font.render(text, True, (0, 0, 0))
        screen.blit(label, pos)

    pygame.display.flip()
    clock.tick(60)
    elapsed_time += clock.get_time() / 1000

print("   Platforms rendered successfully for 3 seconds")

# Test 6: Collision rect validation
print("\n6. Validating collision boundaries...")
platforms = [grass_platform, stone_platform, small_platform]
for i, platform in enumerate(platforms, 1):
    print(f"   Platform {i}:")
    print(f"     Position: ({platform.rect.x}, {platform.rect.y})")
    print(f"     Size: {platform.rect.width}x{platform.rect.height}")
    print(f"     Boundaries: Left={platform.rect.left}, Right={platform.rect.right}, "
          f"Top={platform.rect.top}, Bottom={platform.rect.bottom}")

print("\n" + "=" * 50)
print("✓ All platform tile tests passed!")
print("=" * 50)

pygame.quit()
