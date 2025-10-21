"""
Generate Amazon jungle background for level 3
"""
import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Dimensions
WIDTH = 4800
HEIGHT = 600

# Create surface
surface = pygame.Surface((WIDTH, HEIGHT))

# Color palette - Amazon jungle
sky_top = (100, 180, 220)  # Sky blue visible through canopy
sky_mid = (120, 190, 210)
jungle_dark_green = (20, 60, 30)  # Deep jungle shadows
jungle_green = (40, 80, 45)  # Dark jungle
jungle_mid_green = (60, 120, 65)  # Mid-tone jungle
jungle_light_green = (80, 150, 85)  # Lighter foliage
leaf_bright = (100, 180, 100)  # Bright leaves
leaf_yellow = (150, 200, 100)  # Yellow-green leaves
tree_trunk = (60, 40, 20)  # Dark brown tree trunks
tree_trunk_light = (90, 60, 35)  # Lighter brown
vine_green = (70, 130, 75)  # Vines
fern_green = (85, 160, 90)  # Ferns
water_blue = (80, 140, 160)  # River water glimpse
mist = (200, 220, 210)  # Jungle mist

# Draw gradient sky (barely visible through dense canopy)
for y in range(HEIGHT // 3):
    ratio = y / (HEIGHT // 3)
    r = int(sky_top[0] + (sky_mid[0] - sky_top[0]) * ratio)
    g = int(sky_top[1] + (sky_mid[1] - sky_top[1]) * ratio)
    b = int(sky_top[2] + (sky_mid[2] - sky_top[2]) * ratio)
    pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# Fill rest with jungle canopy gradient
for y in range(HEIGHT // 3, HEIGHT):
    progress = (y - HEIGHT // 3) / (2 * HEIGHT // 3)
    r = int(jungle_mid_green[0] + (jungle_dark_green[0] - jungle_mid_green[0]) * progress)
    g = int(jungle_mid_green[1] + (jungle_dark_green[1] - jungle_mid_green[1]) * progress)
    b = int(jungle_mid_green[2] + (jungle_dark_green[2] - jungle_mid_green[2]) * progress)
    pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

# Function to draw a tree trunk
def draw_tree_trunk(x, y, width, height, color_dark, color_light):
    # Main trunk
    pygame.draw.rect(surface, color_dark, (x, y, width, height))
    # Highlight on left side
    pygame.draw.rect(surface, color_light, (x, y, width // 3, height))
    # Add some bark texture
    for i in range(5):
        bark_y = y + (height // 5) * i + random.randint(-5, 5)
        pygame.draw.line(surface, color_dark, (x, bark_y), (x + width, bark_y), 2)

# Function to draw foliage cluster
def draw_foliage(x, y, radius, color):
    # Draw multiple overlapping circles for leafy effect
    for _ in range(8):
        offset_x = random.randint(-radius//2, radius//2)
        offset_y = random.randint(-radius//2, radius//2)
        r = radius + random.randint(-10, 10)
        pygame.draw.circle(surface, color, (x + offset_x, y + offset_y), r)

# Function to draw a palm frond
def draw_palm_frond(x, y, length, angle, color):
    # Calculate end point
    end_x = x + int(length * np.cos(np.radians(angle)))
    end_y = y + int(length * np.sin(np.radians(angle)))

    # Draw main stem
    pygame.draw.line(surface, color, (x, y), (end_x, end_y), 3)

    # Draw leaves along the frond
    segments = 10
    for i in range(segments):
        t = i / segments
        px = int(x + (end_x - x) * t)
        py = int(y + (end_y - y) * t)
        leaf_size = int(15 * (1 - t))  # Smaller leaves towards tip

        # Left leaf
        pygame.draw.line(surface, color, (px, py),
                        (px - leaf_size, py + leaf_size//2), 2)
        # Right leaf
        pygame.draw.line(surface, color, (px, py),
                        (px + leaf_size, py + leaf_size//2), 2)

# Function to draw hanging vines
def draw_vine(x_start, y_start, length):
    points = []
    x = x_start
    y = y_start

    for i in range(int(length // 10)):
        points.append((x, y))
        x += random.randint(-3, 3)
        y += 10

    if len(points) > 1:
        pygame.draw.lines(surface, vine_green, False, points, 3)
        # Add leaves on vine
        for i in range(len(points) // 3):
            px, py = points[i * 3]
            pygame.draw.ellipse(surface, leaf_bright, (px - 5, py, 10, 15))

# Draw distant jungle layer
random.seed(42)
for i in range(0, WIDTH, 100):
    x = i + random.randint(-20, 20)
    y = 150 + random.randint(-30, 30)
    draw_foliage(x, y, 40, jungle_light_green)

# Draw background trees
for i in range(0, WIDTH, 150):
    x = i + random.randint(-30, 30)
    trunk_height = random.randint(200, 300)
    y = HEIGHT - trunk_height
    draw_tree_trunk(x, y, 30, trunk_height, tree_trunk, tree_trunk_light)
    # Add canopy
    draw_foliage(x + 15, y - 20, 50, jungle_mid_green)
    draw_foliage(x + 15, y - 40, 45, leaf_bright)

# Draw mid-ground foliage
for i in range(0, WIDTH, 80):
    x = i + random.randint(-20, 20)
    y = 250 + random.randint(-50, 50)
    color = random.choice([jungle_mid_green, leaf_bright, leaf_yellow])
    draw_foliage(x, y, 35, color)

# Draw some large foreground trees
foreground_trees = [
    (200, 300), (600, 280), (1100, 320), (1600, 290),
    (2100, 310), (2600, 295), (3100, 305), (3600, 285),
    (4100, 300), (4500, 295)
]

for tx, ty in foreground_trees:
    trunk_h = HEIGHT - ty
    draw_tree_trunk(tx, ty, 40, trunk_h, tree_trunk, tree_trunk_light)

    # Add palm fronds
    num_fronds = 8
    for f in range(num_fronds):
        angle = (360 / num_fronds) * f - 90
        frond_length = random.randint(80, 120)
        draw_palm_frond(tx + 20, ty, frond_length, angle, leaf_bright)

# Draw hanging vines
vine_positions = []
for i in range(30):
    x = random.randint(0, WIDTH)
    y = random.randint(50, 200)
    length = random.randint(100, 300)
    vine_positions.append((x, y, length))

for vx, vy, vl in vine_positions:
    draw_vine(vx, vy, vl)

# Draw foreground ferns and plants at ground level
for i in range(0, WIDTH, 60):
    x = i + random.randint(-15, 15)
    y = HEIGHT - 20

    # Draw fern leaves
    for angle in range(-60, 70, 30):
        leaf_length = random.randint(30, 50)
        end_x = x + int(leaf_length * np.cos(np.radians(angle)))
        end_y = y - int(leaf_length * np.sin(np.radians(angle)))

        # Draw leaf stem
        pygame.draw.line(surface, fern_green, (x, y), (end_x, end_y), 2)

        # Add leaflets
        for t in np.linspace(0, 1, 6):
            px = int(x + (end_x - x) * t)
            py = int(y + (end_y - y) * t)
            leaflet_size = 8
            pygame.draw.ellipse(surface, fern_green, (px - leaflet_size, py - 3, leaflet_size * 2, 6))

# Add some bright flowers for color
flower_colors = [(255, 100, 100), (255, 200, 50), (200, 100, 255), (255, 150, 200)]
for i in range(40):
    fx = random.randint(0, WIDTH)
    fy = random.randint(350, HEIGHT - 50)
    color = random.choice(flower_colors)
    pygame.draw.circle(surface, color, (fx, fy), 5)
    # Petals
    for angle in range(0, 360, 60):
        px = fx + int(8 * np.cos(np.radians(angle)))
        py = fy + int(8 * np.sin(np.radians(angle)))
        pygame.draw.circle(surface, color, (px, py), 4)

# Add atmospheric mist in foreground
mist_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for i in range(20):
    mx = random.randint(-100, WIDTH + 100)
    my = random.randint(HEIGHT // 2, HEIGHT)
    mist_width = random.randint(200, 400)
    mist_height = random.randint(40, 80)
    alpha = random.randint(10, 30)
    mist_color = (*mist[:3], alpha)
    pygame.draw.ellipse(mist_surface, mist_color, (mx, my, mist_width, mist_height))

surface.blit(mist_surface, (0, 0))

# Save the image
pygame.image.save(surface, "assets/images/amazon_jungle.png")
print("Amazon jungle background generated successfully!")

pygame.quit()
