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
GREEN = (34, 139, 34)  # Forest green for platforms

# Player constants
PLAYER_SPEED = 5  # pixels per frame
GRAVITY = 0.8  # pixels per frame² - acceleration due to gravity
TERMINAL_VELOCITY = 20  # pixels per frame - maximum fall speed
JUMP_VELOCITY = -15  # pixels per frame - initial upward velocity when jumping
JUMP_CUTOFF_VELOCITY = -3  # velocity threshold for variable jump height


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

        # Velocity for gravity physics
        self.velocity_y = 0  # vertical velocity in pixels per frame

        # Ground state tracking
        self.is_grounded = False  # True when player is standing on ground/platform

    def update(self, keys_pressed):
        """
        Update player state based on keyboard input and gravity
        Handles horizontal movement, gravity physics, jumping, and screen boundaries

        Args:
            keys_pressed (tuple): Result from pygame.key.get_pressed()
        """
        # Handle left movement (LEFT arrow or A key)
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED

        # Handle right movement (RIGHT arrow or D key)
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.rect.x += PLAYER_SPEED

        # Keep player within screen boundaries (horizontal)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH

        # Handle jumping (UP arrow, W key, or SPACE)
        if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w] or
            keys_pressed[pygame.K_SPACE]) and self.is_grounded:
            self.velocity_y = JUMP_VELOCITY
            self.is_grounded = False

        # Variable jump height: cut jump short if button released early
        # Only reduce velocity if moving upward and above cutoff threshold
        if (not keys_pressed[pygame.K_UP] and not keys_pressed[pygame.K_w] and
            not keys_pressed[pygame.K_SPACE]):
            if self.velocity_y < JUMP_CUTOFF_VELOCITY:
                self.velocity_y = JUMP_CUTOFF_VELOCITY

        # Apply gravity physics
        self.velocity_y += GRAVITY  # Increase downward velocity

        # Cap at terminal velocity
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY

        # Update vertical position
        self.rect.y += self.velocity_y

        # Simple ground collision (bottom of screen for now, until platforms exist)
        # Ground level at y=500 (allowing for player height of 60 pixels)
        ground_level = 500
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0
            self.is_grounded = True


class Platform(pygame.sprite.Sprite):
    """Platform class for ground and floating platforms"""

    def __init__(self, x, y, width, height):
        """
        Initialize a platform

        Args:
            x (int): Platform x position (left edge)
            y (int): Platform y position (top edge)
            width (int): Platform width in pixels
            height (int): Platform height in pixels
        """
        super().__init__()

        # Create platform surface
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)

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

        # Update player with current key states
        player.update(keys)

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
