"""
Polocho enemy entity for Coffee Bros game.
"""
import pygame
import math
from config import GRAVITY, TERMINAL_VELOCITY, RED, ENEMY_SPEED


class Polocho(pygame.sprite.Sprite):
    """Enemy sprite class - Polocho enemies patrol and can be stomped."""

    def __init__(self, x, y, patrol_distance=150, audio_manager=None):
        """
        Initialize Polocho enemy.

        Args:
            x: Initial x position
            y: Initial y position
            patrol_distance: Distance in pixels the enemy patrols (half on each side)
            audio_manager: Optional audio manager for sound effects (US-042)
        """
        super().__init__()

        # Store audio manager reference (US-042)
        self.audio_manager = audio_manager
        print(f"Polocho initialized with audio_manager: {audio_manager}")

        # Enemy appearance - 40x40 pixels, red colored
        self.width = 40
        self.height = 40

        # Animation system (US-052)
        self.walk_frames = self._generate_walk_frames()  # 4 frames for walk cycle
        self.current_frame = 0  # Current animation frame index
        self.animation_timer = 0  # Timer for frame cycling
        self.animation_speed = 8  # Frames to display each animation frame (60 FPS / 8 = 7.5 FPS animation)

        # Create enemy surface with first walk frame
        self.image = self.walk_frames[0].copy()
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

    def _generate_walk_frames(self):
        """
        Generate 4 walking animation frames for Polocho enemy (US-052)
        Creates an evil, menacing creature with horns, sharp features, and glowing eyes

        Returns:
            list: List of 4 pygame.Surface objects representing walk cycle
        """
        frames = []

        for i in range(4):
            # Create a new surface with transparency
            frame = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            frame.fill((0, 0, 0, 0))  # Transparent background

            # Calculate leg positions based on frame number
            # Create a walking effect by varying leg positions
            leg_offset = math.sin(i * math.pi / 2) * 4  # Oscillate between -4 and 4 pixels

            # Evil color palette
            dark_red = (139, 0, 0)  # Dark red body
            blood_red = (180, 0, 0)  # Blood red accents
            evil_red = (220, 20, 60)  # Crimson red
            black = (0, 0, 0)  # Black details
            evil_glow = (255, 50, 50)  # Red glow for eyes

            # Draw legs with clawed feet (darker red)
            leg_width = 6
            leg_height = 12

            # Left leg
            left_leg_x = self.width // 2 - 8 + int(leg_offset)
            left_leg_y = self.height - leg_height
            pygame.draw.rect(frame, blood_red, (left_leg_x, left_leg_y, leg_width, leg_height))
            # Left claw (small triangle at bottom)
            pygame.draw.polygon(frame, black, [
                (left_leg_x - 2, self.height),
                (left_leg_x + leg_width // 2, self.height - 3),
                (left_leg_x, self.height)
            ])

            # Right leg (opposite phase)
            right_leg_x = self.width // 2 + 2 - int(leg_offset)
            right_leg_y = self.height - leg_height
            pygame.draw.rect(frame, blood_red, (right_leg_x, right_leg_y, leg_width, leg_height))
            # Right claw
            pygame.draw.polygon(frame, black, [
                (right_leg_x + leg_width, self.height),
                (right_leg_x + leg_width // 2, self.height - 3),
                (right_leg_x + leg_width + 2, self.height)
            ])

            # Draw body (menacing ellipse shape)
            body_rect = pygame.Rect(4, 4, self.width - 8, self.height - 16)
            pygame.draw.ellipse(frame, evil_red, body_rect)

            # Draw darker inner shadow for depth
            inner_shadow_rect = pygame.Rect(6, 6, self.width - 12, self.height - 20)
            pygame.draw.ellipse(frame, dark_red, inner_shadow_rect)

            # Draw evil horns on top of head
            horn_color = black
            # Left horn
            left_horn_points = [
                (self.width // 2 - 8, 8),  # Base
                (self.width // 2 - 10, 2),  # Tip
                (self.width // 2 - 6, 6)   # Inner point
            ]
            pygame.draw.polygon(frame, horn_color, left_horn_points)

            # Right horn
            right_horn_points = [
                (self.width // 2 + 8, 8),  # Base
                (self.width // 2 + 10, 2),  # Tip
                (self.width // 2 + 6, 6)   # Inner point
            ]
            pygame.draw.polygon(frame, horn_color, right_horn_points)

            # Draw menacing glowing eyes (larger, evil looking)
            left_eye_pos = (self.width // 2 - 7, self.height // 3)
            right_eye_pos = (self.width // 2 + 7, self.height // 3)

            # Outer glow
            pygame.draw.circle(frame, evil_glow, left_eye_pos, 5)
            pygame.draw.circle(frame, evil_glow, right_eye_pos, 5)

            # Inner pupil (vertical slit like a demon)
            pygame.draw.ellipse(frame, black, (left_eye_pos[0] - 1, left_eye_pos[1] - 3, 2, 6))
            pygame.draw.ellipse(frame, black, (right_eye_pos[0] - 1, right_eye_pos[1] - 3, 2, 6))

            # Draw evil fanged mouth (jagged teeth)
            mouth_y = self.height // 2 + 2
            pygame.draw.line(frame, black,
                           (self.width // 2 - 6, mouth_y),
                           (self.width // 2 + 6, mouth_y), 2)
            # Fangs (small triangles)
            pygame.draw.polygon(frame, (255, 255, 255), [
                (self.width // 2 - 4, mouth_y),
                (self.width // 2 - 3, mouth_y + 3),
                (self.width // 2 - 2, mouth_y)
            ])
            pygame.draw.polygon(frame, (255, 255, 255), [
                (self.width // 2 + 2, mouth_y),
                (self.width // 2 + 3, mouth_y + 3),
                (self.width // 2 + 4, mouth_y)
            ])

            frames.append(frame)

        return frames

    def _generate_squashed_frame(self):
        """
        Generate squashed animation frame for defeated enemy (US-053)
        Creates a flattened/compressed sprite showing clear defeat

        Returns:
            pygame.Surface: Squashed sprite frame
        """
        # Squashed dimensions - reduce height significantly, increase width
        squashed_width = int(self.width * 1.5)  # 50% wider
        squashed_height = int(self.height * 0.25)  # 25% of original height (very flat)

        # Create squashed frame surface with transparency
        frame = pygame.Surface((squashed_width, squashed_height), pygame.SRCALPHA)
        frame.fill((0, 0, 0, 0))  # Transparent background

        # Evil color palette (same as walk frames)
        dark_red = (139, 0, 0)
        evil_red = (220, 20, 60)

        # Draw flattened body (ellipse stretched horizontally)
        body_rect = pygame.Rect(2, 2, squashed_width - 4, squashed_height - 4)
        pygame.draw.ellipse(frame, evil_red, body_rect)

        # Draw darker inner
        inner_rect = pygame.Rect(4, 3, squashed_width - 8, squashed_height - 6)
        pygame.draw.ellipse(frame, dark_red, inner_rect)

        # Draw squashed eyes (X's to show defeat)
        black = (0, 0, 0)

        # Left eye X
        left_eye_x = squashed_width // 3
        eye_y = squashed_height // 2
        # Draw X by drawing two small lines
        pygame.draw.line(frame, black,
                        (left_eye_x - 3, eye_y - 2),
                        (left_eye_x + 3, eye_y + 2), 2)
        pygame.draw.line(frame, black,
                        (left_eye_x - 3, eye_y + 2),
                        (left_eye_x + 3, eye_y - 2), 2)

        # Right eye X
        right_eye_x = squashed_width * 2 // 3
        pygame.draw.line(frame, black,
                        (right_eye_x - 3, eye_y - 2),
                        (right_eye_x + 3, eye_y + 2), 2)
        pygame.draw.line(frame, black,
                        (right_eye_x - 3, eye_y + 2),
                        (right_eye_x + 3, eye_y - 2), 2)

        # Draw flattened broken horns
        pygame.draw.line(frame, black, (squashed_width // 3 - 5, eye_y - 1),
                        (squashed_width // 3 - 8, eye_y), 2)
        pygame.draw.line(frame, black, (squashed_width * 2 // 3 + 5, eye_y - 1),
                        (squashed_width * 2 // 3 + 8, eye_y), 2)

        return frame

    def squash(self):
        """Mark enemy as squashed and start squash timer (US-042, US-053)."""
        if not self.is_squashed:
            self.is_squashed = True
            self.squash_timer = 15  # Show squashed state for 15 frames (~0.25 seconds)

            # Change appearance to show squashed state (US-053)
            old_centerx = self.rect.centerx
            old_bottom = self.rect.bottom

            # Generate and apply squashed sprite
            self.image = self._generate_squashed_frame()
            self.rect = self.image.get_rect()
            self.rect.bottom = old_bottom  # Keep bottom position same
            self.rect.centerx = old_centerx  # Keep horizontal center

            # Play stomp sound effect (US-042)
            if self.audio_manager:
                self.audio_manager.play_stomp()

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

        # Update walking animation (US-052)
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

        # Flip sprite horizontally based on movement direction (US-052)
        # direction = 1 means moving right (no flip)
        # direction = -1 means moving left (flip horizontally)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)
