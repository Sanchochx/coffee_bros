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
BOSS_WIDTH = 200
BOSS_HEIGHT = 240

def create_corruption_boss_sprite():
    """
    Create a corrupt politician boss sprite
    Human figure in suit with dollar sign eyes - representing political corruption
    Scaled to 200x240 (33% larger than original 150x180)
    """
    surface = pygame.Surface((BOSS_WIDTH, BOSS_HEIGHT), pygame.SRCALPHA)

    # Skin tone
    skin_color = (210, 180, 140)
    skin_shadow = (180, 150, 110)

    # Draw head (oval) - scaled
    head_center_x = 100
    head_center_y = 67
    pygame.draw.ellipse(surface, skin_color, (67, 33, 67, 80))  # Face
    pygame.draw.ellipse(surface, skin_shadow, (67, 33, 67, 80), 2)  # Face outline

    # Draw evil smirk
    mouth_color = (80, 20, 20)
    pygame.draw.arc(surface, mouth_color, (80, 73, 40, 27), math.pi, 0, 4)  # Smirk

    # Draw DOLLAR SIGN EYES (green money symbols)
    money_green = (0, 180, 0)
    font = pygame.font.Font(None, 53)  # Scaled font
    # Left eye
    dollar_left = font.render("$", True, money_green)
    surface.blit(dollar_left, (73, 47))
    # Right eye
    dollar_right = font.render("$", True, money_green)
    surface.blit(dollar_right, (107, 47))

    # Draw slicked-back hair (corrupt politician style)
    hair_color = (40, 40, 40)
    pygame.draw.ellipse(surface, hair_color, (64, 27, 72, 40))  # Hair top

    # Draw neck
    pygame.draw.rect(surface, skin_shadow, (87, 107, 27, 20))

    # Draw black suit jacket
    suit_color = (20, 20, 25)
    suit_highlight = (40, 40, 50)

    # Jacket body (trapezoid shape) - scaled
    jacket_points = [
        (60, 127),   # Top left shoulder
        (140, 127),  # Top right shoulder
        (160, 240),  # Bottom right
        (40, 240),   # Bottom left
    ]
    pygame.draw.polygon(surface, suit_color, jacket_points)

    # Jacket lapels
    pygame.draw.polygon(surface, suit_highlight, [(60, 127), (80, 127), (93, 173)])  # Left lapel
    pygame.draw.polygon(surface, suit_highlight, [(140, 127), (120, 127), (107, 173)])  # Right lapel

    # White dress shirt
    shirt_white = (240, 240, 245)
    pygame.draw.polygon(surface, shirt_white, [(87, 127), (113, 127), (113, 187), (87, 187)])

    # Red power tie (corrupt politician red tie)
    tie_red = (180, 0, 0)
    pygame.draw.polygon(surface, tie_red, [(96, 127), (104, 127), (107, 187), (93, 187)])

    # Tie knot
    pygame.draw.polygon(surface, (140, 0, 0), [(93, 127), (107, 127), (104, 136), (96, 136)])

    # Arms (reaching for money)
    # Left arm
    pygame.draw.rect(surface, suit_color, (33, 147, 27, 67))
    pygame.draw.circle(surface, skin_color, (47, 213), 13)  # Left hand

    # Right arm
    pygame.draw.rect(surface, suit_color, (140, 147, 27, 67))
    pygame.draw.circle(surface, skin_color, (153, 213), 13)  # Right hand

    # Money bags in hands (symbols of corruption)
    bag_color = (100, 200, 100)
    # Left money bag
    pygame.draw.circle(surface, bag_color, (47, 220), 11)
    money_font = pygame.font.Font(None, 27)
    dollar = money_font.render("$", True, (0, 100, 0))
    surface.blit(dollar, (41, 211))

    # Right money bag
    pygame.draw.circle(surface, bag_color, (153, 220), 11)
    surface.blit(dollar, (147, 211))

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
