"""
Player entity module for Coffee Bros
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
    """Player character class for Coffee"""

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

        # Animation system (US-048, US-049, US-050, US-051)
        self.walk_frames = self._generate_walk_frames()  # 6 frames for walk cycle
        self.jump_frame = self._generate_jump_frame()  # Frame for ascending (US-049)
        self.fall_frame = self._generate_fall_frame()  # Frame for descending (US-049)
        self.idle_frames = self._generate_idle_frames()  # 4 frames for idle animation (US-050)
        self.shoot_frames = self._generate_shoot_frames()  # 4 frames for shooting animation (US-051)
        self.current_frame = 0  # Current animation frame index
        self.animation_timer = 0  # Timer for frame cycling
        self.animation_speed = 6  # Frames to display each animation frame (60 FPS / 6 = 10 FPS animation)
        self.idle_animation_speed = 12  # Slower cycle for idle (60 FPS / 12 = 5 FPS animation)
        self.is_walking = False  # True when player is moving
        # Shooting animation state (US-051)
        self.is_shooting = False  # True when playing shooting animation
        self.shoot_animation_timer = 0  # Timer for shooting animation duration (frames)

        # Create player surface (start with idle animation frame 0)
        self.image = self.idle_frames[0].copy()

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

        # Super Saiyan aura effect (DBZ-style)
        self.aura_frames = []  # List of aura animation frames
        self.aura_frame_index = 0  # Current aura frame
        self.aura_animation_timer = 0  # Timer for aura animation
        self.aura_animation_speed = 3  # Change aura frame every 3 game frames
        self._generate_aura_frames()  # Generate aura animation

    def _generate_walk_frames(self):
        """
        Generate 6 walking animation frames programmatically (US-048).

        Creates a human-like character with short hair, grey t-shirt, blue jeans,
        head, body, arms, and legs. Each frame has different leg positions to
        create a walking effect.

        Returns:
            list: List of 6 pygame.Surface objects representing walk cycle
        """
        frames = []

        for i in range(6):
            # Create a new surface for each frame with transparency
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0))  # Transparent background

            # Calculate leg positions based on frame number
            # Create a walking effect by varying leg positions
            leg_offset = math.sin(i * math.pi / 3) * 5  # Oscillate between -5 and 5 pixels
            arm_offset = math.sin(i * math.pi / 3) * 3  # Arms swing opposite to legs

            # Color palette
            skin_color = (255, 220, 177)  # Light skin tone
            hair_color = (101, 67, 33)  # Dark brown hair
            shirt_color = (128, 128, 128)  # Grey t-shirt
            jeans_color = (70, 130, 180)  # Blue jeans

            # Draw legs (blue jeans) with walking motion
            leg_width = 7
            leg_height = 18

            # Left leg (jeans)
            left_leg_x = self.width // 2 - 9 + int(leg_offset)
            left_leg_y = self.height - leg_height
            pygame.draw.rect(frame, jeans_color,
                           (left_leg_x, left_leg_y, leg_width, leg_height))

            # Right leg (jeans)
            right_leg_x = self.width // 2 + 2 - int(leg_offset)
            right_leg_y = self.height - leg_height
            pygame.draw.rect(frame, jeans_color,
                           (right_leg_x, right_leg_y, leg_width, leg_height))

            # Draw body/torso (grey t-shirt)
            body_rect = pygame.Rect(8, 16, self.width - 16, 26)
            pygame.draw.rect(frame, shirt_color, body_rect, border_radius=3)

            # Draw arms (skin tone) with swing motion
            arm_width = 5
            arm_height = 20

            # Left arm (swings opposite to right leg)
            left_arm_x = 5
            left_arm_y = 20 - int(arm_offset)
            pygame.draw.rect(frame, skin_color,
                           (left_arm_x, left_arm_y, arm_width, arm_height))

            # Right arm (swings opposite to left leg)
            right_arm_x = self.width - 10
            right_arm_y = 20 + int(arm_offset)
            pygame.draw.rect(frame, skin_color,
                           (right_arm_x, right_arm_y, arm_width, arm_height))

            # Draw head (circular, skin tone)
            head_radius = 9
            head_center = (self.width // 2, 10)
            pygame.draw.circle(frame, skin_color, head_center, head_radius)

            # Draw short hair on top of head
            hair_rect = pygame.Rect(self.width // 2 - 8, 2, 16, 8)
            pygame.draw.ellipse(frame, hair_color, hair_rect)

            # Draw eyes (small black dots with white highlights)
            eye_color = (0, 0, 0)
            left_eye_pos = (self.width // 2 - 3, 10)
            right_eye_pos = (self.width // 2 + 3, 10)
            pygame.draw.circle(frame, eye_color, left_eye_pos, 2)
            pygame.draw.circle(frame, eye_color, right_eye_pos, 2)

            # Eye highlights (small white dots)
            pygame.draw.circle(frame, (255, 255, 255), (left_eye_pos[0] - 1, left_eye_pos[1] - 1), 1)
            pygame.draw.circle(frame, (255, 255, 255), (right_eye_pos[0] - 1, right_eye_pos[1] - 1), 1)

            # Draw simple smile
            mouth_color = (100, 50, 50)  # Dark red
            pygame.draw.arc(frame, mouth_color,
                          (self.width // 2 - 4, 11, 8, 5),
                          3.14, 6.28, 2)

            frames.append(frame)

        return frames

    def _generate_jump_frame(self):
        """
        Generate jumping animation frame for ascending motion (US-049).

        Shows human-like player with legs tucked in/bent for jumping pose when velocity_y < 0.
        Used when player is moving upward in the air.

        Returns:
            pygame.Surface: Jump frame surface
        """
        # Create a new surface with transparency
        frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        frame.fill((0, 0, 0, 0))  # Transparent background

        # Color palette
        skin_color = (255, 220, 177)  # Light skin tone
        hair_color = (101, 67, 33)  # Dark brown hair
        shirt_color = (128, 128, 128)  # Grey t-shirt
        jeans_color = (70, 130, 180)  # Blue jeans

        # Draw legs tucked/bent (both legs together, bent at knees) - jeans
        leg_width = 7
        leg_height = 14  # Shorter than walking (tucked)

        # Left leg (bent, close together)
        left_leg_x = self.width // 2 - 8
        left_leg_y = self.height - leg_height - 2
        pygame.draw.rect(frame, jeans_color, (left_leg_x, left_leg_y, leg_width, leg_height))

        # Right leg (bent, close together)
        right_leg_x = self.width // 2 + 1
        right_leg_y = self.height - leg_height - 2
        pygame.draw.rect(frame, jeans_color, (right_leg_x, right_leg_y, leg_width, leg_height))

        # Draw body/torso (grey t-shirt)
        body_rect = pygame.Rect(8, 14, self.width - 16, 26)
        pygame.draw.rect(frame, shirt_color, body_rect, border_radius=3)

        # Draw arms raised up (jumping pose)
        arm_width = 5
        arm_height = 18

        # Left arm (raised up)
        left_arm_x = 6
        left_arm_y = 10
        pygame.draw.rect(frame, skin_color, (left_arm_x, left_arm_y, arm_width, arm_height))

        # Right arm (raised up)
        right_arm_x = self.width - 11
        right_arm_y = 10
        pygame.draw.rect(frame, skin_color, (right_arm_x, right_arm_y, arm_width, arm_height))

        # Draw head (circular, skin tone)
        head_radius = 9
        head_center = (self.width // 2, 10)
        pygame.draw.circle(frame, skin_color, head_center, head_radius)

        # Draw short hair on top of head
        hair_rect = pygame.Rect(self.width // 2 - 8, 2, 16, 8)
        pygame.draw.ellipse(frame, hair_color, hair_rect)

        # Draw eyes (small black dots with highlights)
        eye_color = (0, 0, 0)
        left_eye_pos = (self.width // 2 - 3, 10)
        right_eye_pos = (self.width // 2 + 3, 10)
        pygame.draw.circle(frame, eye_color, left_eye_pos, 2)
        pygame.draw.circle(frame, eye_color, right_eye_pos, 2)

        # Eye highlights
        pygame.draw.circle(frame, (255, 255, 255), (left_eye_pos[0] - 1, left_eye_pos[1] - 1), 1)
        pygame.draw.circle(frame, (255, 255, 255), (right_eye_pos[0] - 1, right_eye_pos[1] - 1), 1)

        # Draw excited expression (open mouth - O shape)
        mouth_color = (100, 50, 50)
        pygame.draw.circle(frame, mouth_color, (self.width // 2, 13), 2)

        return frame

    def _generate_fall_frame(self):
        """
        Generate falling animation frame for descending motion (US-049).

        Shows human-like player with legs slightly extended for landing preparation when velocity_y > 0.
        Used when player is moving downward in the air.

        Returns:
            pygame.Surface: Fall frame surface
        """
        # Create a new surface with transparency
        frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        frame.fill((0, 0, 0, 0))  # Transparent background

        # Color palette
        skin_color = (255, 220, 177)  # Light skin tone
        hair_color = (101, 67, 33)  # Dark brown hair
        shirt_color = (128, 128, 128)  # Grey t-shirt
        jeans_color = (70, 130, 180)  # Blue jeans

        # Draw legs extended/spread for landing preparation - jeans
        leg_width = 7
        leg_height = 19  # Longer legs (extended for landing)

        # Left leg (slightly spread)
        left_leg_x = self.width // 2 - 10
        left_leg_y = self.height - leg_height
        pygame.draw.rect(frame, jeans_color, (left_leg_x, left_leg_y, leg_width, leg_height))

        # Right leg (slightly spread)
        right_leg_x = self.width // 2 + 3
        right_leg_y = self.height - leg_height
        pygame.draw.rect(frame, jeans_color, (right_leg_x, right_leg_y, leg_width, leg_height))

        # Draw body/torso (grey t-shirt)
        body_rect = pygame.Rect(8, 16, self.width - 16, 26)
        pygame.draw.rect(frame, shirt_color, body_rect, border_radius=3)

        # Draw arms extended down (bracing for landing)
        arm_width = 5
        arm_height = 20

        # Left arm (extended downward)
        left_arm_x = 7
        left_arm_y = 24
        pygame.draw.rect(frame, skin_color, (left_arm_x, left_arm_y, arm_width, arm_height))

        # Right arm (extended downward)
        right_arm_x = self.width - 12
        right_arm_y = 24
        pygame.draw.rect(frame, skin_color, (right_arm_x, right_arm_y, arm_width, arm_height))

        # Draw head (circular, skin tone)
        head_radius = 9
        head_center = (self.width // 2, 10)
        pygame.draw.circle(frame, skin_color, head_center, head_radius)

        # Draw short hair on top of head
        hair_rect = pygame.Rect(self.width // 2 - 8, 2, 16, 8)
        pygame.draw.ellipse(frame, hair_color, hair_rect)

        # Draw eyes (small black dots with highlights)
        eye_color = (0, 0, 0)
        left_eye_pos = (self.width // 2 - 3, 10)
        right_eye_pos = (self.width // 2 + 3, 10)
        pygame.draw.circle(frame, eye_color, left_eye_pos, 2)
        pygame.draw.circle(frame, eye_color, right_eye_pos, 2)

        # Eye highlights
        pygame.draw.circle(frame, (255, 255, 255), (left_eye_pos[0] - 1, left_eye_pos[1] - 1), 1)
        pygame.draw.circle(frame, (255, 255, 255), (right_eye_pos[0] - 1, right_eye_pos[1] - 1), 1)

        # Draw concerned expression (small line mouth)
        mouth_color = (100, 50, 50)
        pygame.draw.line(frame, mouth_color,
                        (self.width // 2 - 3, 13),
                        (self.width // 2 + 3, 13), 2)

        return frame

    def _generate_idle_frames(self):
        """
        Generate 4-frame idle animation with subtle breathing effect (US-050).

        Creates a gentle breathing animation for human-like player when standing still.
        Uses sine wave motion to create subtle vertical body movement.

        Returns:
            list: List of 4 pygame.Surface objects representing idle cycle
        """
        frames = []

        for i in range(4):
            # Create a new surface with transparency
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0))  # Transparent background

            # Color palette
            skin_color = (255, 220, 177)  # Light skin tone
            hair_color = (101, 67, 33)  # Dark brown hair
            shirt_color = (128, 128, 128)  # Grey t-shirt
            jeans_color = (70, 130, 180)  # Blue jeans

            # Subtle breathing effect - body moves up/down slightly
            # Creates a sine wave pattern: 0 -> 1 -> 0 -> -1 -> 0
            breathing_offset = int(math.sin(i * math.pi / 2) * 1)  # Oscillate between -1 and 1 pixels

            # Draw legs (stationary, no movement during idle) - jeans
            leg_width = 7
            leg_height = 18

            # Left leg (stationary position)
            left_leg_x = self.width // 2 - 9
            left_leg_y = self.height - leg_height
            pygame.draw.rect(frame, jeans_color, (left_leg_x, left_leg_y, leg_width, leg_height))

            # Right leg (stationary position)
            right_leg_x = self.width // 2 + 2
            right_leg_y = self.height - leg_height
            pygame.draw.rect(frame, jeans_color, (right_leg_x, right_leg_y, leg_width, leg_height))

            # Draw body/torso (grey t-shirt) with breathing offset
            body_y = 16 + breathing_offset
            body_rect = pygame.Rect(8, body_y, self.width - 16, 26)
            pygame.draw.rect(frame, shirt_color, body_rect, border_radius=3)

            # Draw arms at sides (relaxed position)
            arm_width = 5
            arm_height = 20

            # Left arm (at side)
            left_arm_x = 5
            left_arm_y = 18 + breathing_offset
            pygame.draw.rect(frame, skin_color, (left_arm_x, left_arm_y, arm_width, arm_height))

            # Right arm (at side)
            right_arm_x = self.width - 10
            right_arm_y = 18 + breathing_offset
            pygame.draw.rect(frame, skin_color, (right_arm_x, right_arm_y, arm_width, arm_height))

            # Draw head (circular, skin tone) with breathing offset
            head_radius = 9
            head_center = (self.width // 2, 10 + breathing_offset)
            pygame.draw.circle(frame, skin_color, head_center, head_radius)

            # Draw short hair on top of head
            hair_rect = pygame.Rect(self.width // 2 - 8, 2 + breathing_offset, 16, 8)
            pygame.draw.ellipse(frame, hair_color, hair_rect)

            # Draw eyes (small black dots with highlights)
            eye_color = (0, 0, 0)
            left_eye_pos = (self.width // 2 - 3, 10 + breathing_offset)
            right_eye_pos = (self.width // 2 + 3, 10 + breathing_offset)
            pygame.draw.circle(frame, eye_color, left_eye_pos, 2)
            pygame.draw.circle(frame, eye_color, right_eye_pos, 2)

            # Eye highlights
            pygame.draw.circle(frame, (255, 255, 255), (left_eye_pos[0] - 1, left_eye_pos[1] - 1), 1)
            pygame.draw.circle(frame, (255, 255, 255), (right_eye_pos[0] - 1, right_eye_pos[1] - 1), 1)

            # Draw neutral expression (small smile)
            mouth_color = (100, 50, 50)
            pygame.draw.arc(frame, mouth_color,
                          (self.width // 2 - 4, 11 + breathing_offset, 8, 5),
                          3.14, 6.28, 2)

            frames.append(frame)

        return frames

    def _generate_shoot_frames(self):
        """
        Generate 4-frame shooting animation (US-051).

        Shows human-like player with extended arm/hand for laser shooting pose.
        Animation progresses: extend -> hold -> hold -> retract.

        Returns:
            list: List of 4 pygame.Surface objects representing shooting animation
        """
        frames = []

        for i in range(4):
            # Create a new surface with transparency
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0))  # Transparent background

            # Color palette
            skin_color = (255, 220, 177)  # Light skin tone
            hair_color = (101, 67, 33)  # Dark brown hair
            shirt_color = (128, 128, 128)  # Grey t-shirt
            jeans_color = (70, 130, 180)  # Blue jeans

            # Draw legs (stationary during shooting) - jeans
            leg_width = 7
            leg_height = 18

            # Left leg (stationary position)
            left_leg_x = self.width // 2 - 9
            left_leg_y = self.height - leg_height
            pygame.draw.rect(frame, jeans_color, (left_leg_x, left_leg_y, leg_width, leg_height))

            # Right leg (stationary position)
            right_leg_x = self.width // 2 + 2
            right_leg_y = self.height - leg_height
            pygame.draw.rect(frame, jeans_color, (right_leg_x, right_leg_y, leg_width, leg_height))

            # Draw body/torso (grey t-shirt)
            body_rect = pygame.Rect(8, 16, self.width - 16, 26)
            pygame.draw.rect(frame, shirt_color, body_rect, border_radius=3)

            # Calculate arm extension based on frame
            if i == 0:
                # Frame 0: Start extending arm
                arm_extension = 8
            elif i == 1:
                # Frame 1: Fully extended (shooting pose)
                arm_extension = 14
            elif i == 2:
                # Frame 2: Hold extended position
                arm_extension = 14
            else:
                # Frame 3: Retracting arm
                arm_extension = 6

            # Draw extended shooting arm (right side)
            arm_width = 5 + arm_extension
            arm_height = 5
            arm_x = self.width - 8  # Right side of body (will flip for left direction)
            arm_y = self.height // 2 - 3  # Center height (where laser emanates)
            pygame.draw.rect(frame, skin_color, (arm_x - arm_width, arm_y, arm_width, arm_height))

            # Draw non-shooting arm (left side, at side)
            left_arm_width = 5
            left_arm_height = 18
            left_arm_x = 5
            left_arm_y = 20
            pygame.draw.rect(frame, skin_color, (left_arm_x, left_arm_y, left_arm_width, left_arm_height))

            # Draw head (circular, skin tone)
            head_radius = 9
            head_center = (self.width // 2, 10)
            pygame.draw.circle(frame, skin_color, head_center, head_radius)

            # Draw short hair on top of head
            hair_rect = pygame.Rect(self.width // 2 - 8, 2, 16, 8)
            pygame.draw.ellipse(frame, hair_color, hair_rect)

            # Draw eyes (focused, determined look with highlights)
            eye_color = (0, 0, 0)
            left_eye_pos = (self.width // 2 - 3, 10)
            right_eye_pos = (self.width // 2 + 3, 10)
            pygame.draw.circle(frame, eye_color, left_eye_pos, 2)
            pygame.draw.circle(frame, eye_color, right_eye_pos, 2)

            # Eye highlights
            pygame.draw.circle(frame, (255, 255, 255), (left_eye_pos[0] - 1, left_eye_pos[1] - 1), 1)
            pygame.draw.circle(frame, (255, 255, 255), (right_eye_pos[0] - 1, right_eye_pos[1] - 1), 1)

            # Draw determined expression (straight line mouth)
            mouth_color = (100, 50, 50)
            pygame.draw.line(frame, mouth_color,
                            (self.width // 2 - 3, 13),
                            (self.width // 2 + 3, 13), 2)

            frames.append(frame)

        return frames

    def _generate_aura_frames(self):
        """
        Generate Dragon Ball Z-style Super Saiyan aura animation frames.
        Creates a pulsing golden energy aura around the player with flame-like shapes.

        Returns:
            None (stores frames in self.aura_frames)
        """
        self.aura_frames = []

        # Generate 8 frames for smooth aura animation
        for frame_num in range(8):
            # Create aura surface (larger than player to fit aura around them)
            aura_width = self.width + 30  # Extra space for aura
            aura_height = self.height + 30
            aura_surface = pygame.Surface((aura_width, aura_height), pygame.SRCALPHA)
            aura_surface.fill((0, 0, 0, 0))  # Transparent background

            # Golden aura colors (similar to Super Saiyan)
            aura_colors = [
                (255, 223, 0, 120),   # Bright gold (outer, more transparent)
                (255, 215, 0, 160),   # Gold
                (255, 200, 0, 180),   # Deeper gold
                (255, 180, 0, 140),   # Orange-gold (inner flames)
            ]

            # Center position (where player will be)
            center_x = aura_width // 2
            center_y = aura_height // 2

            # Animation phase (0.0 to 1.0)
            phase = frame_num / 8.0

            # Draw multiple layers of aura for depth
            for layer in range(4):
                # Layer-specific animation offset
                layer_phase = (phase + layer * 0.25) % 1.0

                # Pulsing size based on animation phase
                pulse = math.sin(layer_phase * math.pi * 2) * 3 + 3

                # Draw flame-like shapes around the player
                num_flames = 8 + layer * 2  # More flames in outer layers

                for i in range(num_flames):
                    angle = (i / num_flames) * math.pi * 2 + layer_phase * math.pi * 0.5

                    # Distance from center (varies by layer)
                    base_distance = 22 + layer * 5
                    distance = base_distance + pulse

                    # Flame position
                    flame_x = center_x + int(math.cos(angle) * distance)
                    flame_y = center_y + int(math.sin(angle) * distance)

                    # Flame size (varies with animation)
                    flame_size = int(8 + math.sin(angle + layer_phase * math.pi * 4) * 3)

                    # Flame shape (ellipse for upward flame effect)
                    flame_width = flame_size
                    flame_height = flame_size + 4

                    # Get color for this layer
                    color_idx = min(layer, len(aura_colors) - 1)
                    color = aura_colors[color_idx]

                    # Create flame surface with alpha
                    flame_surf = pygame.Surface((flame_width * 2, flame_height * 2), pygame.SRCALPHA)
                    pygame.draw.ellipse(flame_surf, color,
                                      (flame_width // 2, flame_height // 2,
                                       flame_width, flame_height))

                    # Blit flame to aura surface
                    aura_surface.blit(flame_surf,
                                    (flame_x - flame_width, flame_y - flame_height))

            # Draw energy glow in the center (brightest part)
            for radius_layer in range(5, 0, -1):
                alpha = int(40 + radius_layer * 15)
                glow_color = (255, 223, 0, alpha)
                glow_surf = pygame.Surface((aura_width, aura_height), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color,
                                 (center_x, center_y),
                                 18 + radius_layer * 2)
                aura_surface.blit(glow_surf, (0, 0))

            # Add some random energy sparks for extra effect
            for spark in range(5):
                spark_angle = (spark / 5.0) * math.pi * 2 + phase * math.pi * 4
                spark_dist = 20 + (spark % 3) * 5
                spark_x = center_x + int(math.cos(spark_angle) * spark_dist)
                spark_y = center_y + int(math.sin(spark_angle) * spark_dist)

                # Draw small spark circle
                pygame.draw.circle(aura_surface, (255, 255, 200, 200),
                                 (spark_x, spark_y), 2)

            self.aura_frames.append(aura_surface)

    def get_aura_surface(self):
        """
        Get the current aura animation frame for rendering.
        Returns None if player is not powered up.

        Returns:
            pygame.Surface or None: Current aura frame or None
        """
        if not self.is_powered_up or not self.aura_frames:
            return None

        return self.aura_frames[self.aura_frame_index]

    def get_aura_position(self):
        """
        Get the position where the aura should be drawn (centered on player).

        Returns:
            tuple: (x, y) position for aura blit
        """
        if not self.is_powered_up or not self.aura_frames:
            return None

        aura_surface = self.aura_frames[self.aura_frame_index]
        # Center aura on player
        aura_x = self.rect.centerx - aura_surface.get_width() // 2
        aura_y = self.rect.centery - aura_surface.get_height() // 2

        return (aura_x, aura_y)

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
        Handle player collecting a power-up (Golden Arepa) (US-017, US-018).

        Enters powered-up state for POWERUP_DURATION frames, enabling:
        - Laser shooting capability (US-019)
        - Golden border visual effect (US-018)
        - Powerup timer countdown (US-033)
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
        Check if player can shoot a laser (US-019).

        Player must be powered up and cooldown must be 0 to shoot.

        Returns:
            bool: True if player can shoot, False otherwise
        """
        return self.is_powered_up and self.shoot_cooldown == 0

    def shoot(self):
        """
        Attempt to shoot a laser (US-019, US-051).

        Triggers shooting animation and returns laser spawn position if successful.
        Applies shooting cooldown to prevent spamming.

        Returns:
            tuple or None: (x, y, direction) tuple if shot successful, None if cannot shoot
        """
        if not self.can_shoot():
            return None

        # Start cooldown
        self.shoot_cooldown = LASER_COOLDOWN

        # Trigger shooting animation (US-051)
        # Play shooting animation for 12 frames total (4 frames x 3 display frames each)
        self.is_shooting = True
        self.shoot_animation_timer = 12

        # Calculate laser spawn position (from center of player)
        laser_x = self.rect.centerx
        laser_y = self.rect.centery

        # Play laser shoot sound effect (US-043)
        if self.audio_manager:
            self.audio_manager.play_laser()

        return (laser_x, laser_y, self.facing_direction)

    def _update_appearance(self):
        """
        Update player visual appearance based on current state (US-018, US-048-051).

        Regenerates all animation frames with current powered-up state.
        Adds golden border when powered up, removes it when normal.
        Handles state transitions between all animation types.
        """
        # Regenerate animation frames with current powered-up state (US-048, US-049, US-050, US-051)
        self.walk_frames = self._generate_walk_frames()
        self.jump_frame = self._generate_jump_frame()
        self.fall_frame = self._generate_fall_frame()
        self.idle_frames = self._generate_idle_frames()
        self.shoot_frames = self._generate_shoot_frames()

        # Reset current_frame to prevent index out of bounds errors
        # Different animation states have different frame counts
        self.current_frame = 0

        # Set current image based on animation state
        if not self.is_grounded:
            # In air - use jump/fall animation (US-049)
            if self.velocity_y < 0:
                self.image = self.jump_frame.copy()  # Ascending
            else:
                self.image = self.fall_frame.copy()  # Descending
        elif self.is_walking:
            # Safety check for walking frames
            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0
            self.image = self.walk_frames[self.current_frame].copy()
        else:
            # Idle - use idle animation (US-050)
            # Safety check for idle frames
            if self.current_frame >= len(self.idle_frames):
                self.current_frame = 0
            self.image = self.idle_frames[self.current_frame].copy()

        # If powered up, add DBZ Super Saiyan aura effect
        if self.is_powered_up:
            # No need to modify self.image here - aura will be drawn separately
            # Just keep the base character image clean
            pass

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

        # Update aura animation if powered up
        if self.is_powered_up:
            self.aura_animation_timer += 1
            if self.aura_animation_timer >= self.aura_animation_speed:
                self.aura_animation_timer = 0
                self.aura_frame_index = (self.aura_frame_index + 1) % len(self.aura_frames)

        # Handle shooting animation timer (US-051)
        if self.is_shooting:
            self.shoot_animation_timer -= 1
            if self.shoot_animation_timer <= 0:
                self.is_shooting = False  # End shooting animation
                # Reset frame index to prevent out-of-bounds errors when returning to other animations
                self.current_frame = 0
                self.animation_timer = 0

        # Update animation based on player state (US-048, US-049, US-051)
        # Priority: shooting animation > jump/fall > walking > idle
        if self.is_shooting:
            # Player is shooting - use shooting animation (US-051)
            # Calculate which frame to display based on timer
            # Timer goes 12 -> 0, we have 4 frames, show each for 3 frames
            frame_index = (12 - self.shoot_animation_timer) // 3
            frame_index = min(frame_index, 3)  # Clamp to valid range (0-3)

            self.image = self.shoot_frames[frame_index].copy()

            # Flip sprite horizontally based on facing direction
            if self.facing_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            # Update original image for blinking effect
            self.original_image = self.image.copy()
        elif not self.is_grounded:
            # Player is in air - use jump/fall animation (US-049)
            if self.velocity_y < 0:
                # Ascending (jumping up)
                self.image = self.jump_frame.copy()
            else:
                # Descending (falling down)
                self.image = self.fall_frame.copy()

            # Flip sprite horizontally based on facing direction
            if self.facing_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            # Update original image for blinking effect
            self.original_image = self.image.copy()
        elif self.is_walking:
            # Player is walking on ground - use walking animation (US-048)
            # Increment animation timer
            self.animation_timer += 1

            # Advance to next frame when timer reaches animation speed
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)

            # Safety check: ensure current_frame is within bounds
            if self.current_frame >= len(self.walk_frames):
                self.current_frame = 0

            # Update image to current frame
            self.image = self.walk_frames[self.current_frame].copy()

            # Flip sprite horizontally based on facing direction (US-048)
            if self.facing_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            # Update original image for blinking effect
            self.original_image = self.image.copy()
        else:
            # Player is idle (not moving, on ground) - use idle animation (US-050)
            # Increment animation timer
            self.animation_timer += 1

            # Advance to next frame when timer reaches idle animation speed (slower than walk)
            if self.animation_timer >= self.idle_animation_speed:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)

            # Safety check: ensure current_frame is within bounds
            if self.current_frame >= len(self.idle_frames):
                self.current_frame = 0

            # Update image to current idle frame
            self.image = self.idle_frames[self.current_frame].copy()

            # Flip sprite horizontally based on facing direction
            if self.facing_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)

            # Update original image for blinking effect
            self.original_image = self.image.copy()
