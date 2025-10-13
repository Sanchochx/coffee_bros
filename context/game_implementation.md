# SANCHO BROS - GAME IMPLEMENTATION PLAN

## Table of Contents
1. [Technical Overview](#technical-overview)
2. [Project Structure](#project-structure)
3. [Core Game Systems](#core-game-systems)
4. [Implementation Phases](#implementation-phases)
5. [Asset Requirements](#asset-requirements)
6. [Class Architecture](#class-architecture)
7. [Level Design System](#level-design-system)
8. [Controls and Input](#controls-and-input)
9. [Testing Strategy](#testing-strategy)

---

## Technical Overview

**Technology Stack:**
- **Language:** Python 3.8+
- **Game Engine:** Pygame 2.5+
- **Graphics:** 2D sprite-based platformer
- **Resolution:** 800x600 pixels (scalable)
- **Target FPS:** 60 FPS

**Game Genre:** 2D Side-scrolling Platformer (Mario-style)

---

## Project Structure

```
sancho_bros/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── README.md              # Project documentation
├── config.py              # Game configuration constants
│
├── src/
│   ├── __init__.py
│   ├── game.py            # Main game loop and state management
│   ├── player.py          # Sancho (player character)
│   ├── enemy.py           # Polocho enemy class
│   ├── powerup.py         # La Arepa Dorada powerup
│   ├── projectile.py      # Laser beam implementation
│   ├── level.py           # Level loading and management
│   ├── platform.py        # Platform/block objects
│   ├── camera.py          # Camera/viewport management
│   ├── collision.py       # Collision detection system
│   ├── physics.py         # Physics engine (gravity, movement)
│   ├── ui.py              # HUD, menus, score display
│   └── audio.py           # Sound effects and music manager
│
├── assets/
│   ├── images/
│   │   ├── sancho/        # Player sprites (idle, walk, jump, shoot)
│   │   ├── polocho/       # Enemy sprites (walk, squashed)
│   │   ├── powerups/      # Golden Arepa sprite
│   │   ├── tiles/         # Platform and block sprites
│   │   ├── backgrounds/   # Level backgrounds (Colombian highlands)
│   │   └── ui/            # Menu elements, hearts, score
│   │
│   ├── sounds/
│   │   ├── jump.wav
│   │   ├── stomp.wav
│   │   ├── shoot.wav
│   │   ├── powerup.wav
│   │   ├── death.wav
│   │   └── level_complete.wav
│   │
│   ├── music/
│   │   ├── menu_theme.ogg
│   │   └── level_theme.ogg
│   │
│   └── levels/
│       ├── level_1.json
│       ├── level_2.json
│       ├── level_3.json
│       ├── level_4.json
│       └── level_5.json
│
└── tests/
    ├── test_player.py
    ├── test_collision.py
    └── test_physics.py
```

---

## Core Game Systems

### 1. Physics System
- **Gravity:** Constant downward acceleration (0.8 pixels/frame²)
- **Jump Mechanics:**
  - Initial jump velocity: -15 pixels/frame
  - Variable jump height (release early = lower jump)
  - Terminal velocity: 20 pixels/frame
- **Movement:**
  - Horizontal speed: 5 pixels/frame
  - Acceleration/deceleration for smooth movement

### 2. Collision Detection
- **AABB (Axis-Aligned Bounding Box)** collision
- Collision layers:
  - Player vs. Platforms (solid blocks)
  - Player vs. Enemies (damage or stomp)
  - Player vs. Pits (death)
  - Player vs. Powerups (collection)
  - Projectiles vs. Enemies (elimination)

### 3. State Management
Game states:
- `MENU` - Main menu
- `PLAYING` - Active gameplay
- `PAUSED` - Pause menu
- `LEVEL_COMPLETE` - Level transition
- `GAME_OVER` - Death screen
- `VICTORY` - Game completed

### 4. Camera System
- Follows player horizontally
- Scrolls when player moves past screen center
- Stays within level boundaries
- Smooth camera movement

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
**Goal:** Basic game engine and player movement

**Tasks:**
1. Set up project structure and virtual environment
2. Install Pygame and create main game loop
3. Implement basic window and FPS control
4. Create Player class with keyboard input
5. Implement basic physics (gravity, jumping)
6. Add collision detection with ground
7. Create simple test level with platforms

**Deliverables:**
- Player can move left/right and jump
- Basic collision with platforms works
- Game runs at 60 FPS

### Phase 2: Core Gameplay (Week 2)
**Goal:** Enemies, combat, and death mechanics

**Tasks:**
1. Implement Enemy (Polocho) class
   - Walking AI (patrol between points)
   - Animation states
2. Add stomp mechanic (jump on enemy head)
3. Implement damage system (collision kills player)
4. Create death and respawn system
5. Add basic UI (lives, score)
6. Implement pit/fall zones

**Deliverables:**
- Enemies walk and can be stomped
- Player dies on touch or falling
- Lives system functional

### Phase 3: Power-ups and Combat (Week 3)
**Goal:** Golden Arepa and laser shooting

**Tasks:**
1. Create PowerUp class (La Arepa Dorada)
2. Implement power-up collection
3. Add player powered-up state (timer)
4. Create Projectile class (laser beams)
5. Implement shooting mechanics
6. Add projectile-enemy collision
7. Create visual effects for powered state

**Deliverables:**
- Power-up spawns and can be collected
- Player can shoot laser beams
- Enemies are destroyed by lasers
- Power-up expires after time limit

### Phase 4: Level System (Week 4)
**Goal:** 5 complete levels with progression

**Tasks:**
1. Create level data format (JSON)
2. Implement level loading system
3. Design and create 5 levels:
   - Level 1: Tutorial (easy)
   - Level 2: Platform jumping focus
   - Level 3: Enemy-heavy
   - Level 4: Precision platforming
   - Level 5: Final challenge (all mechanics)
4. Add level completion detection (reach goal)
5. Implement level transition screens
6. Add victory screen

**Deliverables:**
- 5 playable levels
- Level progression system
- Win condition

### Phase 5: Polish and Assets (Week 5)
**Goal:** Graphics, sound, and game feel

**Tasks:**
1. Create/source all sprite assets
   - Sancho animations (idle, walk, jump, shoot)
   - Polocho animations (walk, squashed)
   - Platform tiles
   - Background images
   - UI elements
2. Add sound effects for all actions
3. Implement background music
4. Add particle effects (death, stomp, powerup)
5. Create main menu
6. Add pause functionality
7. Implement settings (volume, controls)

**Deliverables:**
- Complete visual and audio experience
- Polished game feel
- Menu system

### Phase 6: Testing and Balancing (Week 6)
**Goal:** Bug-free, balanced gameplay

**Tasks:**
1. Write unit tests for core systems
2. Playtest all levels
3. Balance difficulty curve
4. Fix bugs and edge cases
5. Optimize performance
6. Add game instructions/tutorial
7. Create README and documentation

**Deliverables:**
- Stable, bug-free game
- Balanced difficulty
- Complete documentation

---

## Class Architecture

### Player Class (`src/player.py`)
```python
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Position and velocity
        # Animation state
        # Health/lives
        # Powered-up state

    def update(self, platforms, enemies, powerups):
        # Handle input
        # Apply physics
        # Check collisions
        # Update animation

    def jump(self):
        # Jump logic

    def shoot(self):
        # Create projectile

    def take_damage(self):
        # Handle being hit

    def collect_powerup(self, powerup):
        # Activate powered state
```

### Enemy Class (`src/enemy.py`)
```python
class Polocho(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_start, patrol_end):
        # Position and velocity
        # Patrol boundaries
        # Animation state

    def update(self, platforms):
        # Patrol movement
        # Collision detection
        # Update animation

    def get_stomped(self):
        # Death animation and removal
```

### PowerUp Class (`src/powerup.py`)
```python
class GoldenArepa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Position
        # Animation (floating, glowing)

    def update(self):
        # Animate

    def collect(self):
        # Trigger effect and remove
```

### Level Class (`src/level.py`)
```python
class Level:
    def __init__(self, level_number):
        # Load level data
        # Create platforms, enemies, powerups
        # Set spawn point and goal

    def update(self):
        # Update all entities

    def draw(self, screen, camera):
        # Render level

    def is_complete(self, player):
        # Check if player reached goal
```

### Game Class (`src/game.py`)
```python
class Game:
    def __init__(self):
        # Initialize pygame
        # Load assets
        # Create game objects
        # Set initial state

    def run(self):
        # Main game loop

    def handle_events(self):
        # Process input

    def update(self):
        # Update game state

    def draw(self):
        # Render everything
```

---

## Level Design System

### Level Data Format (JSON)
```json
{
    "level_number": 1,
    "name": "Coffee Hills",
    "width": 3200,
    "height": 600,
    "background": "highlands_1.png",
    "music": "level_theme.ogg",

    "player_spawn": {"x": 100, "y": 400},
    "goal": {"x": 3000, "y": 400},

    "platforms": [
        {"x": 0, "y": 550, "width": 800, "height": 50, "type": "ground"},
        {"x": 200, "y": 450, "width": 100, "height": 20, "type": "floating"},
        {"x": 350, "y": 400, "width": 100, "height": 20, "type": "floating"}
    ],

    "enemies": [
        {"type": "polocho", "x": 400, "y": 530, "patrol_start": 300, "patrol_end": 500},
        {"type": "polocho", "x": 600, "y": 530, "patrol_start": 550, "patrol_end": 700}
    ],

    "powerups": [
        {"type": "golden_arepa", "x": 500, "y": 400}
    ],

    "pits": [
        {"x": 800, "width": 100}
    ]
}
```

### Level Progression Design

**Level 1: Coffee Hills (Tutorial)**
- Length: Medium (3200px)
- Enemies: 5 Polochos (easy patterns)
- Powerups: 1 Golden Arepa (early introduction)
- Difficulty: Easy
- Focus: Basic movement and jumping

**Level 2: Mountain Paths**
- Length: Medium-Long (4000px)
- Enemies: 8 Polochos
- Powerups: 2 Golden Arepas
- Difficulty: Easy-Medium
- Focus: Platform precision jumping

**Level 3: Bean Valley**
- Length: Long (4800px)
- Enemies: 12 Polochos (closer together)
- Powerups: 2 Golden Arepas
- Difficulty: Medium
- Focus: Enemy combat and timing

**Level 4: Harvest Heights**
- Length: Long (5000px)
- Enemies: 15 Polochos (complex patterns)
- Powerups: 3 Golden Arepas
- Difficulty: Medium-Hard
- Focus: Combining platforming and combat

**Level 5: El Pico del Café (Final Level)**
- Length: Very Long (6000px)
- Enemies: 20 Polochos (challenging placement)
- Powerups: 3 Golden Arepas
- Difficulty: Hard
- Focus: Mastery of all mechanics

---

## Controls and Input

### Keyboard Controls
- **Arrow Keys / WASD:** Movement
  - Left/A: Move left
  - Right/D: Move right
  - Up/W or Space: Jump
- **X or J:** Shoot laser (when powered up)
- **ESC:** Pause menu
- **Enter:** Confirm/Select in menus

### Controller Support (Optional Enhancement)
- Left Stick: Movement
- A Button: Jump
- X Button: Shoot
- Start: Pause

---

## Asset Requirements

### Graphics Specifications
- **Art Style:** Pixel art or cartoon style
- **Tile Size:** 50x50 pixels
- **Sprite Size:** Player 40x60px, Enemies 40x40px
- **Animation Frames:**
  - Sancho: Idle (4), Walk (6), Jump (2), Shoot (4)
  - Polocho: Walk (4), Squashed (1)
  - Golden Arepa: Glow (6 frames)

### Color Palette (Colombian Theme)
- Primary: Yellow (#FFD700) - Gold/Arepa
- Secondary: Brown (#8B4513) - Coffee
- Accent: Green (#228B22) - Highlands
- Background: Sky blue (#87CEEB), Mountain gray (#696969)

### Sound Effects Needed
1. **Jump** - Whoosh sound
2. **Stomp** - Squish/pop sound
3. **Shoot** - Laser zap
4. **Powerup Collection** - Magical chime
5. **Death** - Descending tone
6. **Level Complete** - Victory fanfare
7. **Menu Select** - Click/beep

### Music
- Upbeat Colombian-inspired chiptune music
- Main menu theme (looping)
- Level theme (looping, energetic)

---

## Testing Strategy

### Unit Tests
- `test_player.py`: Movement, jumping, shooting, collision
- `test_physics.py`: Gravity, velocity, acceleration
- `test_collision.py`: AABB detection, response
- `test_level.py`: Level loading, entity creation

### Integration Tests
- Player-enemy interactions (stomp vs. damage)
- Powerup collection and effects
- Level completion detection
- Score/lives system

### Playtesting Checklist
- [ ] All levels are completable
- [ ] No soft-lock situations
- [ ] Controls feel responsive
- [ ] Difficulty curve is smooth
- [ ] No game-breaking bugs
- [ ] Performance is stable (60 FPS)
- [ ] Audio levels are balanced

---

## Configuration Constants (`config.py`)

```python
# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Sancho Bros"

# Physics
GRAVITY = 0.8
TERMINAL_VELOCITY = 20
JUMP_VELOCITY = -15
PLAYER_SPEED = 5

# Game settings
STARTING_LIVES = 3
POWERUP_DURATION = 10  # seconds
LASER_SPEED = 10
LASER_DAMAGE = 1

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SKY_BLUE = (135, 206, 235)
```

---

## Dependencies (`requirements.txt`)

```
pygame>=2.5.0
```

---

## Development Timeline

| Phase | Duration | Completion Target |
|-------|----------|-------------------|
| Phase 1: Foundation | 1 week | Week 1 |
| Phase 2: Core Gameplay | 1 week | Week 2 |
| Phase 3: Power-ups | 1 week | Week 3 |
| Phase 4: Level System | 1 week | Week 4 |
| Phase 5: Polish | 1 week | Week 5 |
| Phase 6: Testing | 1 week | Week 6 |

**Total Development Time:** 6 weeks

---

## Next Steps

1. **Set up development environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install pygame
   ```

2. **Start with Phase 1:** Create basic project structure and implement player movement

3. **Iterate rapidly:** Get something playable as soon as possible, then refine

4. **Test frequently:** Playtest after each major feature addition

5. **Stay flexible:** Adjust design based on what feels fun during development

---

## Additional Features (Post-Launch)

If time permits, consider adding:
- High score system (persistent storage)
- Additional powerups (speed boost, invincibility)
- Boss fight in final level
- Secret areas and collectibles
- Multiple difficulty modes
- Leaderboard
- Level editor

---

**¡Vamos a crear un juego increíble!**
