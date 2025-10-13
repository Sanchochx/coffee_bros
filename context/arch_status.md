# Architecture Status

## Current Project State

**Last Updated:** 2025-10-13
**Completed User Stories:** 8 / 72
**Current Phase:** Epic 1 - Foundation (Complete)

---

## Implemented Features

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
│       └── platform.py             # Platform sprite class
└── context/                         # Project context and documentation
    ├── task_execution.md           # Task execution workflow
    ├── arch_status.md              # This file - architecture status tracking
    ├── IMPLEMENTATION_PLAN.md      # Complete implementation plan with all user stories
    └── user_stories/               # Detailed user story files
        └── epic_01_foundation/
            └── US-001_basic_game_window_setup.md
```

---

## Files Created/Modified

### config.py
- **Purpose:** Central configuration file for all game constants
- **Key Components:**
  - **Window Settings:** `WINDOW_WIDTH` (800), `WINDOW_HEIGHT` (600), `FPS` (60), `WINDOW_TITLE`
  - **Color Constants:** `BLACK`, `YELLOW` (Colombian yellow), `GREEN` (platform color)
  - **Player Physics Constants:** `PLAYER_SPEED` (5), `GRAVITY` (0.8), `TERMINAL_VELOCITY` (20), `JUMP_VELOCITY` (-15), `JUMP_CUTOFF_VELOCITY` (-3)
- **Design:** Single source of truth for all configuration values, imported by other modules

### main.py
- **Purpose:** Main game entry point - bootstraps and runs the game
- **Key Components:**
  - Imports from `config` and `src.entities`
  - `main()`: Main game function containing initialization and game loop
- **Key Features:**
  - Pygame initialization
  - Display surface creation
  - FPS control with pygame.time.Clock()
  - Event handling (QUIT and ESC key)
  - Player and platform creation
  - Sprite group management (all_sprites, platforms)
  - Key state polling via pygame.key.get_pressed()
  - Game loop with update and render
  - Clean shutdown with pygame.quit()

### src/entities/player.py
- **Purpose:** Player character entity
- **Key Components:**
  - `Player`: Sprite class for the player character (Sancho)
- **Player Class:**
  - Extends pygame.sprite.Sprite
  - Properties: width (40), height (60), image, rect, velocity_y, is_grounded
  - Positioned using x, y coordinates
  - Yellow colored rectangle placeholder
  - **update(keys_pressed, platforms) method:** Handles keyboard input, movement, gravity, jumping, and platform collision
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

### src/__init__.py & src/entities/__init__.py
- **Purpose:** Package initialization files
- **Features:**
  - Marks directories as Python packages
  - `src/entities/__init__.py` exports Player and Platform for easy importing
  - Enables clean imports: `from src.entities import Player, Platform`

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

**Next Epic:** Epic 2 - Enemies and Combat
**Next User Story:** US-009 - Enemy Creation (Polocho)
- Create Polocho enemy sprites with basic properties
- Path: `context/user_stories/epic_02_enemies_combat/US-009_enemy_creation.md`

**Dependencies:** Epic 1 (Foundation) is complete

---

## Notes

- **Epic 1 (Foundation) completed successfully** - all 8 user stories done!
- Project now has proper modular structure (US-008)
- Player can move left and right with keyboard controls
- Gravity system implemented - player falls naturally
- Jumping mechanics fully functional with variable jump height
- Physics feel natural with smooth acceleration and terminal velocity
- Movement is smooth and responsive with proper boundary checking
- Platform system created with ground and floating platforms
- Platforms are visually distinct with green color
- **Platform collision detection is fully functional:**
  - Player lands on and walks along platforms
  - Cannot pass through platforms from any direction
  - Precise AABB collision with separate axis checking
  - Ground state properly tracked for jumping mechanics
- **Code is well-organized:**
  - Modular structure with src/ package
  - Configuration separated into config.py
  - Each entity in its own file
  - Clean imports and package structure
- Ready to begin Epic 2 (Enemies and Combat)
- Pygame must be installed: `pip install pygame`
