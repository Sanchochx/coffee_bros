# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Coffee Bros** is a complete 2D platformer game built with Python and Pygame 2.5.0, inspired by Super Mario Bros with Colombian cultural themes. Players guide Coffee through 5 levels from Coffee Hills to El Pico del Café, featuring enemies, power-ups, and a boss fight.

## Project Structure

```
coffee_bros/
├── main.py                      # Main game entry point and game loop
├── config.py                    # All game constants and configuration values
├── build.py                     # PyInstaller build script for executables
├── requirements.txt             # Python dependencies (pygame>=2.5.0)
├── README.md                    # User-facing game documentation
├── BUILD_INSTRUCTIONS.md        # Quick build guide for distribution
├── DISTRIBUTION_GUIDE.md        # Comprehensive distribution manual
├── CROSS_PLATFORM_TESTING.md   # Cross-platform testing checklist
├── settings.json                # User settings (volumes, etc.)
├── .gitignore                   # Git ignore patterns
│
├── src/                         # Source code modules
│   ├── __init__.py
│   ├── menu.py                  # Main menu, pause menu, settings menu
│   ├── level.py                 # Level class and level loading system
│   ├── audio_manager.py         # Sound effects and music management
│   ├── save_manager.py          # Save/load game progress
│   ├── settings_manager.py      # Settings persistence
│   ├── performance_monitor.py   # FPS and performance tracking (F3)
│   ├── optimization.py          # Performance optimization utilities
│   ├── draw_utils.py            # Drawing utility functions
│   │
│   └── entities/                # Game entity classes
│       ├── __init__.py
│       ├── player.py            # Player character (Coffee)
│       ├── enemy.py             # Basic enemy (Polocho)
│       ├── boss.py              # Final boss enemy
│       ├── powerup.py           # Golden Arepa power-up
│       ├── platform.py          # Platform/ground tiles
│       ├── goal.py              # Level end goal (castle)
│       ├── laser.py             # Laser projectile
│       ├── particle.py          # Particle effects system
│       └── level_name_display.py # Level intro screen
│
├── assets/                      # Game assets
│   ├── images/                  # Sprites and backgrounds
│   │   ├── coffee_hills.png     # Level 1 background
│   │   ├── mountain_paths.png   # Level 2 background
│   │   ├── bean_valley.png      # Level 3 background
│   │   ├── harvest_heights.png  # Level 4 background
│   │   ├── el_pico_del_cafe.png # Level 5 background
│   │   └── heart.png            # Life/heart icon
│   │
│   ├── tiles/                   # Platform tile graphics
│   │   ├── grass_left.png
│   │   ├── grass_middle.png
│   │   ├── grass_right.png
│   │   ├── stone_left.png
│   │   ├── stone_middle.png
│   │   └── stone_right.png
│   │
│   ├── sounds/                  # Sound effects
│   │   ├── jump.wav
│   │   ├── stomp.wav
│   │   ├── laser.wav
│   │   ├── powerup.wav
│   │   ├── death.wav
│   │   └── complete.wav
│   │
│   └── music/                   # Background music
│       ├── menu_music.wav
│       ├── gameplay_music.wav
│       └── victory_music.wav
│
├── tools/                       # Asset generation scripts
│   ├── generate_heart.py
│   ├── generate_tiles.py
│   ├── test_platform_tiles.py
│   └── generate_*.py            # Various asset generators
│
├── tests/                       # Test files
│   ├── test_collision_detection.py
│   ├── test_collision_simple.py
│   ├── test_edge_cases.py
│   ├── test_level_completability.py
│   └── LEVEL_COMPLETABILITY_TESTING_REPORT.md
│
└── context/                     # Project documentation
    ├── IMPLEMENTATION_PLAN.md
    ├── task_execution.md
    └── user_stories/            # Epics and user stories
        ├── epic_01_foundation/
        ├── epic_02_enemies_combat/
        ├── epic_03_powerups/
        ├── epic_04_level_system/
        ├── epic_05_ui_hud/
        ├── epic_06_camera/
        ├── epic_07_audio/
        ├── epic_08_visual_polish/
        ├── epic_09_settings/
        ├── epic_10_testing/
        └── epic_11_documentation/
```

## Architecture

### Game Flow
1. **main.py** - Entry point, contains main game loop
2. **Menu System** (src/menu.py) - Main menu, pause, settings, game over screens
3. **Level System** (src/level.py) - Loads level data, manages entities, handles game state
4. **Entity System** (src/entities/) - Player, enemies, power-ups, projectiles
5. **Audio System** (src/audio_manager.py) - Sound effects and music playback
6. **Save System** (src/save_manager.py) - Progress persistence

### Key Systems

