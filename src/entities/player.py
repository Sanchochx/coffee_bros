"""
Player entity module for Sancho Bros
Contains the Player sprite class and related functionality.
"""

import pygame
from config import (
    YELLOW, PLAYER_SPEED, GRAVITY, TERMINAL_VELOCITY,
    JUMP_VELOCITY, JUMP_CUTOFF_VELOCITY, WINDOW_WIDTH,
    PLAYER_STARTING_LIVES, INVULNERABILITY_DURATION, BLINK_INTERVAL,
    KNOCKBACK_DISTANCE, KNOCKBACK_BOUNCE, POWERUP_DURATION, GOLD,
    LASER_COOLDOWN
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

        # Damage and invulnerability system
        self.lives = PLAYER_STARTING_LIVES  # Starting lives (US-013 will use this)
        self.is_invulnerable = False  # True when player is invulnerable after taking damage
        self.invulnerability_timer = 0  # Frames remaining of invulnerability
        self.blink_timer = 0  # Timer for blinking effect during invulnerability
        self.visible = True  # Used for blinking effect

        # Store original image for blinking effect
        self.original_image = self.image.copy()

        # Powered-up state (US-017)
        self.is_powered_up = False  # True when player has collected a power-up
        self.powerup_timer = 0  # Frames remaining of powered-up state

        # Shooting system (US-019)
        self.facing_direction = 1  # 1 = right, -1 = left
        self.shoot_cooldown = 0  # Frames until can shoot again

    def take_damage(self, knockback_direction=0):
        """
        Handle player taking damage from an enemy

        Args:
            knockback_direction (int): Direction of knockback (-1 for left, 1 for right, 0 for none)
        """
        if self.is_invulnerable:
            return  # Already invulnerable, no damage

        # Lose one life
        self.lives -= 1

        # Activate invulnerability (1 second = 60 frames at 60 FPS)
        self.is_invulnerable = True
        self.invulnerability_timer = INVULNERABILITY_DURATION

        # Apply knockback
        if knockback_direction != 0:
            self.rect.x += knockback_direction * KNOCKBACK_DISTANCE  # Push player away
            self.velocity_y = KNOCKBACK_BOUNCE  # Small upward bounce

        # Placeholder for damage sound effect (will be implemented in Epic 7)
        # TODO: Play damage sound effect

    def collect_powerup(self):
        """
        Handle player collecting a power-up (Golden Arepa)
        Enters powered-up state for POWERUP_DURATION frames
        """
        # Enter powered-up state
        self.is_powered_up = True
        self.powerup_timer = POWERUP_DURATION

        # Visual change: add golden glow/border to show powered-up state (US-018)
        self._update_appearance()

        # Placeholder for powerup collection sound effect (will be implemented in Epic 7)
        # TODO (US-044): Play powerup collection sound effect

    def can_shoot(self):
        """
        Check if player can shoot a laser
        Must be powered up and cooldown must be 0

        Returns:
            bool: True if player can shoot, False otherwise
        """
        return self.is_powered_up and self.shoot_cooldown == 0

    def shoot(self):
        """
        Attempt to shoot a laser
        Returns laser spawn position and direction if successful

        Returns:
            tuple or None: (x, y, direction) if shot successful, None otherwise
        """
        if not self.can_shoot():
            return None

        # Start cooldown
        self.shoot_cooldown = LASER_COOLDOWN

        # Calculate laser spawn position (from center of player)
        laser_x = self.rect.centerx
        laser_y = self.rect.centery

        # Placeholder for shooting sound effect (will be implemented in Epic 7)
        # TODO (US-043): Play laser shoot sound effect

        return (laser_x, laser_y, self.facing_direction)

    def _update_appearance(self):
        """Update player visual appearance based on current state"""
        # Create base image
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(YELLOW)

        # If powered up, add golden border/glow effect
        if self.is_powered_up:
            # Draw golden border around player
            pygame.draw.rect(self.image, GOLD, self.image.get_rect(), 3)  # 3-pixel border

        # Update original image for blinking effect
        self.original_image = self.image.copy()

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
            self.facing_direction = -1  # Facing left

        # Handle right movement (RIGHT arrow or D key)
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            self.facing_direction = 1  # Facing right

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

        # Handle invulnerability timer and blinking
        if self.is_invulnerable:
            self.invulnerability_timer -= 1

            # Blink effect: toggle visibility every BLINK_INTERVAL frames
            self.blink_timer += 1
            if self.blink_timer >= BLINK_INTERVAL:
                self.visible = not self.visible
                self.blink_timer = 0

                # Update sprite visibility
                if self.visible:
                    self.image = self.original_image.copy()
                else:
                    # Create transparent image for "invisible" blink
                    self.image = pygame.Surface((self.width, self.height))
                    self.image.set_alpha(100)  # Semi-transparent
                    self.image.fill(YELLOW)

            # End invulnerability when timer expires
            if self.invulnerability_timer <= 0:
                self.is_invulnerable = False
                self.visible = True
                self.image = self.original_image.copy()

        # Handle powered-up timer (US-017, US-018)
        if self.is_powered_up:
            self.powerup_timer -= 1

            # Visual warning when powerup about to expire (last 3 seconds = 180 frames)
            # Flash the golden border on and off every 10 frames when timer < 180
            if self.powerup_timer < 180 and self.powerup_timer % 20 < 10:
                # Flash effect: temporarily show normal appearance (no border)
                temp_powered_up = self.is_powered_up
                self.is_powered_up = False
                self._update_appearance()
                self.is_powered_up = temp_powered_up
            elif self.powerup_timer < 180:
                # Show powered-up appearance (with border)
                self._update_appearance()

            # End powered-up state when timer expires
            if self.powerup_timer <= 0:
                self.is_powered_up = False
                self._update_appearance()  # Remove golden border visual

        # Handle shooting cooldown (US-019)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
