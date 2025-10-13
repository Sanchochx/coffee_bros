# Architecture Status

## Current Project State

**Last Updated:** 2025-10-13
**Completed User Stories:** 7 / 72
**Current Phase:** Epic 1 - Foundation

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

---

## File Structure

```
sancho_bros/
├── main.py                          # Main game entry point with pygame window and game loop
├── CLAUDE.md                        # Project documentation for Claude Code
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

### main.py
- **Purpose:** Main game entry point
- **Key Components:**
  - `WINDOW_WIDTH`, `WINDOW_HEIGHT`: Window dimensions (800x600)
  - `FPS`: Frame rate constant (60)
  - `PLAYER_SPEED`: Movement speed constant (5 pixels/frame)
  - `GRAVITY`: Gravity acceleration constant (0.8 pixels/frame²)
  - `TERMINAL_VELOCITY`: Maximum fall speed constant (20 pixels/frame)
  - `JUMP_VELOCITY`: Initial jump velocity constant (-15 pixels/frame)
  - `JUMP_CUTOFF_VELOCITY`: Variable jump cutoff constant (-3 pixels/frame)
  - `BLACK`, `YELLOW`, `GREEN`: Color constants
  - `Player`: Sprite class for the player character
  - `Platform`: Sprite class for platforms
  - `main()`: Main game function containing initialization and game loop
- **Key Features:**
  - Pygame initialization
  - Display surface creation
  - FPS control with pygame.time.Clock()
  - Event handling (QUIT and ESC key)
  - Player sprite creation and rendering
  - Sprite group management (all_sprites)
  - Key state polling via pygame.key.get_pressed()
  - Player updates with key states passed to update()
  - Screen rendering with sprite drawing
  - Clean shutdown with pygame.quit()
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
- **Platform Class:**
  - Extends pygame.sprite.Sprite
  - Constructor takes x, y, width, height parameters
  - Green colored rectangle using GREEN constant
  - Positioned using x, y coordinates (top-left corner)
  - Static - no update method needed as platforms don't move
  - Used to create ground and floating platforms throughout the level

---

## Technical Decisions

### Technology Stack
- **Language:** Python
- **Game Framework:** Pygame
- **Window Resolution:** 800x600 (standard 4:3 aspect ratio)
- **Target FPS:** 60 (smooth gameplay)

### Code Organization
- Single main.py file for now (will be modularized as project grows)
- Constants defined at module level
- Player class defined before main() function
- Main game logic in main() function
- Clean separation of initialization, game loop, and shutdown
- Sprite groups used for organized rendering

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

**Next User Story:** US-008 - Project Structure Setup
- Organize code into proper modules and directories
- Separate concerns: entities, game logic, constants, utilities
- Create organized file structure for scalability

**Dependencies:** US-001 through US-007 are complete

---

## Notes

- Project is in initial foundation phase
- US-001 through US-007 completed successfully
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
- Ready to refactor code into proper project structure (US-008)
- Pygame must be installed: `pip install pygame`
