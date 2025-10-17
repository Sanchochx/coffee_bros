"""
Particle system for Sancho Bros game
Handles visual effects like stomping particles and powerup collection particles
"""
import pygame
import random
from config import YELLOW, RED, GOLD


class Particle(pygame.sprite.Sprite):
    """
    Individual particle sprite
    Used for visual effects like enemy stomp impacts
    """

    def __init__(self, x, y, color, velocity_x, velocity_y, lifetime=25):
        """
        Initialize a particle

        Args:
            x (int): Starting x position
            y (int): Starting y position
            color (tuple): RGB color of the particle
            velocity_x (float): Horizontal velocity in pixels per frame
            velocity_y (float): Vertical velocity in pixels per frame
            lifetime (int): Number of frames before particle disappears
        """
        super().__init__()

        # Particle dimensions (small square)
        self.size = random.randint(3, 6)  # Random size between 3-6 pixels

        # Create particle surface
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Movement properties
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.gravity = 0.3  # Slight gravity effect on particles

        # Lifetime tracking
        self.lifetime = lifetime  # Total lifetime in frames
        self.age = 0  # Current age in frames
        self.initial_color = color  # Store original color for fading

    def update(self):
        """
        Update particle position and handle fading/lifetime
        """
        # Update position based on velocity
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Apply gravity to vertical velocity
        self.velocity_y += self.gravity

        # Increment age
        self.age += 1

        # Fade out effect: reduce alpha based on age/lifetime ratio
        # Particles become more transparent as they approach end of lifetime
        fade_ratio = 1.0 - (self.age / self.lifetime)
        alpha = int(255 * fade_ratio)

        # Update image alpha (transparency)
        self.image.set_alpha(alpha)

        # Kill particle when lifetime expires
        if self.age >= self.lifetime:
            self.kill()


class ParticleSystem:
    """
    Particle system manager
    Creates and manages groups of particles for various effects
    """

    @staticmethod
    def create_stomp_particles(x, y, particle_group):
        """
        Create particles for enemy stomp effect (US-058)
        Spawns 5-10 small particles that spread outward from impact point

        Args:
            x (int): X position of stomp impact (center of enemy)
            y (int): Y position of stomp impact (top of enemy)
            particle_group (pygame.sprite.Group): Group to add particles to
        """
        num_particles = random.randint(5, 10)  # Random number of particles

        # Colors for stomp particles (reds and dark colors)
        particle_colors = [
            (255, 100, 100),  # Light red
            (200, 50, 50),    # Medium red
            (150, 0, 0),      # Dark red
            (100, 100, 100),  # Gray
            (80, 80, 80),     # Dark gray
        ]

        for _ in range(num_particles):
            # Random color from palette
            color = random.choice(particle_colors)

            # Random velocity - spread particles outward in all directions
            # Horizontal velocity: -4 to 4 pixels per frame
            velocity_x = random.uniform(-4, 4)
            # Vertical velocity: upward bias (-6 to -2) for explosion effect
            velocity_y = random.uniform(-6, -2)

            # Random lifetime between 20-30 frames (~0.33-0.5 seconds at 60 FPS)
            lifetime = random.randint(20, 30)

            # Create particle and add to group
            particle = Particle(x, y, color, velocity_x, velocity_y, lifetime)
            particle_group.add(particle)

    @staticmethod
    def create_powerup_particles(x, y, particle_group):
        """
        Create particles for powerup collection effect (US-059)
        Spawns golden/yellow particles that float upward

        Args:
            x (int): X position of powerup (center)
            y (int): Y position of powerup (center)
            particle_group (pygame.sprite.Group): Group to add particles to
        """
        num_particles = random.randint(8, 12)  # More particles for powerup effect

        # Colors for powerup particles (golds and yellows)
        particle_colors = [
            GOLD,             # Gold
            YELLOW,           # Yellow
            (255, 215, 0),    # Bright gold
            (255, 255, 150),  # Light yellow
        ]

        for _ in range(num_particles):
            # Random color from palette
            color = random.choice(particle_colors)

            # Random velocity - spread particles outward and upward
            # Horizontal velocity: -3 to 3 pixels per frame
            velocity_x = random.uniform(-3, 3)
            # Vertical velocity: upward (-5 to -1) for rising effect
            velocity_y = random.uniform(-5, -1)

            # Random lifetime between 25-35 frames (~0.4-0.6 seconds at 60 FPS)
            lifetime = random.randint(25, 35)

            # Create particle and add to group
            particle = Particle(x, y, color, velocity_x, velocity_y, lifetime)
            particle_group.add(particle)
