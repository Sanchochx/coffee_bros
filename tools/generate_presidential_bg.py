"""
Generate presidential office background for boss fight level
Colombian Casa de Nariño (Presidential House) interior with flags
"""

import pygame
import os
import math

# Initialize pygame
pygame.init()

# Background dimensions
BG_WIDTH = 800
BG_HEIGHT = 600

def create_presidential_office_background():
    """Create a Colombian presidential office background - Casa de Nariño style"""
    surface = pygame.Surface((BG_WIDTH, BG_HEIGHT))

    # Colombian flag colors
    flag_yellow = (255, 209, 0)
    flag_blue = (0, 56, 168)
    flag_red = (206, 17, 38)

    # Office colors
    wall_color = (160, 140, 120)  # Elegant beige wall
    dark_wood = (50, 35, 20)
    gold = (220, 180, 70)

    # BACKGROUND: Fill with wall color
    surface.fill(wall_color)

    # FLOOR/CARPET - Rich red carpet with Colombian flag border
    carpet_y = 420
    # Main carpet area
    pygame.draw.rect(surface, (120, 20, 20), (0, carpet_y, BG_WIDTH, BG_HEIGHT - carpet_y))
    # Colombian flag stripe at top of carpet
    stripe_h = 25
    pygame.draw.rect(surface, flag_yellow, (0, carpet_y, BG_WIDTH, stripe_h // 2))
    pygame.draw.rect(surface, flag_blue, (0, carpet_y + stripe_h // 2, BG_WIDTH, stripe_h // 4))
    pygame.draw.rect(surface, flag_red, (0, carpet_y + 3 * stripe_h // 4, BG_WIDTH, stripe_h // 4))

    # Gold carpet patterns
    for x in range(100, BG_WIDTH, 150):
        y = carpet_y + 60
        # Diamond pattern
        pygame.draw.polygon(surface, gold, [
            (x, y - 25), (x + 20, y), (x, y + 25), (x - 20, y)
        ], 3)

    # WALL PANELING - Wood panels with gold trim
    panel_w = 120
    for x in range(0, BG_WIDTH, panel_w):
        pygame.draw.rect(surface, dark_wood, (x, 0, 6, carpet_y), 0)
        pygame.draw.rect(surface, gold, (x + 1, 0, 2, carpet_y), 0)

    # Horizontal trim
    pygame.draw.rect(surface, dark_wood, (0, 180, BG_WIDTH, 15))
    pygame.draw.rect(surface, gold, (0, 185, BG_WIDTH, 5))

    # COLOMBIAN FLAG #1 - LEFT SIDE (LARGE)
    flag1_x, flag1_y = 50, 50
    flag1_w, flag1_h = 180, 120
    # Yellow (50%)
    pygame.draw.rect(surface, flag_yellow, (flag1_x, flag1_y, flag1_w, flag1_h // 2))
    # Blue (25%)
    pygame.draw.rect(surface, flag_blue, (flag1_x, flag1_y + flag1_h // 2, flag1_w, flag1_h // 4))
    # Red (25%)
    pygame.draw.rect(surface, flag_red, (flag1_x, flag1_y + 3 * flag1_h // 4, flag1_w, flag1_h // 4))
    # Gold ornate frame
    pygame.draw.rect(surface, gold, (flag1_x - 5, flag1_y - 5, flag1_w + 10, flag1_h + 10), 5)
    pygame.draw.rect(surface, dark_wood, (flag1_x - 2, flag1_y - 2, flag1_w + 4, flag1_h + 4), 2)

    # COLOMBIAN FLAG #2 - CENTER (LARGEST, BEHIND DESK)
    flag2_x, flag2_y = 310, 30
    flag2_w, flag2_h = 180, 120
    # Yellow (50%)
    pygame.draw.rect(surface, flag_yellow, (flag2_x, flag2_y, flag2_w, flag2_h // 2))
    # Blue (25%)
    pygame.draw.rect(surface, flag_blue, (flag2_x, flag2_y + flag2_h // 2, flag2_w, flag2_h // 4))
    # Red (25%)
    pygame.draw.rect(surface, flag_red, (flag2_x, flag2_y + 3 * flag2_h // 4, flag2_w, flag2_h // 4))
    # Gold ornate frame
    pygame.draw.rect(surface, gold, (flag2_x - 5, flag2_y - 5, flag2_w + 10, flag2_h + 10), 5)
    pygame.draw.rect(surface, dark_wood, (flag2_x - 2, flag2_y - 2, flag2_w + 4, flag2_h + 4), 2)

    # Colombian coat of arms above center flag
    shield_x, shield_y = 385, 5
    pygame.draw.ellipse(surface, gold, (shield_x, shield_y, 30, 25))
    pygame.draw.ellipse(surface, flag_yellow, (shield_x + 3, shield_y + 3, 24, 19))

    # COLOMBIAN FLAG #3 - RIGHT SIDE (LARGE)
    flag3_x, flag3_y = 570, 50
    flag3_w, flag3_h = 180, 120
    # Yellow (50%)
    pygame.draw.rect(surface, flag_yellow, (flag3_x, flag3_y, flag3_w, flag3_h // 2))
    # Blue (25%)
    pygame.draw.rect(surface, flag_blue, (flag3_x, flag3_y + flag3_h // 2, flag3_w, flag3_h // 4))
    # Red (25%)
    pygame.draw.rect(surface, flag_red, (flag3_x, flag3_y + 3 * flag3_h // 4, flag3_w, flag3_h // 4))
    # Gold ornate frame
    pygame.draw.rect(surface, gold, (flag3_x - 5, flag3_y - 5, flag3_w + 10, flag3_h + 10), 5)
    pygame.draw.rect(surface, dark_wood, (flag3_x - 2, flag3_y - 2, flag3_w + 4, flag3_h + 4), 2)

    # COLOMBIAN FLAG #4 - LEFT LOWER
    flag4_x, flag4_y = 60, 220
    flag4_w, flag4_h = 120, 80
    pygame.draw.rect(surface, flag_yellow, (flag4_x, flag4_y, flag4_w, flag4_h // 2))
    pygame.draw.rect(surface, flag_blue, (flag4_x, flag4_y + flag4_h // 2, flag4_w, flag4_h // 4))
    pygame.draw.rect(surface, flag_red, (flag4_x, flag4_y + 3 * flag4_h // 4, flag4_w, flag4_h // 4))
    pygame.draw.rect(surface, gold, (flag4_x - 3, flag4_y - 3, flag4_w + 6, flag4_h + 6), 3)

    # COLOMBIAN FLAG #5 - RIGHT LOWER
    flag5_x, flag5_y = 620, 220
    flag5_w, flag5_h = 120, 80
    pygame.draw.rect(surface, flag_yellow, (flag5_x, flag5_y, flag5_w, flag5_h // 2))
    pygame.draw.rect(surface, flag_blue, (flag5_x, flag5_y + flag5_h // 2, flag5_w, flag5_h // 4))
    pygame.draw.rect(surface, flag_red, (flag5_x, flag5_y + 3 * flag5_h // 4, flag5_w, flag5_h // 4))
    pygame.draw.rect(surface, gold, (flag5_x - 3, flag5_y - 3, flag5_w + 6, flag5_h + 6), 3)

    # PRESIDENTIAL DESK (ornate with gold)
    desk_x, desk_y = 250, 320
    desk_w, desk_h = 300, 100
    pygame.draw.rect(surface, dark_wood, (desk_x, desk_y, desk_w, desk_h))
    pygame.draw.rect(surface, gold, (desk_x, desk_y, desk_w, 6))  # Top trim
    pygame.draw.rect(surface, gold, (desk_x, desk_y, 6, desk_h))  # Left trim
    pygame.draw.rect(surface, gold, (desk_x + desk_w - 6, desk_y, 6, desk_h))  # Right trim

    # Desk drawers with gold handles
    drawer_y = desk_y + 25
    for i in range(4):
        dx = desk_x + 20 + i * 65
        pygame.draw.rect(surface, (35, 25, 15), (dx, drawer_y, 50, 35), 2)
        pygame.draw.circle(surface, gold, (dx + 25, drawer_y + 17), 4)

    # ORNATE CHANDELIER
    chandelier_x, chandelier_y = BG_WIDTH // 2, 30
    pygame.draw.circle(surface, (255, 245, 210), (chandelier_x, chandelier_y), 25)
    pygame.draw.circle(surface, gold, (chandelier_x, chandelier_y), 25, 4)
    # Chandelier crystals
    for angle in range(0, 360, 60):
        cx = chandelier_x + int(18 * math.cos(math.radians(angle)))
        cy = chandelier_y + int(18 * math.sin(math.radians(angle)))
        pygame.draw.circle(surface, gold, (cx, cy), 4)
        pygame.draw.circle(surface, (255, 255, 220), (cx, cy), 2)

    # WINDOWS with golden curtains
    # Left window
    win_x, win_y = 15, 200
    pygame.draw.rect(surface, (200, 220, 255), (win_x, win_y, 35, 120))
    pygame.draw.rect(surface, dark_wood, (win_x, win_y, 35, 120), 4)
    pygame.draw.line(surface, dark_wood, (win_x + 17, win_y), (win_x + 17, win_y + 120), 3)
    # Curtains
    pygame.draw.polygon(surface, gold, [(win_x - 5, win_y - 10), (win_x + 5, win_y), (win_x + 5, win_y + 130), (win_x - 5, win_y + 120)])
    pygame.draw.polygon(surface, gold, [(win_x + 55, win_y - 10), (win_x + 45, win_y), (win_x + 45, win_y + 130), (win_x + 55, win_y + 120)])

    # Right window
    win2_x = BG_WIDTH - 50
    pygame.draw.rect(surface, (200, 220, 255), (win2_x, win_y, 35, 120))
    pygame.draw.rect(surface, dark_wood, (win2_x, win_y, 35, 120), 4)
    pygame.draw.line(surface, dark_wood, (win2_x + 17, win_y), (win2_x + 17, win_y + 120), 3)
    # Curtains
    pygame.draw.polygon(surface, gold, [(win2_x - 5, win_y - 10), (win2_x + 5, win_y), (win2_x + 5, win_y + 130), (win2_x - 5, win_y + 120)])
    pygame.draw.polygon(surface, gold, [(win2_x + 55, win_y - 10), (win2_x + 45, win_y), (win2_x + 45, win_y + 130), (win2_x + 55, win_y + 120)])

    # PORTRAIT FRAMES (ornate gold frames)
    # Left portrait
    pygame.draw.rect(surface, dark_wood, (240, 200, 70, 90))
    pygame.draw.rect(surface, gold, (238, 198, 74, 94), 4)
    # Right portrait
    pygame.draw.rect(surface, dark_wood, (490, 200, 70, 90))
    pygame.draw.rect(surface, gold, (488, 198, 74, 94), 4)

    return surface


def create_presidential_tileset():
    """Create presidential office floor tiles (brown wood matching background)"""
    tile_size = 50

    # Brown wood colors matching the background
    tile = pygame.Surface((tile_size, tile_size))
    wood_brown = (80, 60, 40)  # Dark rich wood
    wood_light = (100, 75, 50)  # Lighter wood highlight
    wood_dark = (60, 45, 30)  # Darker wood shadow
    gold = (220, 180, 70)

    tile.fill(wood_brown)

    # Wood grain texture (horizontal lines)
    for i in range(5):
        y = 10 + i * 8
        pygame.draw.line(tile, wood_dark, (0, y), (tile_size, y), 1)
        pygame.draw.line(tile, wood_light, (0, y + 2), (tile_size, y + 2), 1)

    # Wood knots/patterns
    pygame.draw.circle(tile, wood_dark, (15, 15), 3)
    pygame.draw.circle(tile, wood_dark, (38, 32), 2)

    # Gold trim border to match presidential theme
    pygame.draw.rect(tile, gold, (0, 0, tile_size, tile_size), 2)
    pygame.draw.rect(tile, wood_dark, (1, 1, tile_size - 2, tile_size - 2), 1)

    return tile


def main():
    """Generate and save presidential office graphics"""
    # Create output directories
    img_dir = "assets/images"
    tile_dir = "assets/images/tiles"
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(tile_dir, exist_ok=True)

    print("Generating Presidential Office graphics...")

    # Create presidential office background
    office_bg = create_presidential_office_background()
    pygame.image.save(office_bg, os.path.join(img_dir, "presidential_office.png"))
    print(f"Created presidential_office.png ({BG_WIDTH}x{BG_HEIGHT})")

    # Create marble tiles
    marble_tile = create_presidential_tileset()
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile.png"))
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile_left.png"))
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile_middle.png"))
    pygame.image.save(marble_tile, os.path.join(tile_dir, "presidential_tile_right.png"))
    print(f"Created presidential_tile variants (50x50)")

    print(f"\nPresidential office graphics saved!")
    print("Colombian Presidential Office with 5 FLAGS ready!")


if __name__ == "__main__":
    main()
