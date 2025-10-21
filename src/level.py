"""
Level loading and management system.
Loads level data from JSON files and creates game entities.
"""

import json
import os
import time
import pygame
from src.entities import Player, Platform, Polocho, GoldenArepa, Goal, CorruptionBoss


class Level:
    """
    Level class that loads and manages level data from JSON files.
    Handles creation of all game entities including platforms, enemies, powerups, and player.
    """

    def __init__(self, audio_manager=None):
        """
        Initialize empty level.

        Args:
            audio_manager (AudioManager): Optional audio manager for sound effects (US-041)
        """
        self.metadata = {}
        self.player_spawn = {"spawn_x": 100, "spawn_y": 400}  # Default spawn
        self.goal_data = {}
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.goals = pygame.sprite.Group()  # Sprite group for goals
        self.all_sprites = pygame.sprite.Group()
        self.player = None
        self.goal_sprite = None  # Reference to the goal sprite
        self.boss = None  # Reference to boss sprite (level 5 only)
        self.initial_enemy_positions = []
        self.level_data = None
        self.audio_manager = audio_manager  # Store audio manager reference (US-041)
        self.background_image = None  # Background image surface (US-056)

    @classmethod
    def load_from_file(cls, level_number, audio_manager=None):
        """
        Load level data from JSON file and create all game entities.
        Optimized for fast loading (US-063).

        Args:
            level_number (int): The level number to load (e.g., 1 for level_1.json)
            audio_manager (AudioManager): Optional audio manager for sound effects (US-041)

        Returns:
            Level: A Level instance with all entities created and ready to use

        Raises:
            FileNotFoundError: If level file doesn't exist
            ValueError: If JSON is malformed or missing required fields
        """
        # Track loading time for performance monitoring (US-063)
        start_time = time.time()

        level = cls(audio_manager)

        # Construct file path (cross-platform compatible - US-067)
        level_file = os.path.join("assets", "levels", f"level_{level_number}.json")

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

        # Load background image (US-056, US-067: cross-platform paths)
        background_type = level.metadata.get("background_type")
        if background_type:
            background_path = os.path.join("assets", "images", f"{background_type}.png")
            if os.path.exists(background_path):
                try:
                    level.background_image = pygame.image.load(background_path).convert()
                except pygame.error as e:
                    print(f"Warning: Could not load background image {background_path}: {e}")
                    level.background_image = None
            else:
                print(f"Warning: Background image not found: {background_path}")
                level.background_image = None

        # Load player spawn position
        player_data = level.level_data.get("player", {})
        level.player_spawn = {
            "spawn_x": player_data.get("spawn_x", 100),
            "spawn_y": player_data.get("spawn_y", 400)
        }

        # Create player at spawn position (US-041: pass audio_manager)
        level.player = Player(level.player_spawn["spawn_x"], level.player_spawn["spawn_y"], audio_manager)
        level.all_sprites.add(level.player)

        # Load goal data
        level.goal_data = level.level_data.get("goal", {})

        # Create platforms from JSON data
        platforms_data = level.level_data.get("platforms", [])
        for platform_data in platforms_data:
            x = platform_data.get("x", 0)
            y = platform_data.get("y", 0)
            width = platform_data.get("width", 100)
            height = platform_data.get("height", 20)
            platform_type = platform_data.get("type", "ground")
            texture = platform_data.get("texture", "grass")

            platform = Platform(x, y, width, height, platform_type, texture)
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
                enemy = Polocho(spawn_x, spawn_y, patrol_distance, audio_manager)
                level.enemies.add(enemy)
                level.all_sprites.add(enemy)

        # Create boss if present (level 5)
        boss_data = level.level_data.get("boss")
        if boss_data:
            boss_type = boss_data.get("type", "corruption_boss")
            spawn_x = boss_data.get("spawn_x", 400)
            spawn_y = boss_data.get("spawn_y", 300)

            if boss_type == "corruption_boss":
                level.boss = CorruptionBoss(spawn_x, spawn_y, audio_manager)
                level.enemies.add(level.boss)  # Add to enemies group for collision
                level.all_sprites.add(level.boss)

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

        # Create goal sprite from JSON data
        if level.goal_data:
            goal_x = level.goal_data.get("x", 0)
            goal_y = level.goal_data.get("y", 0)
            goal_width = level.goal_data.get("width", 40)
            goal_height = level.goal_data.get("height", 80)

            level.goal_sprite = Goal(goal_x, goal_y, goal_width, goal_height)
            level.goals.add(level.goal_sprite)
            level.all_sprites.add(level.goal_sprite)

        # Log loading time for performance monitoring (US-063)
        load_time = time.time() - start_time
        print(f"Level {level_number} loaded in {load_time:.3f} seconds")

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
                enemy = Polocho(spawn_x, spawn_y, patrol_distance, self.audio_manager)
                self.enemies.add(enemy)
                # Note: Don't add to all_sprites here - it's managed by reset_level()

    def reset_level(self):
        """
        Reset the entire level to initial state.
        Respawns player, enemies, powerups, and goal.
        Used when player dies and respawns.
        """
        # Clear all sprite groups
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.powerups.empty()
        self.goals.empty()

        # Reload level from stored data
        if self.level_data:
            # Recreate player (US-041: pass audio_manager)
            self.player = Player(self.player_spawn["spawn_x"], self.player_spawn["spawn_y"], self.audio_manager)
            self.all_sprites.add(self.player)

            # Recreate platforms
            platforms_data = self.level_data.get("platforms", [])
            for platform_data in platforms_data:
                x = platform_data.get("x", 0)
                y = platform_data.get("y", 0)
                width = platform_data.get("width", 100)
                height = platform_data.get("height", 20)
                platform_type = platform_data.get("type", "ground")
                texture = platform_data.get("texture", "grass")

                platform = Platform(x, y, width, height, platform_type, texture)
                self.platforms.add(platform)
                self.all_sprites.add(platform)

            # Recreate enemies
            for enemy_pos in self.initial_enemy_positions:
                enemy_type = enemy_pos.get("type", "polocho")
                spawn_x = enemy_pos.get("spawn_x", 0)
                spawn_y = enemy_pos.get("spawn_y", 0)
                patrol_distance = enemy_pos.get("patrol_distance", 150)

                if enemy_type == "polocho":
                    enemy = Polocho(spawn_x, spawn_y, patrol_distance, self.audio_manager)
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

            # Recreate goal
            if self.goal_data:
                goal_x = self.goal_data.get("x", 0)
                goal_y = self.goal_data.get("y", 0)
                goal_width = self.goal_data.get("width", 40)
                goal_height = self.goal_data.get("height", 80)

                self.goal_sprite = Goal(goal_x, goal_y, goal_width, goal_height)
                self.goals.add(self.goal_sprite)
                self.all_sprites.add(self.goal_sprite)
