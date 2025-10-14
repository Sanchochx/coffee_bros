"""
Level loading and management system.
Loads level data from JSON files and creates game entities.
"""

import json
import os
import pygame
from src.entities import Player, Platform, Polocho, GoldenArepa


class Level:
    """
    Level class that loads and manages level data from JSON files.
    Handles creation of all game entities including platforms, enemies, powerups, and player.
    """

    def __init__(self):
        """Initialize empty level."""
        self.metadata = {}
        self.player_spawn = {"spawn_x": 100, "spawn_y": 400}  # Default spawn
        self.goal = {}
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player = None
        self.initial_enemy_positions = []
        self.level_data = None

    @classmethod
    def load_from_file(cls, level_number):
        """
        Load level data from JSON file and create all game entities.

        Args:
            level_number (int): The level number to load (e.g., 1 for level_1.json)

        Returns:
            Level: A Level instance with all entities created and ready to use

        Raises:
            FileNotFoundError: If level file doesn't exist
            ValueError: If JSON is malformed or missing required fields
        """
        level = cls()

        # Construct file path
        level_file = f"assets/levels/level_{level_number}.json"

        # Check if file exists
        if not os.path.exists(level_file):
            raise FileNotFoundError(f"Level file not found: {level_file}")

        # Load JSON data
        try:
            with open(level_file, 'r') as f:
                level.level_data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {level_file}: {e}")

        # Validate required fields
        level._validate_level_data()

        # Load metadata
        level.metadata = level.level_data.get("metadata", {})

        # Load player spawn position
        player_data = level.level_data.get("player", {})
        level.player_spawn = {
            "spawn_x": player_data.get("spawn_x", 100),
            "spawn_y": player_data.get("spawn_y", 400)
        }

        # Create player at spawn position
        level.player = Player(level.player_spawn["spawn_x"], level.player_spawn["spawn_y"])
        level.all_sprites.add(level.player)

        # Load goal data
        level.goal = level.level_data.get("goal", {})

        # Create platforms from JSON data
        platforms_data = level.level_data.get("platforms", [])
        for platform_data in platforms_data:
            x = platform_data.get("x", 0)
            y = platform_data.get("y", 0)
            width = platform_data.get("width", 100)
            height = platform_data.get("height", 20)

            platform = Platform(x, y, width, height)
            level.platforms.add(platform)
            level.all_sprites.add(platform)

        # Create enemies from JSON data
        enemies_data = level.level_data.get("enemies", [])
        for enemy_data in enemies_data:
            enemy_type = enemy_data.get("type", "polocho")
            spawn_x = enemy_data.get("spawn_x", 0)
            spawn_y = enemy_data.get("spawn_y", 0)
            patrol_distance = enemy_data.get("patrol_distance", 150)

            # Store initial enemy position for respawning
            level.initial_enemy_positions.append({
                "type": enemy_type,
                "spawn_x": spawn_x,
                "spawn_y": spawn_y,
                "patrol_distance": patrol_distance
            })

            # Create enemy (currently only Polocho type supported)
            if enemy_type == "polocho":
                enemy = Polocho(spawn_x, spawn_y, patrol_distance)
                level.enemies.add(enemy)
                level.all_sprites.add(enemy)

        # Create powerups from JSON data
        powerups_data = level.level_data.get("powerups", [])
        for powerup_data in powerups_data:
            powerup_type = powerup_data.get("type", "golden_arepa")
            x = powerup_data.get("x", 0)
            y = powerup_data.get("y", 0)

            # Create powerup (currently only golden_arepa type supported)
            if powerup_type == "golden_arepa":
                powerup = GoldenArepa(x, y)
                level.powerups.add(powerup)
                level.all_sprites.add(powerup)

        return level

    def _validate_level_data(self):
        """
        Validate that level data contains all required fields.

        Raises:
            ValueError: If required fields are missing
        """
        if not isinstance(self.level_data, dict):
            raise ValueError("Level data must be a dictionary")

        # Check for required top-level fields
        required_fields = ["metadata", "player", "platforms"]
        for field in required_fields:
            if field not in self.level_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate metadata
        metadata = self.level_data.get("metadata", {})
        if "name" not in metadata:
            raise ValueError("Metadata missing 'name' field")
        if "level_number" not in metadata:
            raise ValueError("Metadata missing 'level_number' field")

        # Validate player spawn
        player_data = self.level_data.get("player", {})
        if "spawn_x" not in player_data or "spawn_y" not in player_data:
            raise ValueError("Player data missing spawn_x or spawn_y")

        # Validate platforms array
        platforms = self.level_data.get("platforms", [])
        if not isinstance(platforms, list):
            raise ValueError("Platforms must be an array")
        if len(platforms) == 0:
            raise ValueError("Level must have at least one platform")

    def respawn_player(self):
        """
        Respawn player at the original spawn position.
        Resets player velocity and grounded state.
        """
        if self.player:
            self.player.rect.x = self.player_spawn["spawn_x"]
            self.player.rect.y = self.player_spawn["spawn_y"]
            self.player.velocity_y = 0
            self.player.is_grounded = False

    def respawn_all_enemies(self):
        """
        Respawn all enemies at their original positions.
        Clears existing enemies and recreates them from stored positions.
        """
        # Clear existing enemies
        self.enemies.empty()

        # Recreate enemies from initial positions
        for enemy_pos in self.initial_enemy_positions:
            enemy_type = enemy_pos.get("type", "polocho")
            spawn_x = enemy_pos.get("spawn_x", 0)
            spawn_y = enemy_pos.get("spawn_y", 0)
            patrol_distance = enemy_pos.get("patrol_distance", 150)

            if enemy_type == "polocho":
                enemy = Polocho(spawn_x, spawn_y, patrol_distance)
                self.enemies.add(enemy)
                # Note: Don't add to all_sprites here - it's managed by reset_level()

    def reset_level(self):
        """
        Reset the entire level to initial state.
        Respawns player, enemies, and powerups.
        Used when player dies and respawns.
        """
        # Clear all sprite groups
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.powerups.empty()

        # Reload level from stored data
        if self.level_data:
            # Recreate player
            self.player = Player(self.player_spawn["spawn_x"], self.player_spawn["spawn_y"])
            self.all_sprites.add(self.player)

            # Recreate platforms
            platforms_data = self.level_data.get("platforms", [])
            for platform_data in platforms_data:
                x = platform_data.get("x", 0)
                y = platform_data.get("y", 0)
                width = platform_data.get("width", 100)
                height = platform_data.get("height", 20)

                platform = Platform(x, y, width, height)
                self.platforms.add(platform)
                self.all_sprites.add(platform)

            # Recreate enemies
            for enemy_pos in self.initial_enemy_positions:
                enemy_type = enemy_pos.get("type", "polocho")
                spawn_x = enemy_pos.get("spawn_x", 0)
                spawn_y = enemy_pos.get("spawn_y", 0)
                patrol_distance = enemy_pos.get("patrol_distance", 150)

                if enemy_type == "polocho":
                    enemy = Polocho(spawn_x, spawn_y, patrol_distance)
                    self.enemies.add(enemy)
                    self.all_sprites.add(enemy)

            # Recreate powerups
            powerups_data = self.level_data.get("powerups", [])
            for powerup_data in powerups_data:
                powerup_type = powerup_data.get("type", "golden_arepa")
                x = powerup_data.get("x", 0)
                y = powerup_data.get("y", 0)

                if powerup_type == "golden_arepa":
                    powerup = GoldenArepa(x, y)
                    self.powerups.add(powerup)
                    self.all_sprites.add(powerup)
