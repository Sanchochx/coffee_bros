# Architecture Status

## Current Project State

**Last Updated:** 2025-10-14
**Completed User Stories:** 24 / 72
**Current Phase:** Epic 4 - Level System and Progression (In Progress - 40%)

---

## Implemented Features

### Epic 4: Level System and Progression
- **US-024: Level 1 - Coffee Hills (Tutorial)** ✓
  - First playable level designed as tutorial to introduce game mechanics
  - Level implemented using existing level_1.json file (created in US-021)
  - Level adjusted to match tutorial requirements (reduced complexity)
  - **Level specifications:**
    - Width: 3200 pixels (scrolling level)
    - Height: 600 pixels (standard viewport height)
    - Name: "Coffee Hills"
    - Description: "Tutorial level introducing basic mechanics"
    - Background type: coffee_hills with sky blue background color (135, 206, 235)
  - **Player spawn:** (100, 400) - left side of level for natural left-to-right progression
  - **Goal location:** (3000, 400) - right side of level, 50x80 pixel flag
  - **Platform layout (13 platforms):**
    - Ground platforms at y=550 spanning most of the level (with gaps for pits)
    - Floating platforms at various heights (200-450) for jumping practice
    - Simple platform layouts designed for learning jumping mechanics
    - Platforms positioned to create clear progression path
  - **Enemy configuration (5 Polochos):**
    - Enemy 1: (600, 500) with 150px patrol - early enemy on ground
    - Enemy 2: (1100, 350) with 100px patrol - floating platform enemy
    - Enemy 3: (1600, 500) with 120px patrol - mid-level ground enemy
    - Enemy 4: (2300, 400) with 120px patrol - late-game challenge
    - Enemy 5: (2700, 500) with 150px patrol - final obstacle before goal
    - Easy patrol patterns (100-150 pixels) suitable for tutorial
    - Low enemy density to avoid overwhelming new players
  - **Power-up placement (1 Golden Arepa):**
    - Single Golden Arepa at (250, 400) - early in level
    - Positioned early so player learns shooting mechanic quickly
    - Placed on ground level for easy collection
    - Introduces powered-up state and laser shooting early in gameplay
  - **Pit/danger zones (2 pits):**
    - Pit 1: x=1200, 100px wide - introduces danger of falling
    - Pit 2: x=1900, 100px wide - reinforces pit awareness
    - At least one small pit to teach players to be careful
    - Pits positioned to require jumping but not overly difficult
  - **Level design philosophy:**
    - Gradually introduces mechanics from left to right
    - Early powerup teaches shooting before encountering many enemies
    - Simple jumping challenges before more complex platforming
    - Low enemy density keeps tutorial accessible
    - Designed to be completable in 1-2 minutes
    - Serves as introduction to all core mechanics before harder levels
  - **Colombian highlands theme:**
    - Background type set to "coffee_hills"
    - Sky blue background color (RGB: 135, 206, 235)
    - Music track: "coffee_hills_theme" (placeholder for Epic 7)
    - Visual theme represents Colombian coffee-growing regions
  - **Integration with game systems:**
    - Loaded via Level.load_from_file(1) in main.py
    - All entities created from JSON data (US-021, US-022)
    - Goal triggers level completion (US-023)
    - Ready for camera system implementation (Epic 6)
    - Background graphics will be added in Epic 8
  - **Testing and validation:**
    - Level JSON validates correctly with all required fields
    - All 5 enemies spawn and patrol correctly
    - Single power-up spawns and is collectible
    - Pits function as death zones
    - Goal triggers level completion
    - Level is playable and completable

