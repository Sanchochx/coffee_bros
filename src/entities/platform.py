"""
Platform entity module for Coffee Bros
Contains the Platform sprite class for ground and floating platforms.
"""

import pygame
import os
from config import GREEN


class Platform(pygame.sprite.Sprite):
    """Platform class for ground and floating platforms"""

    # Class-level tile cache to avoid reloading images
    _tile_cache = {}
    TILE_SIZE = 50

    @classmethod
    def _load_tiles(cls, texture_type):
        """
        Load tile images for a given texture type

        Args:
            texture_type (str): Type of texture ('grass' or 'stone')

        Returns:
            dict: Dictionary with 'left', 'middle', 'right' tile surfaces
        """
        if texture_type in cls._tile_cache:
            return cls._tile_cache[texture_type]

        # Construct paths to tile images
        base_path = os.path.join('assets', 'images', 'tiles')
        tiles = {}

        try:
            tiles['left'] = pygame.image.load(os.path.join(base_path, f'{texture_type}_left.png')).convert_alpha()
            tiles['middle'] = pygame.image.load(os.path.join(base_path, f'{texture_type}_middle.png')).convert_alpha()
            tiles['right'] = pygame.image.load(os.path.join(base_path, f'{texture_type}_right.png')).convert_alpha()

            # Cache the loaded tiles
            cls._tile_cache[texture_type] = tiles
            return tiles

        except pygame.error as e:
            print(f"Warning: Could not load tiles for {texture_type}: {e}")
            return None

    def __init__(self, x, y, width, height, platform_type='ground', texture='grass'):
        """
        Initialize a platform

        Args:
            x (int): Platform x position (left edge)
            y (int): Platform y position (top edge)
            width (int): Platform width in pixels
            height (int): Platform height in pixels
            platform_type (str): Type of platform ('ground' or 'floating')
            texture (str): Texture type ('grass' or 'stone')
        """
        super().__init__()

        self.platform_type = platform_type
        self.texture = texture

        # Create platform surface
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)  # Fallback color

        # Apply tiled texture
        self._apply_texture(width, height)

        # Get rect for positioning
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _apply_texture(self, width, height):
        """
        Apply tiled texture to the platform surface

        Args:
            width (int): Platform width
            height (int): Platform height
        """
        tiles = self._load_tiles(self.texture)

        if not tiles:
            # If tiles couldn't be loaded, use solid color fallback
            return

        # Calculate how many tiles we need
        num_tiles = max(1, width // self.TILE_SIZE)

        # For very small platforms (less than 2 tiles wide), just use middle tile
        if width < self.TILE_SIZE * 2:
            # Scale middle tile to fit
            scaled_tile = pygame.transform.scale(tiles['middle'], (width, height))
            self.image.blit(scaled_tile, (0, 0))
            return

        # Calculate actual tile positions
        current_x = 0

        # Left edge tile
        left_tile = pygame.transform.scale(tiles['left'], (self.TILE_SIZE, height))
        self.image.blit(left_tile, (current_x, 0))
        current_x += self.TILE_SIZE

        # Middle tiles
        while current_x < width - self.TILE_SIZE:
            # Calculate remaining width
            remaining = width - current_x - self.TILE_SIZE

            if remaining >= self.TILE_SIZE:
                # Full middle tile
                middle_tile = pygame.transform.scale(tiles['middle'], (self.TILE_SIZE, height))
                self.image.blit(middle_tile, (current_x, 0))
                current_x += self.TILE_SIZE
            else:
                # Partial middle tile (crop it)
                middle_tile = pygame.transform.scale(tiles['middle'], (remaining, height))
                self.image.blit(middle_tile, (current_x, 0))
                current_x += remaining

        # Right edge tile
        if width >= self.TILE_SIZE * 2:
            right_tile = pygame.transform.scale(tiles['right'], (self.TILE_SIZE, height))
            self.image.blit(right_tile, (width - self.TILE_SIZE, 0))
