"""
Player entity module for Sancho Bros
Contains the Player sprite class and related functionality.
"""

import pygame
from config import (
    YELLOW, PLAYER_SPEED, GRAVITY, TERMINAL_VELOCITY,
    JUMP_VELOCITY, JUMP_CUTOFF_VELOCITY, WINDOW_WIDTH
)


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

    def update(self, keys_pressed, platforms):
        """
        Update player state based on keyboard input, gravity, and collision
        Handles horizontal movement, gravity physics, jumping, platform collision, and screen boundaries

        Args:
            keys_pressed (tuple): Result from pygame.key.get_pressed()
            platforms (pygame.sprite.Group): Group of platform sprites for collision detection
        """
        # Handle horizontal movement
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

        # Check for horizontal collision with platforms (side collision)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Moving right - hit left side of platform
                if self.rect.right > platform.rect.left and self.rect.centerx < platform.rect.centerx:
                    self.rect.right = platform.rect.left
                # Moving left - hit right side of platform
                elif self.rect.left < platform.rect.right and self.rect.centerx > platform.rect.centerx:
                    self.rect.left = platform.rect.right

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

        # Assume player is not grounded initially (will be set to True if standing on platform)
        self.is_grounded = False

        # Check for vertical collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Falling down - landing on top of platform
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_grounded = True
                # Moving upward - hitting platform from below
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
