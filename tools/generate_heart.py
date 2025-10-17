"""
Heart sprite generator for lives HUD display
Generates a heart icon for displaying player lives
"""

import pygame
import os

# Initialize pygame for surface creation
pygame.init()

# Heart size
HEART_SIZE = 30

# Output directory
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def create_heart():
    """Create a heart sprite (30x30)"""
    heart = pygame.Surface((HEART_SIZE, HEART_SIZE), pygame.SRCALPHA)

    # Heart color - bright red
    RED = (255, 50, 50)
    DARK_RED = (200, 30, 30)

    # Draw heart shape using circles and a polygon
    # Two circles for the top bumps
    pygame.draw.circle(heart, RED, (10, 10), 8)
    pygame.draw.circle(heart, RED, (20, 10), 8)

    # Triangle for the bottom point
    points = [
        (3, 12),   # Left
        (27, 12),  # Right
        (15, 26)   # Bottom point
    ]
    pygame.draw.polygon(heart, RED, points)

    # Add a filled rectangle in the middle to connect everything
    pygame.draw.rect(heart, RED, (3, 10, 24, 10))

    # Add a subtle highlight for depth
    LIGHT_RED = (255, 100, 100)
    pygame.draw.circle(heart, LIGHT_RED, (12, 8), 3)

    # Add border for definition
    pygame.draw.circle(heart, DARK_RED, (10, 10), 8, 1)
    pygame.draw.circle(heart, DARK_RED, (20, 10), 8, 1)
    pygame.draw.polygon(heart, DARK_RED, points, 1)

    return heart


def main():
    """Generate heart sprite"""
    print("Generating heart sprite for lives display...")

    heart = create_heart()
    pygame.image.save(heart, os.path.join(OUTPUT_DIR, 'heart.png'))
    print("Created: heart.png")

    print("\nHeart sprite generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
