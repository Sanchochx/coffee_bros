"""
Script to generate background images for all levels.
Each background features Colombian highlands theme with sky, mountains, and coffee plants.
"""

import pygame
import os

# Initialize Pygame
pygame.init()

# Background dimensions (width matches level width from JSON)
BACKGROUNDS = {
    "coffee_hills": {
        "width": 3200,
        "height": 600,
        "sky_color": (135, 206, 250),  # Sky blue
        "mountain_colors": [(101, 67, 33), (139, 90, 43), (160, 100, 50)],  # Brown mountain shades
        "grass_color": (34, 139, 34),  # Forest green
        "coffee_plant_color": (0, 100, 0),  # Dark green for coffee plants
    },
    "mountain_paths": {
        "width": 3200,
        "height": 600,
        "sky_color": (120, 180, 240),  # Slightly different blue
        "mountain_colors": [(90, 60, 30), (120, 80, 40), (140, 95, 50)],  # Darker mountains
        "grass_color": (46, 125, 50),  # Medium green
        "coffee_plant_color": (0, 90, 0),
    },
    "bean_valley": {
        "width": 3200,
        "height": 600,
        "sky_color": (150, 200, 255),  # Lighter sky
        "mountain_colors": [(110, 70, 35), (150, 95, 48), (170, 110, 60)],  # Lighter mountains
        "grass_color": (60, 150, 60),  # Bright green valley
        "coffee_plant_color": (0, 110, 0),
    },
    "harvest_heights": {
        "width": 3200,
        "height": 600,
        "sky_color": (100, 150, 220),  # Evening sky
        "mountain_colors": [(80, 50, 25), (110, 70, 35), (130, 85, 45)],  # Darker evening mountains
        "grass_color": (40, 110, 40),  # Darker grass
        "coffee_plant_color": (0, 80, 0),
    },
    "el_pico_del_cafe": {
        "width": 3200,
        "height": 600,
        "sky_color": (70, 120, 200),  # Dramatic sky for final level
        "mountain_colors": [(60, 40, 20), (90, 60, 30), (110, 75, 38)],  # Dramatic dark mountains
        "grass_color": (30, 90, 30),  # Dark grass
        "coffee_plant_color": (0, 70, 0),
    }
}


def draw_mountain(surface, points, color):
    """Draw a mountain polygon on the surface."""
    pygame.draw.polygon(surface, color, points)


def draw_coffee_plant(surface, x, y, color):
    """Draw a simple coffee plant representation."""
    # Draw stem
    pygame.draw.line(surface, color, (x, y), (x, y - 30), 3)
    # Draw leaves (simple oval shapes)
    pygame.draw.ellipse(surface, color, (x - 10, y - 25, 12, 20))
    pygame.draw.ellipse(surface, color, (x - 2, y - 25, 12, 20))
    # Draw coffee beans (red dots)
    pygame.draw.circle(surface, (200, 50, 50), (x - 5, y - 15), 3)
    pygame.draw.circle(surface, (200, 50, 50), (x + 5, y - 20), 3)


def generate_background(bg_name, bg_data, output_path):
    """Generate a background image and save it."""
    width = bg_data["width"]
    height = bg_data["height"]

    # Create surface
    surface = pygame.Surface((width, height))

    # Fill sky
    surface.fill(bg_data["sky_color"])

    # Draw distant mountains (background layer)
    mountain_height = height // 2
    num_peaks = 8
    peak_spacing = width // num_peaks

    for i in range(num_peaks):
        peak_x = i * peak_spacing + peak_spacing // 2
        peak_y = mountain_height - 150 + (i % 3) * 30  # Vary height

        # Create mountain triangle
        points = [
            (peak_x - peak_spacing // 2, height),  # Bottom left
            (peak_x, peak_y),  # Peak
            (peak_x + peak_spacing // 2, height),  # Bottom right
        ]

        # Use different shades for depth
        color = bg_data["mountain_colors"][i % len(bg_data["mountain_colors"])]
        draw_mountain(surface, points, color)

    # Draw grass hills (foreground ground layer)
    grass_start_y = height - 100
    pygame.draw.rect(surface, bg_data["grass_color"], (0, grass_start_y, width, 100))

    # Add some rolling hills to grass
    for i in range(0, width, 200):
        hill_points = [
            (i, grass_start_y + 20),
            (i + 100, grass_start_y - 10),
            (i + 200, grass_start_y + 20),
        ]
        pygame.draw.polygon(surface,
                           (bg_data["grass_color"][0] - 10,
                            bg_data["grass_color"][1] - 10,
                            bg_data["grass_color"][2] - 10),
                           hill_points)

    # Draw coffee plants scattered across the foreground
    plant_y = grass_start_y + 15
    for i in range(0, width, 150):
        offset = (i * 7) % 50  # Pseudo-random offset
        plant_x = i + offset
        draw_coffee_plant(surface, plant_x, plant_y, bg_data["coffee_plant_color"])

    # Add some clouds to the sky
    cloud_color = (255, 255, 255, 100)  # White with transparency
    for i in range(0, width, 400):
        cloud_x = i + ((i * 3) % 100)
        cloud_y = 50 + ((i * 5) % 80)
        # Draw cloud as overlapping circles
        pygame.draw.circle(surface, (240, 240, 240), (cloud_x, cloud_y), 30)
        pygame.draw.circle(surface, (240, 240, 240), (cloud_x + 25, cloud_y + 5), 25)
        pygame.draw.circle(surface, (240, 240, 240), (cloud_x + 50, cloud_y), 30)

    # Save the image
    pygame.image.save(surface, output_path)
    print(f"Generated: {output_path}")


def main():
    """Generate all background images."""
    # Create output directory if it doesn't exist
    output_dir = "assets/images"
    os.makedirs(output_dir, exist_ok=True)

    # Generate each background
    for bg_name, bg_data in BACKGROUNDS.items():
        output_path = os.path.join(output_dir, f"{bg_name}.png")
        generate_background(bg_name, bg_data, output_path)

    print("\nAll backgrounds generated successfully!")
    pygame.quit()


if __name__ == "__main__":
    main()
