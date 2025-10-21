"""
Generate Chiva bus (Colombian party bus) as level goal
Colorful traditional Colombian bus
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Chiva dimensions (width x height)
CHIVA_WIDTH = 80
CHIVA_HEIGHT = 100


def create_chiva_bus():
    """Create a colorful Colombian Chiva bus sprite"""
    surface = pygame.Surface((CHIVA_WIDTH, CHIVA_HEIGHT), pygame.SRCALPHA)

    # Colombian bright colors for Chiva
    chiva_red = (220, 20, 60)
    chiva_yellow = (255, 209, 0)
    chiva_blue = (0, 56, 168)
    chiva_green = (0, 180, 80)
    chiva_orange = (255, 140, 0)
    wood_brown = (139, 90, 43)
    metal_gray = (120, 120, 120)
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Bus body (main red body)
    pygame.draw.rect(surface, chiva_red, (10, 20, 60, 60))

    # Roof (yellow)
    pygame.draw.polygon(surface, chiva_yellow, [
        (5, 20), (75, 20), (70, 10), (10, 10)
    ])

    # Front of bus
    pygame.draw.rect(surface, chiva_red, (10, 10, 60, 10))

    # Colorful decorative stripes (typical Chiva decoration)
    pygame.draw.rect(surface, chiva_yellow, (10, 25, 60, 5))
    pygame.draw.rect(surface, chiva_blue, (10, 35, 60, 5))
    pygame.draw.rect(surface, chiva_green, (10, 45, 60, 5))
    pygame.draw.rect(surface, chiva_orange, (10, 55, 60, 5))
    pygame.draw.rect(surface, chiva_yellow, (10, 65, 60, 5))

    # Open sides (Chivas have open sides with wooden railings)
    # Left side openings
    for i in range(3):
        y = 30 + i * 15
        pygame.draw.rect(surface, (0, 0, 0, 0), (12, y, 8, 12))  # Window opening

    # Right side openings
    for i in range(3):
        y = 30 + i * 15
        pygame.draw.rect(surface, (0, 0, 0, 0), (60, y, 8, 12))  # Window opening

    # Wooden railings
    for i in range(4):
        y = 28 + i * 13
        pygame.draw.line(surface, wood_brown, (10, y), (15, y), 2)
        pygame.draw.line(surface, wood_brown, (65, y), (70, y), 2)

    # Front windshield
    pygame.draw.rect(surface, (150, 200, 255), (20, 12, 18, 6))
    pygame.draw.rect(surface, (150, 200, 255), (45, 12, 18, 6))

    # Headlights
    pygame.draw.circle(surface, chiva_yellow, (18, 18), 3)
    pygame.draw.circle(surface, chiva_yellow, (62, 18), 3)

    # Wheels (big, visible wheels)
    wheel_color = black
    wheel_rim = metal_gray

    # Front wheel
    pygame.draw.circle(surface, wheel_color, (20, 82), 10)
    pygame.draw.circle(surface, wheel_rim, (20, 82), 5)

    # Back wheel
    pygame.draw.circle(surface, wheel_color, (60, 82), 10)
    pygame.draw.circle(surface, wheel_rim, (60, 82), 5)

    # Destination sign on front (Colombian style)
    pygame.draw.rect(surface, white, (25, 14, 30, 4))
    # Add "MEDALLO" text effect (simplified)
    pygame.draw.rect(surface, chiva_blue, (27, 15, 2, 2))
    pygame.draw.rect(surface, chiva_red, (31, 15, 2, 2))
    pygame.draw.rect(surface, chiva_yellow, (35, 15, 2, 2))

    # Add Colombian flag on roof
    flag_x, flag_y = 35, 8
    # Yellow
    pygame.draw.rect(surface, (255, 209, 0), (flag_x, flag_y, 12, 3))
    # Blue
    pygame.draw.rect(surface, (0, 56, 168), (flag_x, flag_y + 3, 12, 1))
    # Red
    pygame.draw.rect(surface, (206, 17, 38), (flag_x, flag_y + 4, 12, 1))

    # Border outline for visibility
    pygame.draw.rect(surface, black, (10, 10, 60, 72), 2)

    return surface


def main():
    """Generate and save Chiva bus sprite"""
    output_dir = "assets/images"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Colombian Chiva Bus...")
    print("The iconic colorful party bus of Colombia!")

    chiva = create_chiva_bus()
    output_file = os.path.join(output_dir, "chiva_bus.png")
    pygame.image.save(chiva, output_file)

    print(f"Created chiva_bus.png ({CHIVA_WIDTH}x{CHIVA_HEIGHT})")
    print("Colombian Chiva is ready to be the level goal!")


if __name__ == "__main__":
    main()
