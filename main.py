"""
Sancho Bros - Main Game Entry Point
A 2D platformer game inspired by Super Mario Bros with Colombian cultural themes.
"""

import pygame
import sys

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Sancho Bros"

# Color constants
BLACK = (0, 0, 0)
YELLOW = (255, 209, 0)  # Colombian yellow for Sancho


class Player(pygame.sprite.Sprite):
    """Player character class for Sancho"""

    def __init__(self, x, y):
        """
        Initialize the player

        Args:
            x (int): Initial x position
            y (int): Initial y position
        """
        super().__init__()

        # Player dimensions
        self.width = 40
        self.height = 60

        # Create player surface (placeholder colored rectangle)
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW)

        # Get rect for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
