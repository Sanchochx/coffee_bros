"""
Generate Bogota city background image.
Grey, depressing urban environment with smog and pollution.
"""

import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Canvas dimensions
WIDTH = 1600
HEIGHT = 600

# Create canvas
canvas = pygame.Surface((WIDTH, HEIGHT))

# Bogota color palette - grey, depressing colors
SKY_GREY = (120, 120, 130)  # Grey smoggy sky
SMOG_LAYER = (140, 140, 145)  # Lighter smog layer
BUILDING_GREY = (90, 90, 95)  # Dark grey buildings
BUILDING_LIGHT = (110, 110, 115)  # Lighter building shade
BUILDING_DARK = (70, 70, 75)  # Darker building shade
WINDOW_DARK = (40, 40, 45)  # Dark windows
WINDOW_LIT = (180, 170, 120)  # Faintly lit windows
ROAD_GREY = (60, 60, 65)  # Dark road
TRASH_COLORS = [(80, 70, 60), (100, 90, 80), (70, 80, 70)]  # Trash bags

# Fill sky with grey smog
canvas.fill(SKY_GREY)

# Add layers of smog for depth
for i in range(3):
    smog_alpha = 30 + i * 20
    smog_y = 50 + i * 80
    smog_height = 120
    smog_surface = pygame.Surface((WIDTH, smog_height), pygame.SRCALPHA)
    smog_surface.fill((*SMOG_LAYER, smog_alpha))
    canvas.blit(smog_surface, (0, smog_y))

# Draw distant mountains (barely visible through smog)
mountain_points = [
    (0, 350),
    (200, 280),
    (400, 320),
    (600, 260),
    (800, 300),
    (1000, 250),
    (1200, 290),
    (1400, 270),
    (WIDTH, 310),
    (WIDTH, 350)
]
pygame.draw.polygon(canvas, (100, 100, 105), mountain_points)

# Draw multiple layers of buildings creating a sad cityscape
building_configs = [
    # Back layer (smaller, more distant)
    {"count": 8, "y_base": 280, "height_range": (120, 180), "x_spacing": 200, "shade": (100, 100, 105)},
    # Middle layer
    {"count": 6, "y_base": 320, "height_range": (180, 260), "x_spacing": 266, "shade": BUILDING_GREY},
    # Front layer (larger, closer)
    {"count": 5, "y_base": 350, "height_range": (200, 350), "x_spacing": 320, "shade": BUILDING_DARK}
]

for layer_config in building_configs:
    x = random.randint(-50, 50)
    for i in range(layer_config["count"]):
        building_width = random.randint(80, 150)
        building_height = random.randint(*layer_config["height_range"])
        building_x = x
        building_y = layer_config["y_base"]

        # Draw building body
        building_color = layer_config["shade"]
        pygame.draw.rect(canvas, building_color,
                        (building_x, building_y, building_width, HEIGHT - building_y))

        # Add building outline (darker)
        pygame.draw.rect(canvas, BUILDING_DARK,
                        (building_x, building_y, building_width, HEIGHT - building_y), 2)

        # Add windows to buildings (most dark, few lit)
        window_rows = (HEIGHT - building_y - 20) // 25
        window_cols = building_width // 20

        for row in range(int(window_rows)):
            for col in range(int(window_cols)):
                window_x = building_x + 5 + col * 20
                window_y = building_y + 10 + row * 25

                # Most windows are dark, occasionally lit (10% chance)
                if random.random() < 0.1:
                    window_color = WINDOW_LIT
                else:
                    window_color = WINDOW_DARK

                pygame.draw.rect(canvas, window_color, (window_x, window_y, 10, 15))

        x += layer_config["x_spacing"]

# Draw polluted road/street at bottom
pygame.draw.rect(canvas, ROAD_GREY, (0, 500, WIDTH, 100))

# Add road markings (faded white lines)
for i in range(0, WIDTH, 80):
    pygame.draw.rect(canvas, (140, 140, 140), (i, 545, 40, 5))

# Add trash and litter on the streets
for _ in range(30):
    trash_x = random.randint(0, WIDTH)
    trash_y = random.randint(480, 550)
    trash_size = random.randint(8, 20)
    trash_color = random.choice(TRASH_COLORS)

    # Draw irregular trash shapes
    if random.random() < 0.5:
        # Trash bag
        pygame.draw.ellipse(canvas, trash_color,
                           (trash_x, trash_y, trash_size, trash_size * 0.8))
    else:
        # Scattered trash
        pygame.draw.rect(canvas, trash_color,
                        (trash_x, trash_y, trash_size, trash_size // 2))

# Add rain effect (light drizzle to enhance sadness)
for _ in range(100):
    rain_x = random.randint(0, WIDTH)
    rain_y = random.randint(0, HEIGHT)
    rain_length = random.randint(10, 20)
    pygame.draw.line(canvas, (150, 150, 155),
                    (rain_x, rain_y),
                    (rain_x + 2, rain_y + rain_length), 1)

# Add smog overlay at the top
smog_overlay = pygame.Surface((WIDTH, 200), pygame.SRCALPHA)
for y in range(200):
    alpha = int(100 * (1 - y / 200))  # Fade from top to bottom
    pygame.draw.line(smog_overlay, (*SMOG_LAYER, alpha), (0, y), (WIDTH, y))
canvas.blit(smog_overlay, (0, 0))

# Save the image
output_path = os.path.join("assets", "images", "bogota_city.png")
pygame.image.save(canvas, output_path)

print(f"Bogota city background saved to {output_path}")
print("A grey, depressing urban environment depicting the sad reality of Colombia's capital.")
