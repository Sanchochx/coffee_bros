"""
Generate Medellin city background for Coffee Bros Level 1
Colombian cityscape with mountains, buildings, and metro
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Background dimensions
BG_WIDTH = 800
BG_HEIGHT = 600


def create_medellin_city_background():
    """Create a realistic Medellin cityscape background"""
    surface = pygame.Surface((BG_WIDTH, BG_HEIGHT))

    # Sky colors (Medellin perfect blue sky)
    sky_top = (100, 160, 230)
    sky_mid = (140, 190, 240)
    sky_bottom = (170, 210, 245)

    # Gradient sky (top to middle - sky ends at y=450)
    sky_end = 450
    for y in range(sky_end):
        if y < sky_end // 2:
            ratio = y / (sky_end // 2)
            r = int(sky_top[0] + (sky_mid[0] - sky_top[0]) * ratio)
            g = int(sky_top[1] + (sky_mid[1] - sky_top[1]) * ratio)
            b = int(sky_top[2] + (sky_mid[2] - sky_top[2]) * ratio)
        else:
            ratio = (y - sky_end // 2) / (sky_end // 2)
            r = int(sky_mid[0] + (sky_bottom[0] - sky_mid[0]) * ratio)
            g = int(sky_mid[1] + (sky_bottom[1] - sky_mid[1]) * ratio)
            b = int(sky_mid[2] + (sky_bottom[2] - sky_mid[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (BG_WIDTH, y))

    # Colombian Andes mountains in background (iconic Medellin mountains)
    mountain_green = (50, 120, 80)
    mountain_dark = (30, 80, 50)

    # Far mountains (lighter)
    far_mountain_points = [
        (0, 250), (150, 180), (300, 220), (450, 160), (600, 200), (800, 230)
    ]
    pygame.draw.polygon(surface, (70, 140, 100), far_mountain_points + [(800, BG_HEIGHT // 2), (0, BG_HEIGHT // 2)])

    # Closer mountains (darker green)
    near_mountain_points = [
        (0, 300), (100, 240), (250, 280), (400, 220), (550, 270), (700, 250), (800, 290)
    ]
    pygame.draw.polygon(surface, mountain_green, near_mountain_points + [(800, BG_HEIGHT // 2), (0, BG_HEIGHT // 2)])

    # Add mountain shadows/details
    for i in range(1, len(near_mountain_points) - 1):
        pygame.draw.line(surface, mountain_dark, near_mountain_points[i],
                        (near_mountain_points[i][0], near_mountain_points[i][1] + 20), 2)

    # Medellin buildings (colorful, modern skyline)
    building_colors = [
        (220, 100, 80),   # Red/orange building
        (200, 200, 220),  # White/gray building
        (180, 140, 100),  # Brown building
        (150, 180, 200),  # Blue building
        (240, 220, 200),  # Cream building
    ]

    # Draw buildings at different positions
    buildings = [
        (50, 320, 80, 120, building_colors[0]),
        (150, 340, 70, 100, building_colors[1]),
        (240, 310, 90, 130, building_colors[2]),
        (350, 330, 75, 110, building_colors[3]),
        (450, 320, 85, 120, building_colors[4]),
        (560, 340, 70, 100, building_colors[0]),
        (650, 325, 80, 115, building_colors[1]),
    ]

    for x, y, w, h, color in buildings:
        # Building body
        pygame.draw.rect(surface, color, (x, y, w, h))
        # Building outline
        pygame.draw.rect(surface, (0, 0, 0), (x, y, w, h), 2)
        # Windows
        window_color = (100, 150, 200)
        for row in range(3):
            for col in range(3):
                wx = x + 10 + col * 20
                wy = y + 15 + row * 25
                if wx + 10 < x + w and wy + 15 < y + h:
                    pygame.draw.rect(surface, window_color, (wx, wy, 10, 15))

    # Metro cable car (iconic Medellin Metrocable)
    cable_color = (80, 80, 80)
    car_color = (200, 50, 50)

    # Cable lines
    pygame.draw.line(surface, cable_color, (0, 280), (800, 240), 3)
    pygame.draw.line(surface, cable_color, (0, 285), (800, 245), 2)

    # Cable car
    car_x, car_y = 300, 260
    pygame.draw.rect(surface, car_color, (car_x, car_y, 40, 30))
    pygame.draw.rect(surface, (150, 150, 180), (car_x + 5, car_y + 5, 12, 12))  # Window
    pygame.draw.rect(surface, (150, 150, 180), (car_x + 23, car_y + 5, 12, 12))  # Window
    pygame.draw.line(surface, cable_color, (car_x + 20, car_y - 5), (car_x + 20, car_y), 3)  # Cable connection

    # Trees (tropical vegetation)
    tree_green = (40, 150, 60)
    tree_trunk = (100, 70, 40)

    tree_positions = [(100, 420), (300, 410), (500, 425), (700, 415)]
    for tx, ty in tree_positions:
        # Trunk
        pygame.draw.rect(surface, tree_trunk, (tx, ty, 8, 20))
        # Foliage
        pygame.draw.circle(surface, tree_green, (tx + 4, ty - 5), 15)
        pygame.draw.circle(surface, (60, 170, 80), (tx + 4, ty - 5), 12)  # Highlight

    # Colombian flag somewhere (small detail)
    flag_x, flag_y = 600, 300
    flag_w, flag_h = 30, 20
    # Yellow (50%)
    pygame.draw.rect(surface, (255, 209, 0), (flag_x, flag_y, flag_w, flag_h // 2))
    # Blue (25%)
    pygame.draw.rect(surface, (0, 56, 168), (flag_x, flag_y + flag_h // 2, flag_w, flag_h // 4))
    # Red (25%)
    pygame.draw.rect(surface, (206, 17, 38), (flag_x, flag_y + 3 * flag_h // 4, flag_w, flag_h // 4))

    # CITY STREET AT BOTTOM (replaces aquamarine section)
    street_y = 450
    street_height = BG_HEIGHT - street_y

    # Asphalt street (dark gray)
    asphalt_gray = (60, 60, 70)
    pygame.draw.rect(surface, asphalt_gray, (0, street_y, BG_WIDTH, street_height))

    # Street markings (yellow dashed lines)
    yellow_line = (255, 220, 0)
    dash_width = 30
    dash_gap = 20
    center_line_y = street_y + street_height // 2
    for x in range(0, BG_WIDTH, dash_width + dash_gap):
        pygame.draw.rect(surface, yellow_line, (x, center_line_y - 2, dash_width, 4))

    # Sidewalk (lighter gray at bottom)
    sidewalk_gray = (120, 120, 130)
    sidewalk_height = 20
    pygame.draw.rect(surface, sidewalk_gray, (0, BG_HEIGHT - sidewalk_height, BG_WIDTH, sidewalk_height))

    # Traffic lights at various positions
    traffic_light_positions = [(150, street_y - 40), (450, street_y - 40), (700, street_y - 40)]

    for tl_x, tl_y in traffic_light_positions:
        # Traffic light pole (black)
        pole_width = 4
        pole_height = 40
        pygame.draw.rect(surface, (40, 40, 40), (tl_x, tl_y, pole_width, pole_height))

        # Traffic light housing (dark gray rectangle)
        light_box_width = 16
        light_box_height = 35
        light_box_x = tl_x - (light_box_width - pole_width) // 2
        light_box_y = tl_y - light_box_height
        pygame.draw.rect(surface, (50, 50, 55), (light_box_x, light_box_y, light_box_width, light_box_height))
        pygame.draw.rect(surface, (30, 30, 35), (light_box_x, light_box_y, light_box_width, light_box_height), 2)

        # Three lights (red, yellow, green) - only green is lit
        light_radius = 5
        # Red light (off)
        red_y = light_box_y + 6
        pygame.draw.circle(surface, (80, 30, 30), (tl_x + 2, red_y), light_radius)
        # Yellow light (off)
        yellow_y = light_box_y + 17
        pygame.draw.circle(surface, (80, 80, 30), (tl_x + 2, yellow_y), light_radius)
        # Green light (ON - bright)
        green_y = light_box_y + 28
        pygame.draw.circle(surface, (50, 200, 50), (tl_x + 2, green_y), light_radius)
        pygame.draw.circle(surface, (150, 255, 150), (tl_x + 2, green_y), light_radius - 2)  # Bright center

    # Simple cars on the street
    car_colors = [(200, 50, 50), (50, 100, 200), (255, 200, 50)]
    car_positions = [(80, street_y + 35), (320, street_y + 75), (600, street_y + 40)]

    for i, (car_x, car_y) in enumerate(car_positions):
        car_color = car_colors[i % len(car_colors)]
        # Car body
        car_width = 50
        car_height = 25
        pygame.draw.rect(surface, car_color, (car_x, car_y, car_width, car_height), border_radius=5)
        # Car roof
        roof_width = 30
        roof_height = 15
        roof_x = car_x + 10
        roof_y = car_y - 12
        pygame.draw.rect(surface, car_color, (roof_x, roof_y, roof_width, roof_height), border_radius=3)
        # Windows (light blue)
        pygame.draw.rect(surface, (150, 200, 230), (roof_x + 3, roof_y + 2, 10, 10))
        pygame.draw.rect(surface, (150, 200, 230), (roof_x + 17, roof_y + 2, 10, 10))
        # Wheels (black circles)
        wheel_radius = 6
        pygame.draw.circle(surface, (30, 30, 30), (car_x + 12, car_y + car_height), wheel_radius)
        pygame.draw.circle(surface, (30, 30, 30), (car_x + car_width - 12, car_y + car_height), wheel_radius)
        # Wheel hubs (gray)
        pygame.draw.circle(surface, (100, 100, 100), (car_x + 12, car_y + car_height), 3)
        pygame.draw.circle(surface, (100, 100, 100), (car_x + car_width - 12, car_y + car_height), 3)

    return surface


def main():
    """Generate and save Medellin city background"""
    bg_dir = "assets/images"
    os.makedirs(bg_dir, exist_ok=True)

    print("Generating Medellin City Background...")
    print("Features: Mountains, buildings, metro cable car, tropical vegetation")

    medellin_bg = create_medellin_city_background()
    output_file = os.path.join(bg_dir, "medellin_city.png")
    pygame.image.save(medellin_bg, output_file)

    print(f"Created medellin_city.png ({BG_WIDTH}x{BG_HEIGHT})")
    print("Medellin - City of Eternal Spring is ready!")


if __name__ == "__main__":
    main()
