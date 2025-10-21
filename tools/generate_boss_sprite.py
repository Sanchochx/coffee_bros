"""
Generate the Corruption Boss sprite for Coffee Bros final level
Creates a large, menacing corruption monster
"""

import pygame
import os
import math

# Initialize pygame
pygame.init()

# Boss sprite dimensions (much larger than regular enemies)
BOSS_WIDTH = 150
BOSS_HEIGHT = 180

def create_corruption_boss_sprite():
    """
    Create a corrupt politician boss sprite
    Human figure in suit with dollar sign eyes - representing political corruption
    """
    surface = pygame.Surface((BOSS_WIDTH, BOSS_HEIGHT), pygame.SRCALPHA)

    # Skin tone
    skin_color = (210, 180, 140)
    skin_shadow = (180, 150, 110)

    # Draw head (oval)
    head_center_x = 75
    head_center_y = 50
    pygame.draw.ellipse(surface, skin_color, (50, 25, 50, 60))  # Face
    pygame.draw.ellipse(surface, skin_shadow, (50, 25, 50, 60), 2)  # Face outline

    # Draw evil smirk
    mouth_color = (80, 20, 20)
    pygame.draw.arc(surface, mouth_color, (60, 55, 30, 20), math.pi, 0, 3)  # Smirk

    # Draw DOLLAR SIGN EYES (green money symbols)
    money_green = (0, 180, 0)
    font = pygame.font.Font(None, 40)
    # Left eye
    dollar_left = font.render("$", True, money_green)
    surface.blit(dollar_left, (55, 35))
    # Right eye
    dollar_right = font.render("$", True, money_green)
    surface.blit(dollar_right, (80, 35))

    # Draw slicked-back hair (corrupt politician style)
    hair_color = (40, 40, 40)
    pygame.draw.ellipse(surface, hair_color, (48, 20, 54, 30))  # Hair top

    # Draw neck
    pygame.draw.rect(surface, skin_shadow, (65, 80, 20, 15))

    # Draw black suit jacket
    suit_color = (20, 20, 25)
    suit_highlight = (40, 40, 50)

    # Jacket body (trapezoid shape)
    jacket_points = [
        (45, 95),   # Top left shoulder
        (105, 95),  # Top right shoulder
        (120, 180), # Bottom right
        (30, 180),  # Bottom left
    ]
    pygame.draw.polygon(surface, suit_color, jacket_points)

    # Jacket lapels
    pygame.draw.polygon(surface, suit_highlight, [(45, 95), (60, 95), (70, 130)])  # Left lapel
    pygame.draw.polygon(surface, suit_highlight, [(105, 95), (90, 95), (80, 130)])  # Right lapel

    # White dress shirt
    shirt_white = (240, 240, 245)
    pygame.draw.polygon(surface, shirt_white, [(65, 95), (85, 95), (85, 140), (65, 140)])

    # Red power tie (corrupt politician red tie)
    tie_red = (180, 0, 0)
    pygame.draw.polygon(surface, tie_red, [(72, 95), (78, 95), (80, 140), (70, 140)])

    # Tie knot
    pygame.draw.polygon(surface, (140, 0, 0), [(70, 95), (80, 95), (78, 102), (72, 102)])

    # Arms (reaching for money)
    # Left arm
    pygame.draw.rect(surface, suit_color, (25, 110, 20, 50))
    pygame.draw.circle(surface, skin_color, (35, 160), 10)  # Left hand

    # Right arm
    pygame.draw.rect(surface, suit_color, (105, 110, 20, 50))
    pygame.draw.circle(surface, skin_color, (115, 160), 10)  # Right hand

    # Money bags in hands (symbols of corruption)
    bag_color = (100, 200, 100)
    # Left money bag
    pygame.draw.circle(surface, bag_color, (35, 165), 8)
    money_font = pygame.font.Font(None, 20)
    dollar = money_font.render("$", True, (0, 100, 0))
    surface.blit(dollar, (31, 158))

    # Right money bag
    pygame.draw.circle(surface, bag_color, (115, 165), 8)
    surface.blit(dollar, (111, 158))

    return surface


def create_boss_hit_sprite():
    """Create a 'damaged' version of the boss with blood-red overlay"""
    surface = create_corruption_boss_sprite()

    # Create blood-red flash overlay for hit effect
    blood_flash = pygame.Surface((BOSS_WIDTH, BOSS_HEIGHT), pygame.SRCALPHA)
    blood_flash.fill((255, 0, 0, 120))  # Blood red with transparency
    surface.blit(blood_flash, (0, 0))

    return surface


def main():
    """Generate and save boss sprites"""
    # Create output directory
    output_dir = "assets/images/boss"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Corruption Boss sprite...")

    # Create normal boss sprite
    boss_sprite = create_corruption_boss_sprite()
    pygame.image.save(boss_sprite, os.path.join(output_dir, "corruption_boss.png"))
    print(f"  Created corruption_boss.png ({BOSS_WIDTH}x{BOSS_HEIGHT})")

    # Create hit/damaged sprite
    boss_hit = create_boss_hit_sprite()
    pygame.image.save(boss_hit, os.path.join(output_dir, "corruption_boss_hit.png"))
    print(f"  Created corruption_boss_hit.png")

    print(f"\nBoss sprites saved to: {output_dir}/")
    print("The Corruption Boss is ready to defend the castle!")


if __name__ == "__main__":
    main()