- **US-023: Level Goal/Completion** ✓
  - Goal sprite class created in `src/entities/goal.py` for level completion
  - Goal extends pygame.sprite.Sprite with standard size (40x80 pixels)
  - Bright green colored rectangle (GOAL_COLOR #00C800) for visibility
  - Goal positioned using x (center) and y (bottom) coordinates
  - Customizable width and height via constructor parameters
  - **Level integration:**
    - Level class loads goal from JSON goal_data (x, y, width, height)
    - Goal sprite created in Level.load_from_file() and added to goals sprite group
    - Goal recreated during Level.reset_level() for consistency
    - Reference stored in level.goal_sprite for easy access
  - **Collision detection in main.py:**
    - Player-goal collision checked each frame using rect.colliderect()
    - Collision triggers level completion state (is_level_complete = True)
    - Completion only triggers once per level (prevents multiple triggers)
    - Time tracking: records completion_time from level start
    - Placeholder for level complete sound/music (audio in Epic 7)
  - **Level completion state:**
    - is_level_complete boolean flag tracks completion state
    - completion_timer counts frames during completion screen display
    - completion_time stores time taken in seconds (calculated from pygame.time.get_ticks())
    - LEVEL_COMPLETE_DELAY constant: 180 frames (3 seconds) before next level
    - Game state management: completion, death, and normal gameplay states
    - Completion state pauses normal gameplay (no entity updates)
  - **Completion screen rendering:**
    - Semi-transparent black overlay (alpha 180) over game view
    - Large "LEVEL COMPLETE!" text in bright green centered at top third
    - Final score displayed in medium font, centered
    - Completion time displayed with 1 decimal precision (e.g., "15.3s")
    - All completion text centered horizontally on screen
    - Completion screen appears immediately upon touching goal
    - Maintains visual feedback while showing statistics
  - **Future progression system:**
    - After LEVEL_COMPLETE_DELAY, will load next level (US-024+)
    - Currently displays completion screen indefinitely
    - Ready for level progression system implementation
  - **Constants added to config.py:**
    - GOAL_COLOR: (0, 200, 0) - bright green for goal visibility
    - LEVEL_COMPLETE_DELAY: 180 frames (3 seconds) - delay before next level
  - **Goal entity features:**
    - Simple rectangular sprite (placeholder for flag/door graphic in Epic 8)
    - No update() method needed (static entity)
    - Visually distinct from other game entities
  - **Design benefits:**
    - Clean level completion flow with visual feedback
    - Score and time tracking for player performance
    - Proper state management prevents bugs
    - Easy to extend for level progression
    - Completion screen provides sense of achievement

- **US-022: Level Loading System** ✓
  - Level class created in `src/level.py` for loading and managing levels
  - `Level.load_from_file(level_number)` class method loads levels from JSON
  - Level loading system features:
    - Constructs file path from level number (e.g., 1 → `assets/levels/level_1.json`)
    - Loads and parses JSON using Python's json module
    - Comprehensive validation of level data structure
    - Error handling for missing files and malformed JSON
  - Level validation checks:
    - Verifies required fields: metadata, player, platforms
    - Validates metadata contains name and level_number
    - Validates player spawn has spawn_x and spawn_y
    - Ensures at least one platform exists
    - Raises FileNotFoundError or ValueError with descriptive messages
  - Entity creation from JSON:
    - **Platforms:** Creates Platform instances from platforms array (x, y, width, height)
    - **Enemies:** Creates Polocho instances from enemies array (type, spawn_x, spawn_y, patrol_distance)
    - **Powerups:** Creates GoldenArepa instances from powerups array (type, x, y)
    - **Player:** Creates Player at spawn position from player object
  - Sprite group management:
    - Level class manages all sprite groups (all_sprites, platforms, enemies, powerups)
    - Entities automatically added to appropriate groups during loading
    - Easy access to all game entities through level object
  - Level properties stored:
    - metadata: Level information (name, dimensions, background, music)
    - player_spawn: Spawn position with spawn_x and spawn_y
    - goal: Level completion trigger data
    - level_data: Complete JSON data stored for level resets
    - initial_enemy_positions: Enemy spawn data stored for respawning
  - Helper methods:
    - `respawn_player()`: Respawns player at original spawn position, resets velocity
    - `respawn_all_enemies()`: Clears and recreates all enemies at initial positions
    - `reset_level()`: Completely resets level to initial state (for death/respawn)
  - Level reset functionality:
    - Clears all sprite groups completely
    - Recreates all entities from stored level_data
    - Maintains original spawn positions and configurations
    - Used when player dies to provide fresh start
  - main.py integration:
    - Replaced hardcoded setup_level() function with Level.load_from_file(1)
    - Error handling wraps level loading with try-except
    - Clean error messages displayed if level fails to load
    - Game exits gracefully if level cannot be loaded
    - References to level entities extracted for compatibility (player, all_sprites, etc.)
    - Death/respawn system updated to use level.reset_level()
    - Pit respawn updated to use level.respawn_player()
  - Future-proof design:
    - Supports any level number (1, 2, 3, etc.)
    - Can easily add new entity types by extending loading logic
    - JSON format defined in US-021 fully supported
    - Ready for level progression system (US-023)
  - Benefits:
    - Levels are data-driven (no code changes needed for new levels)
    - Easy to create and modify levels using JSON
    - Centralized level management reduces code duplication
    - Clean separation between level data and game logic
    - Proper error handling prevents crashes from bad data

- **US-021: Level Data Format** ✓
  - Level data stored in JSON format in `assets/levels/` directory
  - Comprehensive JSON structure includes all game entities:
    - **metadata**: Level name, number, description, dimensions (width/height), background info, music track
    - **player**: Spawn position (spawn_x, spawn_y)
    - **goal**: Level completion area (x, y, width, height, type)
    - **platforms**: Array of platform objects (x, y, width, height, type, texture)
    - **enemies**: Array of enemy spawn points (type, spawn_x, spawn_y, patrol_distance)
    - **powerups**: Array of power-up locations (type, x, y)
    - **pits**: Array of death zones (x, y, width, height, type)
  - Example level file created: `level_1.json` (Coffee Hills tutorial level)
  - Comprehensive format specification documented in `level_format_spec.md`
  - Specification includes:
    - Detailed field descriptions with types and requirements
    - Example JSON snippets for each section
    - Python code examples for loading and parsing levels
    - Validation rules for required vs optional fields
    - Level design guidelines (platform spacing, enemy placement, etc.)
    - Future enhancement considerations
  - JSON format supports multiple entity types:
    - Platform types: ground, floating
    - Enemy types: polocho (with patrol behavior)
    - Power-up types: golden_arepa
    - Pit types: fall_zone, lava, spikes
  - Format designed for easy level creation and modification
  - Uses Python's json module for loading (to be implemented in US-022)
  - Validation system planned for missing/malformed JSON
  - Level 1 example features:
    - 3200x600 pixel scrolling level
    - 13 platforms (ground and floating)
    - 6 Polocho enemies with varied patrol distances
    - 5 Golden Arepa power-ups
    - 2 pit/fall zones
    - Player spawn at (100, 400)
    - Goal flag at (3000, 400)

### Epic 3: Power-ups and Special Abilities
- **US-020: Laser-Enemy Collision** ✓
  - Laser-enemy collision detection implemented using pygame.sprite.spritecollide()
  - Collision checked each frame between all lasers and all enemies
  - Laser hitting enemy destroys the enemy (enemy.squash() called)
  - Laser disappears after hitting enemy (laser.kill() removes from sprite groups)
  - Enemy enters squashed state (same animation as stomp mechanic)
  - Score increases by STOMP_SCORE (100 points) when enemy defeated by laser
  - One laser can only hit one enemy (break after first collision)
  - Squashed enemies are skipped (is_squashed flag check prevents double-collision)
  - Collision detection happens after laser movement updates
  - Uses pygame.sprite.spritecollide() for efficient collision detection
  - Placeholder for enemy defeat sound effect (audio in Epic 7)
  - Placeholder for explosion particle effect at impact point (visual polish in Epic 8)
  - Laser defeat awards same points as stomp defeat (consistent scoring)

- **US-019: Laser Shooting Mechanic** ✓
  - Laser class created extending pygame.sprite.Sprite
  - 20x6 pixel cyan rectangle projectiles (CYAN color #00FFFF)
  - Shooting triggered by pressing X or J key
  - Player can only shoot when powered up (is_powered_up flag check)
  - Player tracks facing direction (1 = right, -1 = left)
  - Facing direction updated automatically during movement
  - Lasers travel horizontally at 10 pixels/frame (LASER_SPEED)
  - Lasers spawn from player's center position (rect.centerx, rect.centery)
  - Shooting cooldown system: 0.5 seconds (30 frames at 60 FPS)
  - Player.shoot_cooldown tracks frames until can shoot again
  - Player.can_shoot() method checks if shooting is allowed
  - Player.shoot() method handles laser firing logic
  - Maximum 5 active lasers at once (MAX_LASERS constant)
  - Lasers stored in dedicated sprite group
  - Lasers automatically removed when leaving screen (x < 0 or x > WINDOW_WIDTH)
  - Laser.update() handles movement and off-screen cleanup via kill()
  - Lasers cleared on player death/respawn
  - Placeholder for laser shoot sound effect (audio in Epic 7)
  - KEYDOWN event handling for shooting (not continuous input)

- **US-018: Powered-Up State** ✓
  - Player appearance changes when powered up (golden 3-pixel border)
  - Powerup timer displayed on HUD showing remaining time in seconds
  - Timer appears as "Powerup: X.Xs" in gold text below lives display
  - Powered-up state lasts exactly 10 seconds (600 frames at 60 FPS)
  - State automatically expires when timer reaches 0
  - Visual warning when powerup about to expire (last 3 seconds = 180 frames)
  - Flash effect: golden border flashes on/off every 10 frames during warning period
  - Player returns to normal yellow appearance after powerup expires
  - Timer display disappears when powerup expires
  - Flash warning helps player anticipate end of powered-up state
  - Timer displayed in gold color (255, 215, 0) to match powerup theme
  - Smooth countdown with decimal precision (e.g., "9.5s", "3.2s", "0.1s")

- **US-017: Powerup Collection** ✓
  - Collision detection between player and power-ups implemented
  - Walking into a Golden Arepa collects it automatically
  - Power-up disappears when collected (removed from sprite groups via kill())
  - Player enters powered-up state immediately upon collection
  - Player.is_powered_up flag tracks powered-up state
  - Player.powerup_timer tracks remaining powered-up time
  - POWERUP_DURATION constant set to 600 frames (10 seconds at 60 FPS)
  - Visual feedback: golden border (3-pixel width) added to player sprite when powered up
  - _update_appearance() helper method manages player visual state changes
  - Golden border automatically removed when powerup timer expires
  - Score increases by POWERUP_SCORE (200 points) when power-up collected
  - Player.collect_powerup() method handles power-up collection logic
  - Placeholder added for collection sound effect (audio in Epic 7)
  - Placeholder added for collection particle effect (visual polish in Epic 8)
  - Powerup timer counts down each frame when powered up
  - Powered-up state persists for full duration regardless of damage
  - Multiple power-ups can be collected sequentially (timer resets to full duration)

- **US-016: Golden Arepa Spawning** ✓
  - GoldenArepa class created extending pygame.sprite.Sprite
  - 30x30 pixel golden square sprites (GOLD color #FFD700)
  - Three Golden Arepas spawn at different positions in the level
  - Floating animation using sine wave motion (math.sin)
  - Float amplitude of 10 pixels up and down from base position
  - Float speed controlled by POWERUP_FLOAT_SPEED constant (0.1)
  - Smooth continuous floating animation via float_timer increment
  - Power-ups stored in dedicated powerups sprite group
  - Multiple power-ups can exist simultaneously in a level
  - Power-ups rendered with all sprites via all_sprites group
  - Distinct golden appearance makes them easily identifiable
  - 30x30 size makes them more noticeable than player (40x60) or enemies (40x40)

### Epic 2: Enemies and Combat
- **US-015: Pit/Fall Zones** ✓
  - Pit detection when player falls below screen bottom (y > WINDOW_HEIGHT)
  - Player loses one life when falling into pit
  - Immediate pit death (no delay)
  - Player respawns at spawn position (100, 400) if lives remain
  - Velocity and grounded state reset on respawn
  - If no lives remain, triggers death state (US-014)
  - Placeholder for fall death sound effect (audio in Epic 7)
  - Pit zones can be defined in level data (currently uses screen bottom)
  - Future: Can define specific pit rectangles for mid-level pits

- **US-014: Death and Respawn** ✓
  - Death occurs when lives reach 0 (replaces game exit from US-013)
  - is_dead boolean flag tracks death state
  - death_timer counts frames during death delay
  - Brief death animation delay (2 seconds / 120 frames) before respawn
  - Player respawns at original spawn position (100, 400)
  - Lives reset to PLAYER_STARTING_LIVES (3) on respawn
  - All enemies respawn in original positions
  - Enemy spawn positions stored in initial_enemy_positions list
  - setup_level() function creates and returns all level entities
  - Score resets to 0 on respawn
  - All sprite groups recreated on respawn (fresh level state)
  - Game continues running after death (no longer exits like in US-013)
  - Placeholder for death sound effect (audio in Epic 7)
  - Placeholder for respawn sound effect (audio in Epic 7)
  - Death state pauses gameplay updates (player and enemies don't update)
  - Note: Pit/fall death will be implemented in US-015

- **US-013: Lives System** ✓
  - Player starts with 3 lives (PLAYER_STARTING_LIVES constant)
  - Lives tracked in player.lives attribute
  - Lives displayed on HUD below score at position (10, 50)
  - Lives decrease when player takes damage from enemies
  - Game over logic: game ends when lives reach 0
  - Lives persist throughout the level attempt
  - Lives system integrates with damage system (US-012)
  - Note: Pit/fall death (decreasing lives when falling off map) will be implemented in US-015

- **US-012: Enemy Collision Damage** ✓
  - Side collision with enemy damages player
  - Bottom collision (hitting enemy from below) damages player
  - Player loses one life when damaged
  - 1-second invulnerability period (60 frames) after taking damage
  - Visual blinking effect during invulnerability (toggles every 5 frames)
  - Invulnerability prevents further damage during its duration
  - Knockback effect pushes player 30 pixels away from enemy
  - Small upward bounce on hit (velocity_y = -5)
  - Knockback direction determined by player's position relative to enemy
  - Lives displayed on HUD below score
  - Placeholder added for damage sound effect (audio in Epic 7)
  - Proper distinction between stomp (from above) and damage collisions

- **US-011: Enemy Stomp Mechanic** ✓
  - Collision detection for player jumping on enemies from above
  - Player must be falling (velocity_y > 0) to stomp
  - Check if player's bottom hits enemy's top half (below enemy's centery)
  - Enemy enters "squashed" state before disappearing
  - Squashed state displays flattened appearance (1/3 original height)
  - Squashed animation lasts 15 frames (~0.25 seconds at 60 FPS)
  - Enemy removed from game after squash animation completes
  - Player bounces upward after stomping (velocity_y = -8)
  - Score tracking system implemented
  - Score increases by 100 points (STOMP_SCORE) per enemy defeated
  - Score displayed in top-left corner as white text
  - Placeholder added for stomp sound effect (audio in Epic 7)
  - Enemy cannot damage player during stomp (prevents double collision)

- **US-010: Enemy Patrol Movement** ✓
  - Automatic left/right patrol movement at 2 pixels/frame
  - Configurable patrol boundaries (patrol_start and patrol_end)
  - Default patrol distance of 150 pixels (75 each direction from spawn)
  - Direction reversal when reaching patrol boundaries
  - Edge detection prevents enemies from walking off platforms
  - Look-ahead system checks for ground 5 pixels ahead
  - Wall collision detection with automatic direction reversal
  - Side collision handling for horizontal platform walls
  - Consistent movement speed using ENEMY_SPEED constant
  - Enemies patrol continuously within their boundaries

- **US-009: Enemy Creation (Polocho)** ✓
  - Polocho class extending pygame.sprite.Sprite
  - 40x40 pixel red rectangle sprites for enemies
  - Enemies spawn at defined positions in the level
  - Three enemy instances created at different locations
  - Enemies affected by gravity (same physics as player)
  - Terminal velocity cap prevents unrealistic falling
  - Platform collision detection for enemies
  - Enemies stored in dedicated sprite group
  - RED color constant (#DC143C) for enemy visibility

### Epic 1: Foundation
- **US-001: Basic Game Window Setup** ✓
  - Pygame initialization and main game loop
  - 800x600 window with "Sancho Bros" title
  - 60 FPS game loop with Clock control
  - Event handling for window close (X button and ESC key)
  - Black background rendering

- **US-002: Player Character Creation** ✓
  - Player class extending pygame.sprite.Sprite
  - 40x60 pixel yellow rectangle sprite (placeholder)
  - Initial spawn position at (x=100, y=400)
  - Sprite rendering using pygame sprite groups
  - Colombian yellow color (#FFD100) for visibility

- **US-003: Basic Player Movement** ✓
  - Horizontal movement controls (LEFT/A and RIGHT/D keys)
  - Movement speed of 5 pixels per frame
  - Continuous input handling using pygame.key.get_pressed()
  - Screen boundary collision detection (prevents off-screen movement)
  - Instant direction changes with no momentum
  - Smooth and responsive movement at 60 FPS

- **US-004: Gravity System** ✓
  - Gravity acceleration of 0.8 pixels/frame²
  - Terminal velocity cap at 20 pixels/frame downward
  - velocity_y variable for vertical velocity tracking
  - Continuous gravity application during gameplay
  - Smooth falling motion without jittering
  - Player falls naturally when in air

- **US-005: Jumping Mechanics** ✓
  - Jump input detection (UP arrow, W key, SPACE bar)
  - Initial jump velocity of -15 pixels/frame (upward)
  - is_grounded state tracking to prevent double-jumping
  - Variable jump height based on button hold duration
  - Jump cutoff velocity of -3 pixels/frame for short hops
  - Simple ground collision at y=500 (temporary until platforms)
  - Responsive and natural jump feel
  - Can only jump when touching ground

- **US-006: Platform Creation** ✓
  - Platform class extending pygame.sprite.Sprite
  - Platforms with defined position and size (x, y, width, height)
  - Green colored platforms (#228B22) for visual distinction
  - Ground platform at bottom of screen (full width, y=550)
  - Four floating platforms at various heights and positions:
    - Platform 1: (200, 450) - 150x20 pixels
    - Platform 2: (400, 350) - 120x20 pixels
    - Platform 3: (550, 250) - 180x20 pixels
    - Platform 4: (100, 200) - 100x20 pixels
  - Platforms stored in dedicated sprite group
  - Static platforms that don't move
  - Platforms rendered with all sprites

- **US-007: Platform Collision Detection** ✓
  - AABB (Axis-Aligned Bounding Box) collision detection using pygame's rect.colliderect()
  - Separate collision checks for horizontal and vertical axes
  - **Vertical collision handling:**
    - Landing on top: Player bottom aligned with platform top, velocity set to 0, is_grounded set to True
    - Hitting from below: Player top aligned with platform bottom, upward velocity stopped
  - **Horizontal collision handling:**
    - Side collision detection prevents passing through platforms horizontally
    - Uses center position comparison to determine which side was hit
  - Player can walk along platform surfaces smoothly
  - Player cannot pass through platforms from any direction
  - Precise collision with no gaps or overlapping
  - Ground state correctly tracked for jumping

- **US-008: Project Structure Setup** ✓
  - Proper modular code organization implemented
  - `src/` directory contains all game modules
  - `src/entities/` directory for game entity classes
  - `config.py` contains all game constants (window, colors, physics)
  - `main.py` serves as clean entry point with imports
  - Each class in its own file (player.py, platform.py)
  - `__init__.py` files in src/ and src/entities/ for proper package structure
  - Consistent naming conventions (snake_case for modules, PascalCase for classes)
  - Clean separation of concerns: configuration, entities, and game loop
  - Uses absolute imports from config and src.entities

---

## File Structure

```
sancho_bros/
├── main.py                          # Main game entry point - imports and runs game
├── config.py                        # All game constants and configuration
├── CLAUDE.md                        # Project documentation for Claude Code
├── src/                            # Source code package
│   ├── __init__.py                 # Package initialization
│   ├── level.py                    # Level loading and management system (US-022, US-023)
│   └── entities/                   # Game entity classes
│       ├── __init__.py             # Entities package exports
│       ├── player.py               # Player sprite class
│       ├── platform.py             # Platform sprite class
│       ├── polocho.py              # Polocho enemy sprite class
│       ├── golden_arepa.py         # Golden Arepa power-up sprite class
│       ├── laser.py                # Laser projectile sprite class
│       └── goal.py                 # Goal sprite class (US-023)
├── assets/                         # Game assets and data
│   └── levels/                     # Level data files (US-021)
│       ├── level_1.json            # Level 1: Coffee Hills data
│       └── level_format_spec.md    # JSON format specification
└── context/                         # Project context and documentation
    ├── task_execution.md           # Task execution workflow
    ├── arch_status.md              # This file - architecture status tracking
    ├── IMPLEMENTATION_PLAN.md      # Complete implementation plan with all user stories
    └── user_stories/               # Detailed user story files
        ├── epic_01_foundation/
        │   └── US-001_basic_game_window_setup.md
        ├── epic_02_enemies_combat/
        │   └── US-009_enemy_creation.md
        ├── epic_03_powerups/
        │   └── US-016_golden_arepa_spawning.md
        └── epic_04_level_system/
            └── US-021_level_data_format.md
```

---

## Files Created/Modified

### config.py
- **Purpose:** Central configuration file for all game constants
- **Key Components:**
  - **Window Settings:** `WINDOW_WIDTH` (800), `WINDOW_HEIGHT` (600), `FPS` (60), `WINDOW_TITLE`
  - **Color Constants:** `BLACK`, `YELLOW` (Colombian yellow), `GREEN` (platform color), `RED` (Polocho enemy color), `GOLD` (Golden Arepa power-up color #FFD700), `CYAN` (Laser projectile color #00FFFF)
  - **Player Physics Constants:** `PLAYER_SPEED` (5), `GRAVITY` (0.8), `TERMINAL_VELOCITY` (20), `JUMP_VELOCITY` (-15), `JUMP_CUTOFF_VELOCITY` (-3)
  - **Player Combat Constants (US-012):** `PLAYER_STARTING_LIVES` (3), `INVULNERABILITY_DURATION` (60 frames), `BLINK_INTERVAL` (5 frames), `KNOCKBACK_DISTANCE` (30 pixels), `KNOCKBACK_BOUNCE` (-5)
  - **Enemy Constants:** `ENEMY_SPEED` (2) - patrol movement speed for enemies
  - **Score Constants:** `STOMP_SCORE` (100) - points awarded for stomping an enemy, `POWERUP_SCORE` (200) - points awarded for collecting a power-up
  - **Death and Respawn Constants (US-014):** `DEATH_DELAY` (120 frames / 2 seconds) - delay before respawn after death
  - **Power-up Constants (US-016, US-017):** `POWERUP_FLOAT_AMPLITUDE` (10 pixels), `POWERUP_FLOAT_SPEED` (0.1) - floating animation parameters, `POWERUP_DURATION` (600 frames / 10 seconds) - how long powered-up state lasts
  - **Laser Constants (US-019):** `LASER_SPEED` (10 pixels/frame) - horizontal laser travel speed, `LASER_COOLDOWN` (30 frames / 0.5 seconds) - time between shots, `MAX_LASERS` (5) - maximum active lasers, `LASER_WIDTH` (20), `LASER_HEIGHT` (6)
  - **Goal Constants (US-023):** `GOAL_COLOR` (0, 200, 0) - bright green for goal visibility, `LEVEL_COMPLETE_DELAY` (180 frames / 3 seconds) - delay before next level loads
- **Design:** Single source of truth for all configuration values, imported by other modules

### src/level.py
- **Purpose:** Level loading and management system
- **Key Components:**
  - `Level`: Class that loads and manages level data from JSON files
- **Level Class:**
  - Properties: metadata, player_spawn, goal_data, platforms, enemies, powerups, goals, all_sprites, player, goal_sprite, initial_enemy_positions, level_data
  - **__init__()**: Initializes empty level with default spawn position and empty sprite groups
  - **load_from_file(level_number)**: Class method that loads level from JSON file
    - Takes level number as parameter (e.g., 1 for level_1.json)
    - Constructs file path to assets/levels/level_{number}.json
    - Opens and parses JSON file using json.load()
    - Calls _validate_level_data() to ensure data integrity
    - Creates all game entities from JSON data:
      - Player at spawn_x, spawn_y position
      - Platforms from platforms array
      - Enemies (Polocho) from enemies array with patrol_distance
      - Powerups (GoldenArepa) from powerups array
      - Goal from goal_data (x, y, width, height) - US-023
    - Stores initial_enemy_positions for respawning
    - Adds all entities to appropriate sprite groups
    - Returns fully initialized Level instance
    - Raises FileNotFoundError if level file doesn't exist
    - Raises ValueError if JSON is malformed or missing required fields
  - **_validate_level_data()**: Validates level data structure
    - Checks for required top-level fields: metadata, player, platforms
    - Validates metadata has name and level_number
    - Validates player has spawn_x and spawn_y
    - Validates platforms is an array with at least one platform
    - Raises ValueError with descriptive message for any validation failure
  - **respawn_player()**: Respawns player at original spawn position
    - Sets player rect position to player_spawn coordinates
    - Resets velocity_y to 0
    - Resets is_grounded to False
  - **respawn_all_enemies()**: Respawns all enemies at original positions
    - Clears enemies sprite group
    - Recreates enemies from initial_enemy_positions list
    - Supports different enemy types (currently only Polocho)
  - **reset_level()**: Completely resets level to initial state
    - Clears all sprite groups (all_sprites, platforms, enemies, powerups, goals)
    - Recreates player from player_spawn data
    - Recreates all platforms from level_data
    - Recreates all enemies from initial_enemy_positions
    - Recreates all powerups from level_data
    - Recreates goal from goal_data - US-023
    - Used when player dies and needs fresh level state
- **Design Features:**
  - Data-driven level design (levels defined in JSON, not code)
  - Comprehensive error handling prevents crashes
  - Extensible for new entity types
  - Stores complete level data for resets
  - Manages all sprite groups internally
  - Easy integration with main game loop

### main.py
- **Purpose:** Main game entry point - bootstraps and runs the game
- **Key Components:**
  - Imports from `config`, `src.entities` (Player, Platform, Polocho, GoldenArepa, Laser, Goal), and `src.level` (Level)
  - **Level loading (US-022):**
    - Uses `Level.load_from_file(1)` to load level 1 from JSON
    - Error handling with try-except catches FileNotFoundError and ValueError
    - Displays error message and exits gracefully if level fails to load
    - Extracts references to level entities for compatibility (player, all_sprites, platforms, enemies, powerups, goals)
  - `main()`: Main game function containing initialization and game loop
- **Key Features:**
  - Pygame initialization
  - Display surface creation
  - FPS control with pygame.time.Clock()
  - Event handling (QUIT and ESC key)
  - Player and platform creation
  - Enemy creation (three Polocho enemies at different positions)
  - Sprite group management (all_sprites, platforms, enemies, powerups, lasers)
  - Key state polling via pygame.key.get_pressed()
  - **Score tracking system (US-011):**
    - Score variable initialized to 0
    - Font initialized for rendering score text
    - Score displayed at top-left corner in white text
  - **Enemy collision detection (US-011, US-012, US-013):**
    - Checks collision between player and enemies (skips squashed enemies)
    - **Stomp detection (US-011):**
      - Validates player is falling (velocity_y > 0)
      - Validates player hits enemy from above (player.rect.bottom < enemy.rect.centery)
      - Calls enemy.squash() to trigger squash animation
      - Applies upward bounce to player (velocity_y = -8)
      - Increases score by STOMP_SCORE
      - Prevents double-counting with is_squashed check
    - **Damage detection (US-012):**
      - Side or bottom collisions trigger player damage
      - Determines knockback direction based on relative positions
      - Calls player.take_damage(knockback_direction)
      - Placeholder for damage sound effect
  - **Power-up collision detection (US-017):**
    - Checks collision between player and power-ups
    - On collision:
      - Calls player.collect_powerup() to enter powered-up state
      - Increases score by POWERUP_SCORE (200 points)
      - Removes power-up from sprite groups via kill() (disappears)
      - Placeholder for collection sound effect
      - Placeholder for collection particle effect
  - **Level completion detection (US-023):**
    - Checks collision between player and goal using rect.colliderect()
    - On collision with goal:
      - Sets is_level_complete to True (only triggers once)
      - Resets completion_timer to 0
      - Records completion_time from level start (using pygame.time.get_ticks())
      - Placeholder for level complete sound/music (audio in Epic 7)
    - After completion: waits LEVEL_COMPLETE_DELAY frames before loading next level
    - Currently displays completion screen indefinitely (level progression in US-024+)
  - **Pit/fall zone detection (US-015, updated in US-022):**
    - Checks if player.rect.top > WINDOW_HEIGHT (fell below screen)
    - Player loses one life immediately when falling into pit
    - If lives remain: calls level.respawn_player() to respawn at spawn position (US-022)
    - Velocity and grounded state reset on pit respawn
    - If no lives remain: triggers death state (handled by US-014)
    - Placeholder for fall death sound effect
  - **Death and respawn system (US-014, updated in US-022):**
    - is_dead boolean flag tracks death state
    - death_timer counts frames during death delay
    - When is_dead is True, gameplay updates are paused
    - death_timer increments each frame when dead
    - After DEATH_DELAY frames (120 / 2 seconds), respawn occurs:
      - Calls level.reset_level() to recreate all entities (US-022)
      - Refreshes references to level entities (player, all_sprites, platforms, enemies, powerups)
      - Clears all active lasers with lasers.empty()
      - Resets score to 0
      - Resets is_dead to False and death_timer to 0
    - Death detection: when player.lives <= 0, set is_dead = True
    - Placeholder for death and respawn sound effects
  - **Laser shooting system (US-019):**
    - lasers sprite group stores all active laser projectiles
    - KEYDOWN event handling for X or J key press
    - Checks if MAX_LASERS (5) limit reached before spawning
    - Calls player.shoot() which returns (x, y, direction) if successful
    - Creates Laser instance at returned position
    - Adds laser to both lasers and all_sprites groups
    - laser.update() called each frame to handle movement
    - Lasers automatically removed when leaving screen
    - Placeholder for laser shoot sound effect
  - **Laser-enemy collision detection (US-020):**
    - Checks collision between lasers and enemies each frame
    - Uses pygame.sprite.spritecollide() for collision detection
    - For each laser, checks against all enemies in the enemies group
    - On collision with non-squashed enemy:
      - Calls laser.kill() to remove laser from sprite groups
      - Calls enemy.squash() to mark enemy for destruction
      - Increases score by STOMP_SCORE (100 points)
      - Breaks inner loop (one laser hits one enemy only)
    - Placeholder for enemy defeat sound effect
    - Placeholder for explosion particle effect at impact point
  - **HUD rendering:**
    - Score displayed at top-left (10, 10)
    - Lives displayed below score (10, 50)
    - **Powerup timer display (US-018):**
      - Shows remaining powerup time when player is powered up
      - Displayed as "Powerup: X.Xs" below lives (10, 90)
      - Gold colored text (255, 215, 0) to match powerup theme
      - Converts frames to seconds with decimal precision
      - Automatically disappears when powerup expires
  - **Level completion screen (US-023):**
    - Semi-transparent black overlay (alpha 180) over game view
    - Large "LEVEL COMPLETE!" text in bright green (0, 255, 0) at top third
    - Final score displayed in medium font, centered
    - Completion time displayed with 1 decimal precision, centered
    - All text centered horizontally on screen
    - Appears immediately when player touches goal
    - Pauses normal gameplay updates
  - Game loop with update and render for player and enemies
  - Clean shutdown with pygame.quit()

### src/entities/player.py
- **Purpose:** Player character entity
- **Key Components:**
  - `Player`: Sprite class for the player character (Sancho)
- **Player Class:**
  - Extends pygame.sprite.Sprite
  - Properties: width (40), height (60), image, rect, velocity_y, is_grounded, lives, is_invulnerable, invulnerability_timer, blink_timer, visible, original_image, is_powered_up, powerup_timer, facing_direction, shoot_cooldown
  - Positioned using x, y coordinates
  - Yellow colored rectangle placeholder
  - **Powered-up state properties (US-017):**
    - is_powered_up: Boolean flag indicating if player has collected a power-up
    - powerup_timer: Frames remaining of powered-up state
  - **Shooting system properties (US-019):**
    - facing_direction: Current facing direction (1 = right, -1 = left)
    - shoot_cooldown: Frames until can shoot again
  - **collect_powerup() method (US-017):** Handles power-up collection
    - Sets is_powered_up flag to True
    - Sets powerup_timer to POWERUP_DURATION (600 frames / 10 seconds)
    - Calls _update_appearance() to add golden border visual
    - Placeholder for collection sound effect
  - **_update_appearance() method (US-017):** Updates player visual state
    - Creates base yellow player sprite
    - Adds 3-pixel golden border when powered up
    - Updates original_image for blinking effect compatibility
  - **can_shoot() method (US-019):** Checks if player can shoot
    - Returns True if powered up AND cooldown is 0
    - Returns False otherwise
  - **shoot() method (US-019):** Attempts to fire a laser
    - Returns None if can't shoot (not powered up or on cooldown)
    - Starts LASER_COOLDOWN (30 frames) on successful shot
    - Returns tuple (x, y, direction) with laser spawn info
    - Placeholder for laser shoot sound effect
  - **take_damage(knockback_direction) method (US-012):** Handles player taking damage
    - Returns early if already invulnerable (prevents multiple hits)
    - Decrements lives by 1
    - Activates invulnerability for INVULNERABILITY_DURATION frames (60 frames = 1 second)
    - Applies knockback: pushes player KNOCKBACK_DISTANCE pixels away from enemy
    - Applies upward bounce with KNOCKBACK_BOUNCE velocity
    - Placeholder for damage sound effect
  - **update(keys_pressed, platforms) method:** Handles keyboard input, movement, gravity, jumping, platform collision, and invulnerability
    - **Horizontal movement and collision:**
      - Detects LEFT/A and RIGHT/D key presses for horizontal movement
      - Updates horizontal position based on PLAYER_SPEED
      - Updates facing_direction (-1 for left, 1 for right) during movement
      - Clamps horizontal position to screen boundaries
      - Checks horizontal collision with platforms and resolves side collisions
    - **Jumping:**
      - Detects UP/W/SPACE key presses for jumping (only when grounded)
      - Applies JUMP_VELOCITY when jump initiated
      - Implements variable jump height by cutting velocity early
    - **Gravity and vertical movement:**
      - Applies gravity acceleration to velocity_y each frame
      - Caps velocity_y at TERMINAL_VELOCITY
      - Updates vertical position based on velocity_y
    - **Platform collision:**
      - Checks vertical collision with all platforms
      - Landing on top: aligns player bottom with platform top, stops velocity, sets grounded
      - Hitting from below: aligns player top with platform bottom, stops upward velocity
    - **Invulnerability timer and blinking (US-012):**
      - Decrements invulnerability_timer each frame when invulnerable
      - Toggles visibility every BLINK_INTERVAL frames (5 frames)
      - When visible: displays normal sprite
      - When invisible: displays semi-transparent sprite (alpha 100)
      - Ends invulnerability and restores full visibility when timer expires
    - **Powered-up timer (US-017, US-018):**
      - Decrements powerup_timer each frame when powered up
      - **Visual warning (US-018):** When timer < 180 frames (last 3 seconds):
        - Flash effect: border appears/disappears every 10 frames
        - Alternates between normal and powered-up appearance
        - Helps player anticipate end of powerup state
      - When timer reaches 0: sets is_powered_up to False
      - Calls _update_appearance() to remove golden border visual
      - Powered-up state persists for full duration regardless of damage
    - **Shooting cooldown (US-019):**
      - Decrements shoot_cooldown by 1 each frame when > 0
      - Prevents rapid shooting by requiring cooldown to reach 0

### src/entities/platform.py
- **Purpose:** Platform entity for ground and floating platforms
- **Key Components:**
  - `Platform`: Sprite class for platforms
- **Platform Class:**
  - Extends pygame.sprite.Sprite
  - Constructor takes x, y, width, height parameters
  - Green colored rectangle using GREEN constant
  - Positioned using x, y coordinates (top-left corner)
  - Static - no update method needed as platforms don't move
  - Used to create ground and floating platforms throughout the level

### src/entities/polocho.py
- **Purpose:** Polocho enemy entity
- **Key Components:**
  - `Polocho`: Sprite class for enemy characters
- **Polocho Class:**
  - Extends pygame.sprite.Sprite
  - Properties: width (40), height (40), image, rect, velocity_y, is_grounded, patrol_start, patrol_end, direction, speed, is_squashed, squash_timer
  - Constructor takes x, y position parameters and optional patrol_distance (default 150)
  - Red colored rectangle (#DC143C) using RED constant
  - Patrol boundaries calculated as x ± patrol_distance
  - Direction: 1 for right, -1 for left
  - **Squashed state properties (US-011):**
    - is_squashed: Boolean flag indicating if enemy has been stomped
    - squash_timer: Frame counter for squashed animation duration
  - **squash() method (US-011):** Marks enemy as squashed and starts animation
    - Sets is_squashed flag to True
    - Sets squash_timer to 15 frames (~0.25 seconds)
    - Changes appearance to flattened rectangle (1/3 original height)
    - Maintains bottom position and horizontal center
  - **update(platforms) method:** Handles enemy patrol movement, physics, and collision
    - **Squash animation handling (US-011):**
      - If squashed, decrements squash_timer each frame
      - Calls self.kill() when timer reaches 0 (removes from sprite groups)
      - Returns early to prevent movement when squashed
    - **Horizontal patrol movement:**
      - Moves automatically at ENEMY_SPEED * direction pixels/frame
      - Reverses direction when reaching patrol_start or patrol_end boundaries
      - Edge detection: checks 5 pixels ahead for platform underneath
      - Turns around if no ground detected ahead (prevents falling off platforms)
      - Wall collision: detects side collisions with platforms and reverses direction
    - **Gravity and vertical movement:**
      - Applies GRAVITY acceleration to velocity_y each frame
      - Caps velocity_y at TERMINAL_VELOCITY to prevent unrealistic falling
      - Updates vertical position based on velocity_y
    - **Platform collision (vertical):**
      - Checks vertical collision with all platforms
      - Landing on top: aligns enemy bottom with platform top, stops velocity, sets grounded
      - Hitting from below: aligns enemy top with platform bottom, stops upward velocity
  - Enemies patrol continuously within their defined boundaries
  - Smart edge and wall detection prevents enemies from falling or getting stuck

### src/entities/laser.py
- **Purpose:** Laser projectile entity
- **Key Components:**
  - `Laser`: Sprite class for laser projectiles
- **Laser Class:**
  - Extends pygame.sprite.Sprite
  - Properties: width (20), height (6), image, rect, direction, speed
  - Constructor takes x, y, direction parameters
  - Cyan colored rectangle using CYAN constant (#00FFFF)
  - Positioned using x, y coordinates (center of laser)
  - direction: 1 for right, -1 for left
  - speed: LASER_SPEED (10 pixels/frame)
  - **update() method:** Handles laser movement and cleanup
    - Moves horizontally: rect.x += speed * direction
    - Checks if laser left screen (rect.right < 0 or rect.left > WINDOW_WIDTH)
    - Calls self.kill() to remove from sprite groups when off-screen
    - Automatic cleanup prevents memory leaks from projectiles
  - No physics or collision logic (collision in US-020)
  - 20x6 size makes it visible but not overwhelming

### src/entities/golden_arepa.py
- **Purpose:** Golden Arepa power-up entity
- **Key Components:**
  - `GoldenArepa`: Sprite class for collectible power-up items
- **GoldenArepa Class:**
  - Extends pygame.sprite.Sprite
  - Properties: width (30), height (30), image, rect, base_y, float_timer
  - Constructor takes x, y position parameters for center and base position
  - Golden colored square using GOLD constant (#FFD700)
  - Positioned using x, y coordinates (centered on x, y is base of float range)
  - **Floating animation:**
    - Uses sine wave (math.sin) for smooth up/down motion
    - float_timer increments by POWERUP_FLOAT_SPEED each frame
    - Float offset calculated as sin(float_timer) * POWERUP_FLOAT_AMPLITUDE
    - Results in smooth 10-pixel vertical oscillation around base_y position
    - Creates eye-catching "floating" effect typical of collectible items
  - **update() method:** Updates floating animation position
    - Increments float_timer for sine wave progression
    - Calculates new vertical position based on sine wave
    - Updates rect.centery to animate the power-up
  - No physics or collision logic - purely visual entity (collision in US-017)
  - 30x30 size makes it distinct and noticeable in the game world

### src/entities/goal.py
- **Purpose:** Goal entity for level completion
- **Key Components:**
  - `Goal`: Sprite class for level completion trigger
- **Goal Class:**
  - Extends pygame.sprite.Sprite
  - Properties: width, height, image, rect
  - Constructor takes x, y, width (default 40), height (default 80) parameters
  - Bright green colored rectangle using GOAL_COLOR constant (#00C800)
  - Positioned using x (center), y (bottom) coordinates
  - **Visual design:**
    - Default size 40x80 pixels (tall rectangular flag/door shape)
    - Bright green color for high visibility and distinction from other entities
    - Static sprite (no update method needed)
    - Placeholder for flag or door graphic (to be added in Epic 8)
  - **Collision:**
    - Collision detection handled in main.py game loop
    - Triggers level completion when player touches goal
  - **Design notes:**
    - Simple rectangular sprite for now (will be replaced with graphic in Epic 8)
    - Customizable width and height for different level goal types
    - Easy to identify visually (distinct color and shape)
    - No physics or movement logic needed (static entity)

### src/__init__.py & src/entities/__init__.py
- **Purpose:** Package initialization files
- **Features:**
  - Marks directories as Python packages
  - `src/entities/__init__.py` exports Player, Platform, Polocho, GoldenArepa, Laser, and Goal for easy importing
  - Enables clean imports: `from src.entities import Player, Platform, Polocho, GoldenArepa, Laser, Goal`

### assets/levels/level_1.json
- **Purpose:** Level 1 data definition (Coffee Hills tutorial level)
- **Key Components:**
  - **Metadata:** Level name "Coffee Hills", 3200x600 dimensions, background info
  - **Player spawn:** (100, 400) - left side of level
  - **Goal:** Flag at (3000, 400) - right side of level
  - **13 platforms:** Mix of ground platforms and floating platforms at various heights
  - **6 enemies:** Polocho enemies with varied patrol distances (100-200 pixels)
  - **5 power-ups:** Golden Arepas placed at strategic locations throughout level
  - **2 pits:** Fall zones at x=1200 and x=1900 (100 pixels wide each)
- **Design Philosophy:**
  - Tutorial level introducing basic mechanics
  - Gradually increasing difficulty from left to right
  - Power-ups reward exploration and platforming skill
  - Enemies teach combat mechanics without overwhelming player
  - Wide scrolling level (3200 pixels) for camera system (Epic 6)

### assets/levels/level_format_spec.md
- **Purpose:** Comprehensive documentation of level JSON format
- **Key Sections:**
  1. **Overview:** Introduction to level data format and file naming conventions
  2. **JSON Structure:** Root-level field specification
  3. **Field Specifications:** Detailed documentation for each field:
     - metadata: Level info (name, dimensions, background, music)
     - player: Spawn position
     - goal: Level completion trigger
     - platforms: Platform objects with position, size, type, texture
     - enemies: Enemy spawns with patrol behavior
     - powerups: Power-up locations
     - pits: Death zone definitions
  4. **Validation Rules:** Required vs optional fields
  5. **Python Loading Examples:** Code snippets for loading and parsing JSON
  6. **Entity Creation Examples:** How to instantiate game objects from data
  7. **Level Design Guidelines:** Best practices for:
     - Platform spacing (based on player jump capabilities)
     - Enemy placement and patrol distances
     - Power-up positioning for rewards
     - Pit placement for fair challenge
  8. **Level Dimensions:** Standard sizes and scrolling considerations
  9. **Future Enhancements:** Planned additions (moving platforms, new enemy types, etc.)
- **Features:**
  - Includes Python code examples for loading levels with error handling
  - Documents all current entity types (polocho, golden_arepa, etc.)
  - Provides validation examples for required fields
  - Includes versioning information for format changes

---

## Technical Decisions

### Technology Stack
- **Language:** Python
- **Game Framework:** Pygame
- **Window Resolution:** 800x600 (standard 4:3 aspect ratio)
- **Target FPS:** 60 (smooth gameplay)

### Code Organization
- **Modular structure** with proper package hierarchy (US-008)
- `config.py` - single source of truth for all configuration constants
- `src/entities/` - dedicated package for game entity classes
- Each class in its own file for maintainability
- Main game logic in main.py imports from modules
- Clean separation of concerns: config, entities, game loop
- `__init__.py` files enable clean package imports
- Consistent naming conventions: snake_case for modules, PascalCase for classes
- Absolute imports used throughout for clarity

### Sprite System
- Using pygame.sprite.Sprite as base class for game objects
- Sprite groups (pygame.sprite.Group) for batch rendering
- Player sprite uses Surface and Rect for positioning and rendering

### Physics System
- Gravity-based physics for vertical movement
- Acceleration: 0.8 pixels/frame² provides natural falling feel
- Terminal velocity: 20 pixels/frame prevents unrealistic speeds
- Velocity-based position updates for smooth motion
- Per-frame physics updates integrated with game loop

---

## Next Steps

**Epic 1 Complete!** All foundation stories (US-001 through US-008) have been completed.
**Epic 2 Complete!** All 7 stories (US-009 through US-015) have been completed!
**Epic 3 Complete!** All 5 stories (US-016 through US-020) have been completed!

**Epic 4 In Progress!** (4/10 stories completed - 40%)

**Completed in Epic 4:**
- US-021 - Level Data Format ✓
- US-022 - Level Loading System ✓
- US-023 - Level Goal/Completion ✓
- US-024 - Level 1: Coffee Hills (Tutorial) ✓

**Next User Story:** US-025 - Level 2: Mountain Paths
- Design and implement first tutorial level
- Path: `context/user_stories/epic_04_level_system/US-024_level_1_coffee_hills.md`

**Dependencies:**
- US-021 complete (level data format defined) ✓
- US-022 complete (level loading system) ✓
- US-023 complete (level goal/completion) ✓
- All foundation systems complete (US-001 through US-008) ✓

---

## Notes

- **Epic 1 (Foundation) completed successfully** - all 8 user stories done!
- **Epic 2 (Enemies and Combat) completed successfully** - all 7 user stories done!
- Project now has proper modular structure (US-008)
- Player can move left and right with keyboard controls
- Gravity system implemented - player falls naturally
- Jumping mechanics fully functional with variable jump height
- Physics feel natural with smooth acceleration and terminal velocity
- Movement is smooth and responsive with proper boundary checking
- Platform system created with ground and floating platforms
- Platforms are visually distinct with green color
- **Enemy system implemented (US-009, US-010, US-011):**
  - Polocho enemy class created
  - Enemies are 40x40 pixel red rectangles (distinct from 40x60 yellow player)
  - Three enemies spawn at different positions
  - Enemies affected by gravity and respond to platform collisions
  - Enemies stored in dedicated sprite group
  - **Patrol movement fully functional (US-010):**
    - Enemies walk back and forth automatically at 2 pixels/frame
    - Configurable patrol boundaries with default 150 pixel range
    - Smart edge detection prevents falling off platforms
    - Wall collision detection causes direction reversal
    - Consistent movement speed throughout patrol
  - **Stomp mechanic fully functional (US-011):**
    - Player can defeat enemies by jumping on them from above
    - Enemies display squashed state for 15 frames before disappearing
    - Player bounces upward after successful stomp
    - Score tracking system displays current score
    - 100 points awarded per enemy defeated
    - Placeholder added for stomp sound effect (audio in Epic 7)
  - **Damage system fully functional (US-012):**
    - Side and bottom collisions with enemies damage the player
    - Player loses one life per hit
    - 1-second invulnerability period after taking damage
    - Visual blinking effect during invulnerability
    - Knockback pushes player away from enemy
    - Lives displayed on HUD
    - Placeholder added for damage sound effect (audio in Epic 7)
  - **Lives system fully functional (US-013):**
    - Player starts with 3 lives
    - Lives displayed on HUD below score
    - Lives decrease when taking damage from enemies
    - Game over occurs when lives reach 0 (triggers death state)
    - Lives persist throughout the level attempt
    - Clean integration with damage and combat systems
  - **Death and respawn system fully functional (US-014):**
    - Death triggers when lives reach 0
    - 2-second death delay before respawn
    - Player respawns at starting position (100, 400)
    - All enemies respawn in original positions
    - Lives reset to 3 on respawn
    - Score resets to 0 on respawn
    - Level state completely resets (fresh start)
    - Game continues running after death (no exit)
  - **Pit/fall zones fully functional (US-015):**
    - Player dies when falling below screen bottom
    - Immediate pit death (no delay)
    - Player loses one life when falling into pit
    - If lives remain: respawn at spawn position with reset velocity
    - If no lives: triggers death state (US-014)
    - Placeholder for fall death sound effect
    - Future: can define specific pit rectangles for mid-level pits
- **Platform collision detection is fully functional:**
  - Player lands on and walks along platforms
  - Enemies also respond to platform collisions
  - Cannot pass through platforms from any direction
  - Precise AABB collision with separate axis checking
  - Ground state properly tracked for jumping mechanics
- **Code is well-organized:**
  - Modular structure with src/ package
  - Configuration separated into config.py
  - Each entity in its own file
  - Clean imports and package structure
- **Epic 2 Complete!** All 7 stories completed successfully!
- **Epic 3 Complete!** All 5 stories completed successfully! Power-up and laser shooting systems fully functional
  - **Laser-enemy collision fully functional (US-020):**
    - Lasers destroy enemies on contact using pygame.sprite.spritecollide()
    - Both laser and enemy disappear after collision
    - Enemy enters squashed state (same animation as stomp)
    - Score increases by 100 points per laser kill (same as stomp)
    - One laser can only hit one enemy (consistent behavior)
    - Placeholder for enemy defeat sound effect (audio in Epic 7)
    - Placeholder for explosion particle effect (visual polish in Epic 8)
  - **Laser shooting fully functional (US-019):**
    - Player can shoot lasers when powered up by pressing X or J
    - Player tracks facing direction automatically during movement
    - Lasers are 20x6 cyan rectangles that travel horizontally
    - Shooting cooldown prevents spam (0.5 seconds between shots)
    - Maximum 5 active lasers at once
    - Lasers automatically removed when leaving screen
    - Placeholder for laser shoot sound effect (audio in Epic 7)
  - **Golden Arepa spawning fully functional (US-016):**
    - Three golden arepas float at different positions
    - 30x30 golden square sprites with distinct appearance
    - Smooth sine wave floating animation
    - Multiple power-ups can exist simultaneously
  - **Powerup collection fully functional (US-017):**
    - Walking into power-ups collects them automatically
    - Power-ups disappear when collected (removed from sprite groups)
    - Player enters powered-up state for 10 seconds (600 frames)
    - Visual feedback: golden border added to player when powered up
    - Score increases by 200 points when collecting power-up
    - Powered-up state timer counts down and expires automatically
    - Multiple power-ups can be collected (timer resets each time)
    - Placeholder for collection sound effect (audio in Epic 7)
    - Placeholder for collection particle effect (visual polish in Epic 8)
  - **Powered-up state fully functional (US-018):**
    - Player appearance changes with golden border when powered up
    - Powerup timer displays on HUD showing remaining time in seconds
    - Timer appears in gold text below lives display
    - Visual warning: border flashes during last 3 seconds
    - State automatically expires after 10 seconds
    - Player returns to normal appearance after expiry
    - Timer display disappears when powerup expires
- **Epic 3 Complete!** Ready to begin Epic 4 (Level System and Progression)
- Pygame must be installed: `pip install pygame`
