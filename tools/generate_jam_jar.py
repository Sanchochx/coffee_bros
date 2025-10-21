"""
Generate a purple jam jar sprite for level 5 goal.
Creates a jar of purple jam with label and lid.
"""

import pygame
import os

def create_jam_jar_sprite(width=50, height=80):
    """
    Create a purple jam jar sprite.

    Args:
        width: Width of the sprite
        height: Height of the sprite

    Returns:
        pygame.Surface: Jam jar sprite
    """
    # Initialize pygame if not already initialized
    if not pygame.get_init():
        pygame.init()

    # Create surface with transparency
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))  # Transparent background

    # Color palette
    glass_color = (200, 230, 255, 180)  # Light blue-ish transparent glass
    glass_highlight = (255, 255, 255, 100)  # Glass shine
    purple_jam = (120, 40, 150)  # Deep purple jam color
    jam_highlight = (160, 80, 180)  # Lighter purple for depth
    lid_gold = (218, 165, 32)  # Golden lid
    lid_shadow = (180, 130, 20)  # Darker gold for shadow
    label_cream = (255, 250, 220)  # Cream label
    label_border = (200, 180, 150)  # Label border

    # Proportions
    jar_width = int(width * 0.85)
    jar_height = int(height * 0.7)
    lid_height = int(height * 0.15)

    # Center the jar
    jar_x = (width - jar_width) // 2
    jar_y = height - jar_height

    # Draw jar body (rounded rectangle for glass jar)
    jar_rect = pygame.Rect(jar_x, jar_y, jar_width, jar_height)
    # Main jar body
    pygame.draw.rect(surface, glass_color, jar_rect, border_radius=8)

    # Draw jam inside jar (slightly smaller than jar)
    jam_margin = 3
    jam_height = int(jar_height * 0.75)  # Jar is 75% full
    jam_rect = pygame.Rect(
        jar_x + jam_margin,
        jar_y + (jar_height - jam_height) + jam_margin,
        jar_width - jam_margin * 2,
        jam_height - jam_margin
    )
    pygame.draw.rect(surface, purple_jam, jam_rect, border_radius=6)

    # Add jam highlights for texture (bubbles/depth)
    jam_highlight_rect = pygame.Rect(
        jar_x + jam_margin + 2,
        jam_rect.top + 2,
        int(jar_width * 0.4),
        int(jam_height * 0.3)
    )
    pygame.draw.ellipse(surface, jam_highlight, jam_highlight_rect)

    # Draw small jam bubbles
    bubble_positions = [
        (jar_x + jar_width // 4, jam_rect.top + jam_height // 3),
        (jar_x + 3 * jar_width // 4, jam_rect.top + 2 * jam_height // 3),
        (jar_x + jar_width // 2, jam_rect.top + jam_height // 2)
    ]
    for bx, by in bubble_positions:
        pygame.draw.circle(surface, jam_highlight, (bx, by), 3)

    # Draw glass shine/reflection
    shine_rect = pygame.Rect(
        jar_x + jar_width - 12,
        jar_y + 8,
        8,
        int(jar_height * 0.6)
    )
    pygame.draw.ellipse(surface, glass_highlight, shine_rect)

    # Draw lid
    lid_y = jar_y - lid_height
    lid_rect = pygame.Rect(jar_x - 2, lid_y, jar_width + 4, lid_height)
    pygame.draw.rect(surface, lid_gold, lid_rect, border_radius=3)

    # Lid shadow/depth
    pygame.draw.line(surface, lid_shadow,
                     (jar_x - 2, lid_y + lid_height - 2),
                     (jar_x + jar_width + 2, lid_y + lid_height - 2), 2)

    # Lid ridges (texture)
    for i in range(3):
        ridge_y = lid_y + 3 + i * 3
        pygame.draw.line(surface, lid_shadow,
                        (jar_x, ridge_y),
                        (jar_x + jar_width, ridge_y), 1)

    # Draw label on jar
    label_width = int(jar_width * 0.75)
    label_height = int(jar_height * 0.3)
    label_x = jar_x + (jar_width - label_width) // 2
    label_y = jar_y + (jar_height - jam_height) + 5
    label_rect = pygame.Rect(label_x, label_y, label_width, label_height)
    pygame.draw.rect(surface, label_cream, label_rect, border_radius=4)
    pygame.draw.rect(surface, label_border, label_rect, 1, border_radius=4)

    # Add text "JAM" on label (simple pixel art style)
    # Draw decorative wavy lines above and below center
    pygame.draw.line(surface, purple_jam,
                     (label_x + 3, label_y + label_height // 3),
                     (label_x + label_width - 3, label_y + label_height // 3), 1)
    pygame.draw.line(surface, purple_jam,
                     (label_x + 3, label_y + 2 * label_height // 3),
                     (label_x + label_width - 3, label_y + 2 * label_height // 3), 1)

    # Draw small purple dots pattern on label
    for i in range(3):
        dot_x = label_x + 5 + i * 8
        dot_y = label_y + label_height // 2
        pygame.draw.circle(surface, purple_jam, (dot_x, dot_y), 2)

    return surface


if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = os.path.join("assets", "images")
    os.makedirs(output_dir, exist_ok=True)

    # Generate the jam jar sprite
    jam_jar = create_jam_jar_sprite(50, 80)

    # Save the sprite
    output_path = os.path.join(output_dir, "purple_jam_jar.png")
    pygame.image.save(jam_jar, output_path)

    print(f"Purple jam jar sprite generated successfully: {output_path}")

    pygame.quit()