**Entity Hierarchy:**
- All entities have position, size, velocity, and collision detection
- Player: Controlled character with movement, jumping, shooting, lives
- Enemy: Patrol-based movement with collision damage
- Boss: Enhanced enemy with multiple lives for final level
- Powerup: Collectible that grants temporary laser shooting ability
- Platform: Static collidable surfaces
- Goal: Level completion trigger
- Laser: Player projectile when powered up
- Particle: Visual effects for actions

**Level Data:**
Levels are defined in main.py with:
- Level number and name
- Platform positions and sizes
- Enemy spawn positions
- Powerup locations
- Goal position
- Tile type (grass/stone)

**Collision System:**
- Rectangle-based AABB collision detection
- Player can stomp enemies from above
- Side/front collision causes damage
- Platform collision for standing/jumping
- Goal collision triggers level completion

**State Management:**
- Game states: MENU, PLAYING, PAUSED, GAME_OVER, LEVEL_COMPLETE, VICTORY
- Player states: Normal, powered-up, invulnerable (after damage)
- Save state: Current level, score, lives

## Development Commands

### Running the Game
```bash
python main.py
```

### Building Executable
```bash
python build.py
```
Creates standalone executable in `dist/` folder.

### Running Tests
```bash
# Collision detection tests
python tests/test_collision_detection.py
python tests/test_collision_simple.py

# Edge case tests
python tests/test_edge_cases.py

# Level completability tests
python tests/test_level_completability.py
```

### Generating Assets
```bash
# Platform tiles
python tools/generate_tiles.py

# Heart icon
python tools/generate_heart.py

# Test tiles
python tools/test_platform_tiles.py
```

## Key Conventions

### Code Style
- **Docstrings:** All classes and functions have comprehensive docstrings
- **Type hints:** Not used (vanilla Python for simplicity)
- **Constants:** Defined in config.py in UPPER_CASE
- **Classes:** PascalCase (Player, Enemy, Level)
- **Functions/Methods:** snake_case
- **Private methods:** Prefix with underscore (_method_name)

### Game Constants
All tunable values are in `config.py`:
- Window size: 800x600
- FPS: 60
- Physics: GRAVITY=0.8, JUMP_VELOCITY=-18
- Player: PLAYER_SPEED=5, PLAYER_STARTING_LIVES=3
- Combat: STOMP_SCORE=100, POWERUP_SCORE=200
- Power-ups: POWERUP_DURATION=600 frames (10 seconds)
- Lasers: LASER_SPEED=10, MAX_LASERS=5

### Coordinate System
- Origin (0,0) is top-left corner
- X increases rightward
- Y increases downward
- Gravity is positive Y acceleration

### Asset Paths
- Use relative paths from project root
- Format: `assets/category/filename.ext`
- Example: `assets/sounds/jump.wav`

### Audio System
- Sound effects: Load once, play on demand
- Music: Loops continuously, one track at a time
- Volume: 0.0 to 1.0, saved in settings.json

### Save System
- Auto-save on level completion
- Stores: current_level, score, lives
- File: savegame.json in project root

### Debug Features
- F3: Toggle performance overlay (FPS, entity count, memory)
- DEBUG_START_LEVEL in config.py: Start at specific level (1-5)

## Important Notes for Development

1. **Main Game Loop**: Located in main.py, handles state machine and delegates to menus/levels
2. **Level Loading**: Levels defined as dictionaries in main.py, loaded by Level class
3. **Collision Detection**: Check player vs enemies, platforms, goals, powerups each frame
4. **Performance**: Optimized for 60 FPS, particle system has limits, entity pooling
5. **Cross-Platform**: Tested on Windows, macOS, Linux (see CROSS_PLATFORM_TESTING.md)

## Common Tasks

### Adding a New Level
1. Define level data dictionary in main.py
2. Add background image to assets/images/
3. Update LEVELS list in main.py
4. Test level completability

### Adding a New Enemy Type
1. Create enemy class in src/entities/ (inherit from Enemy)
2. Add spawn logic in Level class
3. Update collision detection if needed
4. Add sound effects if needed

### Modifying Game Balance
1. Edit constants in config.py
2. Test gameplay feel
3. Run completability tests to ensure levels are still beatable

### Adding New Sound Effects
1. Generate or create .wav file
2. Place in assets/sounds/
3. Load in AudioManager (src/audio_manager.py)
4. Call audio_manager.play_sound() at appropriate time

## Testing Approach

- **Unit Tests:** Collision detection, edge cases
- **Integration Tests:** Level completability
- **Manual Testing:** Gameplay feel, balance, fun factor
- **Performance Testing:** FPS monitoring, memory usage
- **Cross-Platform:** Windows, macOS, Linux builds

## Distribution

See BUILD_INSTRUCTIONS.md and DISTRIBUTION_GUIDE.md for:
- Creating executables with PyInstaller
- Platform-specific considerations
- Dependency bundling
- Testing distribution packages
