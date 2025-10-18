"""
Performance optimization utilities for Sancho Bros.
Provides optimized collision detection and rendering techniques.
"""

import pygame


class SpatialGrid:
    """
    Spatial partitioning grid for efficient collision detection.
    Divides the game world into cells to reduce collision checks from O(n²) to O(n).
    """

    def __init__(self, cell_size=100):
        """
        Initialize spatial grid.

        Args:
            cell_size (int): Size of each grid cell in pixels
        """
        self.cell_size = cell_size
        self.grid = {}  # Dictionary mapping (grid_x, grid_y) to list of sprites

    def clear(self):
        """Clear all sprites from the grid."""
        self.grid.clear()

    def _get_cell(self, x, y):
        """
        Get grid cell coordinates for a world position.

        Args:
            x (int): World x coordinate
            y (int): World y coordinate

        Returns:
            tuple: (grid_x, grid_y) cell coordinates
        """
        return (int(x // self.cell_size), int(y // self.cell_size))

    def _get_cells_for_rect(self, rect):
        """
        Get all grid cells that a rectangle overlaps.

        Args:
            rect (pygame.Rect): Rectangle to check

        Returns:
            list: List of (grid_x, grid_y) cell coordinates
        """
        cells = []

        # Get cell range the rect spans
        min_cell_x, min_cell_y = self._get_cell(rect.left, rect.top)
        max_cell_x, max_cell_y = self._get_cell(rect.right, rect.bottom)

        # Add all cells in the range
        for cx in range(min_cell_x, max_cell_x + 1):
            for cy in range(min_cell_y, max_cell_y + 1):
                cells.append((cx, cy))

        return cells

    def insert(self, sprite):
        """
        Insert a sprite into the grid.

        Args:
            sprite (pygame.sprite.Sprite): Sprite to insert
        """
        cells = self._get_cells_for_rect(sprite.rect)

        for cell in cells:
            if cell not in self.grid:
                self.grid[cell] = []
            self.grid[cell].append(sprite)

    def get_nearby(self, sprite):
        """
        Get all sprites in the same or adjacent cells as the given sprite.

        Args:
            sprite (pygame.sprite.Sprite): Sprite to check around

        Returns:
            set: Set of nearby sprites (excludes the query sprite itself)
        """
        nearby = set()
        cells = self._get_cells_for_rect(sprite.rect)

        for cell in cells:
            if cell in self.grid:
                for other_sprite in self.grid[cell]:
                    if other_sprite != sprite:
                        nearby.add(other_sprite)

        return nearby


class AssetCache:
    """
    Cache for preloading and storing game assets.
    Ensures assets are loaded once and reused, reducing loading times and memory usage.
    """

    def __init__(self):
        """Initialize asset cache."""
        self.images = {}  # Dictionary mapping file paths to loaded images
        self.sounds = {}  # Dictionary mapping file paths to loaded sounds
        self.fonts = {}   # Dictionary mapping (font_path, size) to loaded fonts

    def preload_image(self, path):
        """
        Preload an image into the cache.

        Args:
            path (str): Path to image file

        Returns:
            pygame.Surface: Loaded image surface, or None if loading failed
        """
        if path not in self.images:
            try:
                image = pygame.image.load(path).convert_alpha()
                self.images[path] = image
                return image
            except pygame.error as e:
                print(f"Warning: Failed to load image {path}: {e}")
                return None
        return self.images[path]

    def get_image(self, path):
        """
        Get cached image or load it if not cached.

        Args:
            path (str): Path to image file

        Returns:
            pygame.Surface: Image surface, or None if loading failed
        """
        if path in self.images:
            return self.images[path]
        return self.preload_image(path)

    def preload_sound(self, path):
        """
        Preload a sound into the cache.

        Args:
            path (str): Path to sound file

        Returns:
            pygame.mixer.Sound: Loaded sound, or None if loading failed
        """
        if path not in self.sounds:
            try:
                sound = pygame.mixer.Sound(path)
                self.sounds[path] = sound
                return sound
            except pygame.error as e:
                print(f"Warning: Failed to load sound {path}: {e}")
                return None
        return self.sounds[path]

    def get_sound(self, path):
        """
        Get cached sound or load it if not cached.

        Args:
            path (str): Path to sound file

        Returns:
            pygame.mixer.Sound: Sound object, or None if loading failed
        """
        if path in self.sounds:
            return self.sounds[path]
        return self.preload_sound(path)

    def get_font(self, path, size):
        """
        Get cached font or load it if not cached.

        Args:
            path (str): Path to font file (or None for default font)
            size (int): Font size

        Returns:
            pygame.font.Font: Font object
        """
        key = (path, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(path, size)
        return self.fonts[key]

    def clear(self):
        """Clear all cached assets."""
        self.images.clear()
        self.sounds.clear()
        self.fonts.clear()


class OptimizedRenderer:
    """
    Optimized rendering system with dirty rectangle tracking and sprite batching.
    """

    def __init__(self, screen):
        """
        Initialize optimized renderer.

        Args:
            screen (pygame.Surface): Game screen surface
        """
        self.screen = screen
        self.background = None
        self.dirty_rects = []

    def set_background(self, background):
        """
        Set the background surface for dirty rectangle optimization.

        Args:
            background (pygame.Surface): Background surface
        """
        self.background = background

    def draw_sprites_with_offset(self, sprites, camera_x):
        """
        Draw sprites with camera offset efficiently.
        Uses screen culling to skip sprites outside the visible area.

        Args:
            sprites (pygame.sprite.Group or list): Sprites to draw
            camera_x (int): Camera horizontal offset

        Returns:
            int: Number of sprites actually drawn (for debugging)
        """
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        drawn_count = 0

        for sprite in sprites:
            # Calculate sprite's screen position
            screen_x = sprite.rect.x - camera_x

            # Screen culling: skip sprites outside visible area
            # Add margin for partially visible sprites
            margin = 50
            if (screen_x + sprite.rect.width < -margin or
                screen_x > screen_width + margin or
                sprite.rect.y + sprite.rect.height < -margin or
                sprite.rect.y > screen_height + margin):
                continue

            # Check if sprite is a Player with powered-up aura (DBZ Super Saiyan style)
            # Import Player class locally to avoid circular imports
            from src.entities.player import Player

            if isinstance(sprite, Player):
                # Draw aura behind the player if powered up
                aura_surface = sprite.get_aura_surface()
                if aura_surface is not None:
                    aura_pos = sprite.get_aura_position()
                    if aura_pos:
                        # Apply camera offset to aura position
                        aura_screen_x = aura_pos[0] - camera_x
                        aura_screen_y = aura_pos[1]
                        self.screen.blit(aura_surface, (aura_screen_x, aura_screen_y))

            # Draw sprite at offset position
            offset_rect = sprite.rect.copy()
            offset_rect.x = screen_x
            self.screen.blit(sprite.image, offset_rect)
            drawn_count += 1

        return drawn_count


def optimize_collision_detection(sprite, target_group, spatial_grid=None):
    """
    Optimized collision detection helper function.
    Uses spatial grid if provided, falls back to standard pygame collision if not.

    Args:
        sprite (pygame.sprite.Sprite): Sprite to check collisions for
        target_group (pygame.sprite.Group): Group of sprites to check against
        spatial_grid (SpatialGrid): Optional spatial grid for optimization

    Returns:
        list: List of sprites that collide with the given sprite
    """
    if spatial_grid:
        # Use spatial grid for optimization
        nearby = spatial_grid.get_nearby(sprite)
        collisions = []

        for other in nearby:
            if sprite.rect.colliderect(other.rect):
                collisions.append(other)

        return collisions
    else:
        # Fall back to standard pygame collision detection
        return pygame.sprite.spritecollide(sprite, target_group, False)


def limit_particle_count(particle_group, max_particles=100):
    """
    Limit the number of active particles to prevent performance degradation.
    Removes oldest particles when limit is exceeded.

    Args:
        particle_group (pygame.sprite.Group): Group containing particles
        max_particles (int): Maximum number of particles allowed

    Returns:
        int: Number of particles removed
    """
    if len(particle_group) <= max_particles:
        return 0

    # Convert to list and sort by age (oldest first)
    particles = list(particle_group)
    particles.sort(key=lambda p: p.age if hasattr(p, 'age') else 0, reverse=True)

    # Remove excess particles
    removed_count = 0
    excess = len(particles) - max_particles

    for i in range(excess):
        particles[i].kill()
        removed_count += 1

    return removed_count
