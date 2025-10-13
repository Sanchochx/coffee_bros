"""
Polocho enemy entity for Sancho Bros game.
"""
import pygame
from config import GRAVITY, TERMINAL_VELOCITY, RED, ENEMY_SPEED


class Polocho(pygame.sprite.Sprite):
    """Enemy sprite class - Polocho enemies patrol and can be stomped."""

    def __init__(self, x, y, patrol_distance=150):
        """
        Initialize Polocho enemy.

        Args:
            x: Initial x position
            y: Initial y position
            patrol_distance: Distance in pixels the enemy patrols (half on each side)
        """
        super().__init__()

        # Enemy appearance - 40x40 pixels, red colored
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Physics properties
        self.velocity_y = 0
        self.is_grounded = False

        # Patrol movement properties
        self.patrol_start = x - patrol_distance
        self.patrol_end = x + patrol_distance
        self.direction = 1  # 1 for right, -1 for left
        self.speed = ENEMY_SPEED

        # Squashed state for stomp mechanic
        self.is_squashed = False
        self.squash_timer = 0  # Frames remaining in squashed state

    def squash(self):
        """Mark enemy as squashed and start squash timer."""
        if not self.is_squashed:
            self.is_squashed = True
            self.squash_timer = 15  # Show squashed state for 15 frames (~0.25 seconds)
            # Change appearance to show squashed state (flattened)
            self.image = pygame.Surface((self.width, self.height // 3))  # Flatten to 1/3 height
            self.image.fill(RED)
            old_bottom = self.rect.bottom
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom  # Keep bottom position same
            self.rect.centerx = self.rect.centerx  # Keep horizontal center

    def update(self, platforms):
        """
        Update enemy physics, patrol movement, and collision.

        Args:
            platforms: Sprite group containing platform objects
        """
        # If squashed, count down timer and kill when done
        if self.is_squashed:
            self.squash_timer -= 1
            if self.squash_timer <= 0:
                self.kill()  # Remove from all sprite groups
            return  # Don't process any other movement when squashed

        # Horizontal patrol movement
        self.rect.x += self.speed * self.direction

        # Check patrol boundaries and reverse direction if needed
        if self.rect.left <= self.patrol_start:
            self.rect.left = self.patrol_start
            self.direction = 1  # Turn right
        elif self.rect.right >= self.patrol_end:
            self.rect.right = self.patrol_end
            self.direction = -1  # Turn left

        # Check for platform edges (don't walk off platforms)
        if self.is_grounded:
            # Check if there's no ground ahead by looking for platform underneath future position
            future_x = self.rect.x + (self.speed * self.direction * 5)  # Look ahead
            future_rect = pygame.Rect(future_x, self.rect.bottom, self.width, 1)

            # Check if any platform is under the future position
            has_ground_ahead = False
            for platform in platforms:
                if future_rect.colliderect(platform.rect):
                    has_ground_ahead = True
                    break

            # If no ground ahead, turn around
            if not has_ground_ahead:
                self.direction *= -1

        # Check for horizontal wall collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Check if we hit a vertical wall (side collision)
                if self.direction > 0 and self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                    # Hit wall on right side - turn left
                    self.rect.right = platform.rect.left
                    self.direction = -1
                elif self.direction < 0 and self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                    # Hit wall on left side - turn right
                    self.rect.left = platform.rect.right
                    self.direction = 1

        # Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > TERMINAL_VELOCITY:
            self.velocity_y = TERMINAL_VELOCITY

        # Update vertical position
        self.rect.y += self.velocity_y

        # Check for platform collisions (vertical)
        self.is_grounded = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Landing on top of platform
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_grounded = True
                # Hitting platform from below
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.top:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
