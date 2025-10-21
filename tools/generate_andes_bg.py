"""
Generate Andes mountain range background for level 2
"""
import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Dimensions
WIDTH = 4000
HEIGHT = 600

# Create surface
surface = pygame.Surface((WIDTH, HEIGHT))

# Color palette - Andes mountains with snow peaks
sky_top = (135, 206, 235)  # Light blue sky
sky_bottom = (176, 224, 230)  # Lighter blue near horizon
mountain_dark = (80, 70, 60)  # Dark brown/gray
mountain_mid = (110, 100, 90)  # Mid brown/gray
mountain_light = (140, 130, 120)  # Light brown/gray
snow_peak = (250, 250, 255)  # Snow white with slight blue tint
snow_shadow = (220, 230, 240)  # Snow in shadow
grass_dark = (60, 90, 50)  # Dark green grass
grass_light = (80, 110, 70)  # Light green grass

# Draw gradient sky
for y in range(HEIGHT // 2):
    ratio = y / (HEIGHT // 2)
    r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * ratio)
    g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * ratio)
    b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * ratio)
    pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# Fill lower half with horizon color
surface.fill(sky_bottom, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))

# Function to draw a mountain peak
def draw_mountain(surface, peak_x, peak_y, base_width, color_dark, color_light, has_snow=False):
    # Main mountain body
    points = [
        (peak_x, peak_y),
        (peak_x - base_width // 2, HEIGHT),
        (peak_x + base_width // 2, HEIGHT)
    ]
    pygame.draw.polygon(surface, color_dark, points)

    # Lighter side (left side lit)
    light_points = [
        (peak_x, peak_y),
        (peak_x - base_width // 2, HEIGHT),
        (peak_x, HEIGHT)
    ]
    pygame.draw.polygon(surface, color_light, light_points)

    # Snow cap if needed
    if has_snow:
        snow_height = int((HEIGHT - peak_y) * 0.3)
        snow_points = [
            (peak_x, peak_y),
            (peak_x - base_width // 6, peak_y + snow_height),
            (peak_x + base_width // 6, peak_y + snow_height)
        ]
        pygame.draw.polygon(surface, snow_peak, snow_points)

        # Snow shadow on right side
        shadow_points = [
            (peak_x, peak_y),
            (peak_x + base_width // 6, peak_y + snow_height),
            (peak_x, peak_y + snow_height)
        ]
        pygame.draw.polygon(surface, snow_shadow, shadow_points)

# Draw distant mountains (background layer)
distant_mountains = [
    (500, 250, 800, mountain_light, mountain_mid, True),
    (1200, 200, 900, mountain_light, mountain_mid, True),
    (1900, 220, 850, mountain_light, mountain_mid, True),
    (2700, 180, 1000, mountain_light, mountain_mid, True),
    (3400, 240, 900, mountain_light, mountain_mid, True),
]

for mx, my, mw, mc1, mc2, snow in distant_mountains:
    draw_mountain(surface, mx, my, mw, mc2, mc1, snow)

# Draw mid-ground mountains
mid_mountains = [
    (300, 300, 700, mountain_mid, mountain_light, True),
    (950, 280, 750, mountain_mid, mountain_light, True),
    (1650, 260, 800, mountain_mid, mountain_light, True),
    (2350, 290, 780, mountain_mid, mountain_light, True),
    (3100, 270, 820, mountain_mid, mountain_light, True),
    (3750, 310, 700, mountain_mid, mountain_light, True),
]

for mx, my, mw, mc1, mc2, snow in mid_mountains:
    draw_mountain(surface, mx, my, mw, mc1, mc2, snow)

# Draw foreground mountains
front_mountains = [
    (150, 350, 600, mountain_dark, mountain_mid, False),
    (700, 340, 650, mountain_dark, mountain_mid, False),
    (1350, 330, 700, mountain_dark, mountain_mid, False),
    (2050, 360, 680, mountain_dark, mountain_mid, False),
    (2800, 345, 720, mountain_dark, mountain_mid, False),
    (3500, 355, 650, mountain_dark, mountain_mid, False),
]

for mx, my, mw, mc1, mc2, snow in front_mountains:
    draw_mountain(surface, mx, my, mw, mc1, mc2, snow)

# Add some grass/vegetation on lower slopes
for i in range(0, WIDTH, 20):
    # Varying grass patches
    grass_y = HEIGHT - 50 - int(np.sin(i * 0.01) * 20)
    grass_color = grass_dark if (i // 20) % 2 == 0 else grass_light
    pygame.draw.circle(surface, grass_color, (i, grass_y), 8)

# Add some clouds
cloud_color = (255, 255, 255, 180)
cloud_positions = [
    (300, 80), (800, 120), (1400, 70), (2000, 100), (2600, 90), (3200, 110), (3700, 85)
]

for cx, cy in cloud_positions:
    # Draw fluffy clouds
    pygame.draw.ellipse(surface, (255, 255, 255), (cx, cy, 120, 40))
    pygame.draw.ellipse(surface, (255, 255, 255), (cx + 20, cy - 10, 90, 35))
    pygame.draw.ellipse(surface, (255, 255, 255), (cx + 50, cy, 100, 38))

# Save the image
pygame.image.save(surface, "assets/images/andes_mountains.png")
print("Andes mountain background generated successfully!")

pygame.quit()
