# Architecture Status

## Current Project State

**Last Updated:** 2025-10-14
**Completed User Stories:** 16 / 72
**Current Phase:** Epic 3 - Power-ups and Special Abilities (In Progress)

---

## Implemented Features

### Epic 3: Power-ups and Special Abilities
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
│   └── entities/                   # Game entity classes
│       ├── __init__.py             # Entities package exports
│       ├── player.py               # Player sprite class
│       ├── platform.py             # Platform sprite class
│       ├── polocho.py              # Polocho enemy sprite class
│       └── golden_arepa.py         # Golden Arepa power-up sprite class
└── context/                         # Project context and documentation
    ├── task_execution.md           # Task execution workflow
    ├── arch_status.md              # This file - architecture status tracking
    ├── IMPLEMENTATION_PLAN.md      # Complete implementation plan with all user stories
    └── user_stories/               # Detailed user story files
        ├── epic_01_foundation/
        │   └── US-001_basic_game_window_setup.md
        ├── epic_02_enemies_combat/
        │   └── US-009_enemy_creation.md
        └── epic_03_powerups/
            └── US-016_golden_arepa_spawning.md
```

---

## Files Created/Modified

### config.py
- **Purpose:** Central configuration file for all game constants
- **Key Components:**
  - **Window Settings:** `WINDOW_WIDTH` (800), `WINDOW_HEIGHT` (600), `FPS` (60), `WINDOW_TITLE`
  - **Color Constants:** `BLACK`, `YELLOW` (Colombian yellow), `GREEN` (platform color), `RED` (Polocho enemy color), `GOLD` (Golden Arepa power-up color #FFD700)
  - **Player Physics Constants:** `PLAYER_SPEED` (5), `GRAVITY` (0.8), `TERMINAL_VELOCITY` (20), `JUMP_VELOCITY` (-15), `JUMP_CUTOFF_VELOCITY` (-3)
  - **Player Combat Constants (US-012):** `PLAYER_STARTING_LIVES` (3), `INVULNERABILITY_DURATION` (60 frames), `BLINK_INTERVAL` (5 frames), `KNOCKBACK_DISTANCE` (30 pixels), `KNOCKBACK_BOUNCE` (-5)
  - **Enemy Constants:** `ENEMY_SPEED` (2) - patrol movement speed for enemies
  - **Score Constants:** `STOMP_SCORE` (100) - points awarded for stomping an enemy
  - **Death and Respawn Constants (US-014):** `DEATH_DELAY` (120 frames / 2 seconds) - delay before respawn after death
  - **Power-up Constants (US-016):** `POWERUP_FLOAT_AMPLITUDE` (10 pixels), `POWERUP_FLOAT_SPEED` (0.1) - floating animation parameters
- **Design:** Single source of truth for all configuration values, imported by other modules

### main.py
- **Purpose:** Main game entry point - bootstraps and runs the game
- **Key Components:**
  - Imports from `config` and `src.entities` (Player, Platform, Polocho, GoldenArepa)
  - `setup_level()`: Function that creates and returns all level entities (US-014, US-016)
    - Creates player at spawn position (100, 400)
    - Creates all platforms (ground and floating platforms)
    - Stores initial enemy spawn positions in a list
    - Creates enemies at spawn positions
    - Creates three Golden Arepa power-ups at various positions (US-016)
    - Returns: (player, all_sprites, platforms, enemies, powerups, initial_enemy_positions)
  - `main()`: Main game function containing initialization and game loop
- **Key Features:**
  - Pygame initialization
  - Display surface creation
  - FPS control with pygame.time.Clock()
  - Event handling (QUIT and ESC key)
  - Player and platform creation
  - Enemy creation (three Polocho enemies at different positions)
  - Sprite group management (all_sprites, platforms, enemies)
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
  - **Pit/fall zone detection (US-015):**
    - Checks if player.rect.top > WINDOW_HEIGHT (fell below screen)
    - Player loses one life immediately when falling into pit
    - If lives remain: player respawns at spawn position (100, 400)
    - Velocity and grounded state reset on pit respawn
    - If no lives remain: triggers death state (handled by US-014)
    - Placeholder for fall death sound effect
  - **Death and respawn system (US-014):**
    - is_dead boolean flag tracks death state
    - death_timer counts frames during death delay
    - When is_dead is True, gameplay updates are paused
    - death_timer increments each frame when dead
    - After DEATH_DELAY frames (120 / 2 seconds), respawn occurs:
      - Calls setup_level() to recreate all entities
      - Resets score to 0
      - Resets is_dead to False and death_timer to 0
    - Death detection: when player.lives <= 0, set is_dead = True
    - Placeholder for death and respawn sound effects
  - **HUD rendering:**
    - Score displayed at top-left (10, 10)
    - Lives displayed below score (10, 50)
  - Game loop with update and render for player and enemies
  - Clean shutdown with pygame.quit()

### src/entities/player.py
- **Purpose:** Player character entity
- **Key Components:**
  - `Player`: Sprite class for the player character (Sancho)
- **Player Class:**
  - Extends pygame.sprite.Sprite
  - Properties: width (40), height (60), image, rect, velocity_y, is_grounded, lives, is_invulnerable, invulnerability_timer, blink_timer, visible, original_image
  - Positioned using x, y coordinates
  - Yellow colored rectangle placeholder
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

### src/__init__.py & src/entities/__init__.py
- **Purpose:** Package initialization files
- **Features:**
  - Marks directories as Python packages
  - `src/entities/__init__.py` exports Player, Platform, Polocho, and GoldenArepa for easy importing
  - Enables clean imports: `from src.entities import Player, Platform, Polocho, GoldenArepa`

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

**Current Epic:** Epic 3 - Power-ups and Special Abilities (In Progress)
**Next User Story:** US-017 - Powerup Collection
- Implement collision detection for power-ups
- Path: `context/user_stories/epic_03_powerups/US-017_powerup_collection.md`

**Completed in Epic 3:**
- US-016 - Golden Arepa Spawning ✓

**Dependencies:** US-016 is complete

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
- **Epic 3 In Progress:** Golden Arepa power-ups now spawn in the level
  - **Golden Arepa spawning fully functional (US-016):**
    - Three golden arepas float at different positions
    - 30x30 golden square sprites with distinct appearance
    - Smooth sine wave floating animation
    - Multiple power-ups can exist simultaneously
    - Ready for collection system (US-017)
- Next: US-017 (Powerup Collection)
- Pygame must be installed: `pip install pygame`
