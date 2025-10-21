"""
Corruption Boss entity for Coffee Bros final level
The ultimate enemy - a massive corruption monster that must be defeated
"""

import pygame
import os
import math

class CorruptionBoss(pygame.sprite.Sprite):
    """
    Massive corruption boss - final enemy
    Features:
    - Large sprite (150x180)
    - Health bar system
    - Takes damage from stomps and lasers
    - Movement patterns
    - Hit flash effect
    """

    def __init__(self, x, y, audio_manager=None):
        """
        Initialize the Corruption Boss

        Args:
            x: Starting x position
            y: Starting y position (bottom of sprite)
            audio_manager: AudioManager instance for sound effects
        """
        super().__init__()

        # Boss stats
        self.max_health = 20  # Takes 20 hits to defeat
        self.health = self.max_health
        self.damage_per_hit = 1  # Each hit deals 1 damage

        # Load boss sprites
        self.load_sprites()

        # Set initial image and rect
        self.image = self.normal_sprite
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # Physics
        self.vel_x = 2  # Boss moves slowly side to side
        self.vel_y = 0
        self.on_ground = False

        # Movement bounds (boss patrols the arena)
        self.patrol_left = x - 200
        self.patrol_right = x + 200
        self.direction = 1  # 1 = right, -1 = left

        # Hit detection and invulnerability
        self.hit_timer = 0
        self.hit_duration = 20  # Frames to show hit effect
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 30  # Frames of invulnerability after hit

        # Audio
        self.audio_manager = audio_manager

        # Alive state
        self.alive = True
        self.defeated = False

        # Mermelada throwing
        self.throw_cooldown = 0
        self.throw_interval = 90  # Throw every 1.5 seconds (90 frames at 60 FPS)

    def load_sprites(self):
        """Load boss sprite images"""
        boss_dir = "assets/images/boss"

        # Load normal sprite
        normal_path = os.path.join(boss_dir, "corruption_boss.png")
        if os.path.exists(normal_path):
            self.normal_sprite = pygame.image.load(normal_path).convert_alpha()
        else:
            # Fallback: create simple sprite
            self.normal_sprite = self.create_fallback_sprite()

        # Load hit sprite
        hit_path = os.path.join(boss_dir, "corruption_boss_hit.png")
        if os.path.exists(hit_path):
            self.hit_sprite = pygame.image.load(hit_path).convert_alpha()
        else:
            self.hit_sprite = self.create_fallback_sprite((255, 100, 100))

    def create_fallback_sprite(self, color=(100, 50, 150)):
        """Create a simple fallback sprite if image files don't exist"""
        surface = pygame.Surface((200, 240), pygame.SRCALPHA)
        # Draw simple corruption blob (scaled to 200x240)
        pygame.draw.circle(surface, color, (100, 120), 93)
        # Eyes
        pygame.draw.circle(surface, (255, 0, 0), (73, 107), 13)
        pygame.draw.circle(surface, (255, 0, 0), (127, 107), 13)
        return surface

    def take_damage(self, damage=1):
        """
        Boss takes damage

        Args:
            damage: Amount of damage to take

        Returns:
            bool: True if damage was dealt, False if boss is invulnerable
        """
        if self.invulnerable or not self.alive:
            return False

        self.health -= damage
        self.hit_timer = self.hit_duration
        self.invulnerable = True
        self.invulnerable_timer = self.invulnerable_duration

        # Play boss pain sound
        if self.audio_manager:
            self.audio_manager.play_boss_pain()  # Boss pain/damage sound

        # Check if defeated
        if self.health <= 0:
            self.health = 0
            self.defeated = True
            self.alive = False
            if self.audio_manager:
                self.audio_manager.play_sound('death')  # Boss defeated sound

        return True

    def update(self, platforms):
        """
        Update boss state

        Args:
            platforms: Sprite group of platforms for collision
        """
        if not self.alive:
            return

        # Update timers
        if self.hit_timer > 0:
            self.hit_timer -= 1

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer == 0:
                self.invulnerable = False

        # Movement - boss patrols side to side
        self.vel_x = self.direction * 2

        # Update position
        self.rect.x += self.vel_x

        # Check patrol bounds - reverse direction
        if self.rect.left <= self.patrol_left:
            self.direction = 1
            self.rect.left = self.patrol_left
        elif self.rect.right >= self.patrol_right:
            self.direction = -1
            self.rect.right = self.patrol_right

        # Apply gravity
        self.vel_y += 0.8  # Gravity
        if self.vel_y > 20:  # Terminal velocity
            self.vel_y = 20

        self.rect.y += self.vel_y

        # Platform collision (boss needs to stay on ground)
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Vertical collision
                if self.vel_y > 0:  # Falling
                    if self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.vel_y = 0
                        self.on_ground = True

        # Update sprite - always use normal sprite (hit effect removed per user request)
        self.image = self.normal_sprite

        # Update throw cooldown
        if self.throw_cooldown > 0:
            self.throw_cooldown -= 1

    def can_throw(self):
        """Check if boss can throw mermelada"""
        return self.alive and self.throw_cooldown == 0

    def throw_mermeladas_circular(self):
        """
        Throw mermeladas in a circular pattern around boss (old school arcade style)

        Returns:
            list: List of (x, y, angle) tuples for mermelada spawns, or None if can't throw
        """
        if not self.can_throw():
            return None

        # Reset cooldown
        self.throw_cooldown = self.throw_interval

        # Spawn position (boss center)
        spawn_x = self.rect.centerx
        spawn_y = self.rect.centery

        # Create 8 mermeladas in a circular pattern (like old arcade games)
        mermeladas = []
        num_projectiles = 8
        import math
        for i in range(num_projectiles):
            angle = (i / num_projectiles) * 2 * math.pi  # Distribute evenly in circle
            mermeladas.append((spawn_x, spawn_y, angle))

        return mermeladas

    def draw_health_bar(self, surface, camera_x=0):
        """
        Draw boss health bar above the boss

        Args:
            surface: Surface to draw on
            camera_x: Camera offset for scrolling
        """
        if not self.alive and self.defeated:
            return

        # Health bar dimensions
        bar_width = 150
        bar_height = 15
        bar_x = self.rect.centerx - camera_x - bar_width // 2
        bar_y = self.rect.top - 40  # Fixed: don't subtract camera_x from Y coordinate

        # Draw background (red)
        bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, (100, 0, 0), bg_rect)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect, 2)  # White border

        # Draw health (green to yellow to red based on health)
        health_percentage = self.health / self.max_health
        current_width = int(bar_width * health_percentage)

        if current_width > 0:
            # Color changes based on health
            if health_percentage > 0.6:
                health_color = (0, 200, 0)  # Green
            elif health_percentage > 0.3:
                health_color = (255, 200, 0)  # Yellow
            else:
                health_color = (255, 0, 0)  # Red

            health_rect = pygame.Rect(bar_x, bar_y, current_width, bar_height)
            pygame.draw.rect(surface, health_color, health_rect)

        # Boss name label removed per user request

    def get_damage_rect(self):
        """
        Get rect for player damage collision (touching boss hurts player)
        Slightly smaller than visual rect for fairness
        """
        damage_rect = self.rect.copy()
        damage_rect.inflate_ip(-20, -20)  # Shrink by 20 pixels each side
        return damage_rect

    def get_stomp_rect(self):
        """
        Get rect for stomp collision (top of boss)
        """
        stomp_rect = pygame.Rect(
            self.rect.left + 30,
            self.rect.top,
            self.rect.width - 60,
            20
        )
        return stomp_rect
