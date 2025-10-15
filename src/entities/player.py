"""
Player entity module for Sancho Bros
Contains the Player sprite class and related functionality.
"""

import pygame
import math
from config import (
    YELLOW, PLAYER_SPEED, GRAVITY, TERMINAL_VELOCITY,
    JUMP_VELOCITY, JUMP_CUTOFF_VELOCITY, WINDOW_WIDTH,
    PLAYER_STARTING_LIVES, INVULNERABILITY_DURATION, BLINK_INTERVAL,
    KNOCKBACK_DISTANCE, KNOCKBACK_BOUNCE, POWERUP_DURATION, GOLD,
    LASER_COOLDOWN
)


class Player(pygame.sprite.Sprite):
    """Player character class for Sancho"""

    def __init__(self, x, y, audio_manager=None):
        """
        Initialize the player

        Args:
            x (int): Initial x position
            y (int): Initial y position
            audio_manager (AudioManager): Optional audio manager for sound effects
        """
        super().__init__()

        # Store audio manager reference (US-041)
        self.audio_manager = audio_manager
        print(f"Player initialized with audio_manager: {audio_manager}")

        # Player dimensions
        self.width = 40
        self.height = 60

        # Animation system (US-048)
        self.walk_frames = self._generate_walk_frames()  # 6 frames for walk cycle
        self.current_frame = 0  # Current animation frame index
        self.animation_timer = 0  # Timer for frame cycling
        self.animation_speed = 6  # Frames to display each animation frame (60 FPS / 6 = 10 FPS animation)
        self.is_walking = False  # True when player is moving

        # Create player surface (placeholder colored rectangle)
        self.image = self.walk_frames[0].copy()

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

    def _generate_walk_frames(self):
        """
        Generate 6 walking animation frames programmatically
        Creates a simple walking animation with leg movement

        Returns:
            list: List of 6 pygame.Surface objects representing walk cycle
        """
        frames = []

        for i in range(6):
            # Create a new surface for each frame
            frame = pygame.Surface((self.width, self.height))
            frame.fill(YELLOW)

            # Calculate leg positions based on frame number
            # Create a walking effect by varying leg positions
            leg_offset = math.sin(i * math.pi / 3) * 5  # Oscillate between -5 and 5 pixels

            # Draw simple legs (black rectangles) to show walking motion
            leg_width = 8
            leg_height = 15

            # Left leg
            left_leg_x = self.width // 2 - 10 + int(leg_offset)
            left_leg_y = self.height - leg_height
            pygame.draw.rect(frame, (0, 0, 0),
                           (left_leg_x, left_leg_y, leg_width, leg_height))

            # Right leg (opposite phase)
            right_leg_x = self.width // 2 + 2 - int(leg_offset)
            right_leg_y = self.height - leg_height
            pygame.draw.rect(frame, (0, 0, 0),
                           (right_leg_x, right_leg_y, leg_width, leg_height))

            # Draw body (slightly darker yellow rectangle)
            body_color = (230, 189, 0)
            body_rect = pygame.Rect(5, 10, self.width - 10, self.height - 25)
            pygame.draw.rect(frame, body_color, body_rect)

            frames.append(frame)

        return frames

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

        # Play death sound effect (US-045)
        if self.audio_manager:
            self.audio_manager.play_death()

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

        # Play laser shoot sound effect (US-043)
        if self.audio_manager:
            self.audio_manager.play_laser()

        return (laser_x, laser_y, self.facing_direction)

    def _update_appearance(self):
        """Update player visual appearance based on current state"""
        # Regenerate walk frames with current powered-up state
        self.walk_frames = self._generate_walk_frames()

        # Set current image based on animation state
        if self.is_walking:
            self.image = self.walk_frames[self.current_frame].copy()
        else:
            self.image = self.walk_frames[0].copy()

        # If powered up, add golden border/glow effect
        if self.is_powered_up:
            # Draw golden border around current image
            pygame.draw.rect(self.image, GOLD, self.image.get_rect(), 3)  # 3-pixel border

        # Update original image for blinking effect
        self.original_image = self.image.copy()

    def update(self, keys_pressed, platforms, level_width=WINDOW_WIDTH):
        """
        Update player state based on keyboard input, gravity, and collision
        Handles horizontal movement, gravity physics, jumping, platform collision, and level boundaries

        Args:
            keys_pressed (tuple): Result from pygame.key.get_pressed()
            platforms (pygame.sprite.Group): Group of platform sprites for collision detection
            level_width (int): Width of the current level (for boundary clamping with camera system)
        """
        # Handle horizontal movement and walking animation (US-048)
        # Check if player is moving this frame
        is_moving = False

        # Handle left movement (LEFT arrow or A key)
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
            self.facing_direction = -1  # Facing left
            is_moving = True

        # Handle right movement (RIGHT arrow or D key)
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.rect.x += PLAYER_SPEED
            self.facing_direction = 1  # Facing right
            is_moving = True

        # Update walking state (US-048)
        self.is_walking = is_moving

        # Keep player within level boundaries (horizontal) - US-038, US-039
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > level_width:
            self.rect.right = level_width

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
            # Play jump sound effect (US-041)
            if self.audio_manager:
                self.audio_manager.play_jump()

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

        # Update walking animation (US-048)
        if self.is_walking:
            # Increment animation timer
            self.animation_timer += 1

            # Advance to next frame when timer reaches animation speed
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)

            # Update image to current frame
            self.image = self.walk_frames[self.current_frame].copy()

            # Add powered-up border if applicable
            if self.is_powered_up:
                pygame.draw.rect(self.image, GOLD, self.image.get_rect(), 3)

            # Flip sprite horizontally based on facing direction (US-048)
            if self.facing_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            # Update original image for blinking effect
            self.original_image = self.image.copy()
        else:
            # Player is not moving - reset animation to idle (frame 0)
            self.current_frame = 0
            self.animation_timer = 0

            # Update image to idle frame
            self.image = self.walk_frames[0].copy()

            # Add powered-up border if applicable
            if self.is_powered_up:
                pygame.draw.rect(self.image, GOLD, self.image.get_rect(), 3)

            # Flip sprite horizontally based on facing direction (US-048)
            if self.facing_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            # Update original image for blinking effect
            self.original_image = self.image.copy()
