"""
Sancho Bros - Main Game Entry Point
A 2D platformer game inspired by Super Mario Bros with Colombian cultural themes.
"""

import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE, BLACK
from src.entities import Player, Platform


def main():
    """Main game function"""
    # Initialize pygame
    pygame.init()

    # Create game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # Create clock for FPS control
    clock = pygame.time.Clock()

    # Create player at initial spawn position
    player = Player(100, 400)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create platforms
    platforms = pygame.sprite.Group()

    # Ground platform (full width at bottom of screen)
    ground = Platform(0, 550, WINDOW_WIDTH, 50)
    platforms.add(ground)
    all_sprites.add(ground)

    # Floating platforms at various positions
    platform1 = Platform(200, 450, 150, 20)
    platforms.add(platform1)
    all_sprites.add(platform1)

    platform2 = Platform(400, 350, 120, 20)
    platforms.add(platform2)
    all_sprites.add(platform2)

    platform3 = Platform(550, 250, 180, 20)
    platforms.add(platform3)
    all_sprites.add(platform3)

    platform4 = Platform(100, 200, 100, 20)
    platforms.add(platform4)
    all_sprites.add(platform4)

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Get currently pressed keys for continuous input
        keys = pygame.key.get_pressed()

        # Update player with current key states and platform collision
        player.update(keys, platforms)

        # Fill screen with black background
        screen.fill(BLACK)

        # Draw all sprites
        all_sprites.draw(screen)

        # Update display
        pygame.display.flip()

        # Maintain consistent FPS
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
