# Level Data Format Specification

## Overview

This document describes the JSON format used for defining levels in Coffee Bros. All level files are stored in the `assets/levels/` directory with the naming convention `level_X.json` where X is the level number.

---

## JSON Structure

### Root Level Fields

```json
{
  "metadata": { ... },
  "player": { ... },
  "goal": { ... },
  "platforms": [ ... ],
  "enemies": [ ... ],
  "powerups": [ ... ],
  "pits": [ ... ]
}
```

---

## Field Specifications

### 1. Metadata (Required)

Contains level information and configuration.

```json
"metadata": {
  "name": "string",              // Display name of the level
  "level_number": integer,       // Level number (1-5)
  "description": "string",       // Brief description of the level
  "width": integer,              // Level width in pixels
  "height": integer,             // Level height in pixels (typically 600)
  "background_type": "string",   // Background theme identifier
  "background_color": [r, g, b], // RGB values for background color (0-255)
  "music_track": "string"        // Identifier for background music
}
```

**Example:**
```json
"metadata": {
  "name": "Coffee Hills",
  "level_number": 1,
  "description": "Tutorial level introducing basic mechanics",
  "width": 3200,
  "height": 600,
  "background_type": "coffee_hills",
  "background_color": [135, 206, 235],
  "music_track": "coffee_hills_theme"
}
```

---

### 2. Player (Required)

Defines the player's starting position.

```json
"player": {
  "spawn_x": integer,  // X coordinate of spawn position
  "spawn_y": integer   // Y coordinate of spawn position
}
```

**Example:**
```json
"player": {
  "spawn_x": 100,
  "spawn_y": 400
}
```

**Notes:**
- spawn_x and spawn_y represent the top-left corner of the player sprite
- Player dimensions are 40x60 pixels (defined in Player class)

---

### 3. Goal (Required)

Defines the level completion trigger area.

```json
"goal": {
  "x": integer,        // X coordinate of goal position
  "y": integer,        // Y coordinate of goal position
  "width": integer,    // Width of goal collision area
  "height": integer,   // Height of goal collision area
  "type": "string"     // Goal type (e.g., "flag", "door", "portal")
}
```

**Example:**
```json
"goal": {
  "x": 3000,
  "y": 400,
  "width": 50,
  "height": 80,
  "type": "flag"
}
```

**Notes:**
- When player collides with goal area, level is completed
- Type determines visual representation (to be implemented in Epic 8)

---

### 4. Platforms (Required Array)

Defines all platform objects in the level.

```json
"platforms": [
  {
    "x": integer,          // X coordinate (top-left corner)
    "y": integer,          // Y coordinate (top-left corner)
    "width": integer,      // Platform width in pixels
    "height": integer,     // Platform height in pixels
    "type": "string",      // Platform type ("ground" or "floating")
    "texture": "string"    // Texture identifier (e.g., "grass", "stone")
  }
]
```

**Example:**
```json
"platforms": [
  {
    "x": 0,
    "y": 550,
    "width": 800,
    "height": 50,
    "type": "ground",
    "texture": "grass"
  },
  {
    "x": 200,
    "y": 450,
    "width": 150,
    "height": 20,
    "type": "floating",
    "texture": "stone"
  }
]
```

**Platform Types:**
- `ground`: Main ground platforms (typically thicker, at bottom of level)
- `floating`: Floating platforms in mid-air

**Common Textures:**
- `grass`: Green grass texture
- `stone`: Stone/rock texture
- `wood`: Wooden plank texture
- `metal`: Metal platform texture

**Notes:**
- Platforms are solid objects that players and enemies can stand on
- Collision detection prevents passing through from all sides
- At least one platform should exist at ground level

---

### 5. Enemies (Required Array)

Defines all enemy spawn points and patrol behavior.

```json
"enemies": [
  {
    "type": "string",           // Enemy type (currently only "polocho")
    "spawn_x": integer,         // X coordinate of spawn position
    "spawn_y": integer,         // Y coordinate of spawn position
    "patrol_distance": integer  // Distance to patrol from spawn (optional, default: 150)
  }
]
```

**Example:**
```json
"enemies": [
  {
    "type": "polocho",
    "spawn_x": 300,
    "spawn_y": 400,
    "patrol_distance": 150
  },
  {
    "type": "polocho",
    "spawn_x": 600,
    "spawn_y": 500,
    "patrol_distance": 200
  }
]
```

**Enemy Types:**
- `polocho`: Basic walking enemy (40x40 red square)

**Notes:**
- Enemies patrol left/right within patrol_distance from spawn point
- Enemies automatically turn around at patrol boundaries and platform edges
- spawn_x and spawn_y represent the top-left corner of enemy sprite
- Enemies are affected by gravity and collide with platforms

---

### 6. Powerups (Required Array)

Defines all power-up spawn locations.

```json
"powerups": [
  {
    "type": "string",  // Power-up type (currently only "golden_arepa")
    "x": integer,      // X coordinate (center of power-up)
    "y": integer       // Y coordinate (base Y for floating animation)
  }
]
```

**Example:**
```json
"powerups": [
  {
    "type": "golden_arepa",
    "x": 250,
    "y": 400
  },
  {
    "type": "golden_arepa",
    "x": 650,
    "y": 200
  }
]
```

**Power-up Types:**
- `golden_arepa`: Golden power-up that grants shooting ability (30x30 golden square)

**Notes:**
- Power-ups have floating animation (sine wave, ±10 pixels vertical)
- x and y represent the center position of the power-up
- When collected, power-up disappears and player gains abilities for 10 seconds
- Player can shoot lasers while powered up

---

### 7. Pits (Optional Array)

Defines death zones (areas where player dies instantly).

```json
"pits": [
  {
    "x": integer,       // X coordinate (top-left corner)
    "y": integer,       // Y coordinate (top-left corner)
    "width": integer,   // Width of pit area
    "height": integer,  // Height of pit area
    "type": "string"    // Pit type (e.g., "fall_zone", "lava", "spikes")
  }
]
```

**Example:**
```json
"pits": [
  {
    "x": 1200,
    "y": 0,
    "width": 100,
    "height": 600,
    "type": "fall_zone"
  }
]
```

**Pit Types:**
- `fall_zone`: Empty gaps where player falls to death
- `lava`: Lava pit (instant death on contact)
- `spikes`: Spike pit (instant death on contact)

**Notes:**
- When player enters pit area, they lose one life
- If lives remain, player respawns at spawn point
- If no lives remain, death state is triggered
- Pits are typically gaps between platforms or hazard areas

---

## Validation Rules

When loading a level file, the following fields are **required**:

1. **metadata**: Must include name, level_number, width, height
2. **player**: Must include spawn_x and spawn_y
3. **goal**: Must include x, y, width, height
4. **platforms**: Must be an array (can be empty, but not recommended)
5. **enemies**: Must be an array (can be empty)
6. **powerups**: Must be an array (can be empty)

**Optional fields:**
- **pits**: If omitted, only falling below screen bottom triggers death

---

## Loading Levels in Python

Use Python's `json` module to load level data:

```python
import json

def load_level(level_number):
    """Load level data from JSON file."""
    file_path = f"assets/levels/level_{level_number}.json"

    try:
        with open(file_path, 'r') as file:
            level_data = json.load(file)

        # Validate required fields
        required_fields = ['metadata', 'player', 'goal', 'platforms', 'enemies', 'powerups']
        for field in required_fields:
            if field not in level_data:
                raise ValueError(f"Missing required field: {field}")

        return level_data

    except FileNotFoundError:
        print(f"Error: Level file not found: {file_path}")
        return None

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in level file: {e}")
        return None

    except ValueError as e:
        print(f"Error: {e}")
        return None
```

---

## Example: Creating Entities from Level Data

```python
# Load level data
level_data = load_level(1)

# Create player
player = Player(
    level_data['player']['spawn_x'],
    level_data['player']['spawn_y']
)

# Create platforms
platforms = pygame.sprite.Group()
for platform_data in level_data['platforms']:
    platform = Platform(
        platform_data['x'],
        platform_data['y'],
        platform_data['width'],
        platform_data['height']
    )
    platforms.add(platform)

# Create enemies
enemies = pygame.sprite.Group()
for enemy_data in level_data['enemies']:
    if enemy_data['type'] == 'polocho':
        enemy = Polocho(
            enemy_data['spawn_x'],
            enemy_data['spawn_y'],
            enemy_data.get('patrol_distance', 150)  # Default to 150 if not specified
        )
        enemies.add(enemy)

# Create power-ups
powerups = pygame.sprite.Group()
for powerup_data in level_data['powerups']:
    if powerup_data['type'] == 'golden_arepa':
        powerup = GoldenArepa(
            powerup_data['x'],
            powerup_data['y']
        )
        powerups.add(powerup)
```

---

## Level Design Guidelines

### Platform Placement
- Ensure platforms are spaced so player can reach them with jumps
- Player jump height: approximately 200 pixels vertically
- Player jump distance: approximately 150-200 pixels horizontally
- Provide safe landing spots after difficult jumps

### Enemy Placement
- Don't place enemies directly on player spawn point
- Space enemies to allow player to learn attack patterns
- Consider patrol_distance to avoid blocking critical paths
- Place enemies on platforms with enough room to patrol

### Power-up Placement
- Place power-ups in challenging but reachable locations
- Reward exploration and skillful platforming
- Consider power-up duration (10 seconds) when spacing them out
- Use power-ups to teach shooting mechanics

### Pit Placement
- Clearly indicate pit locations (visual cues to be added in Epic 8)
- Don't place pits immediately after spawn
- Allow room for recovery before pit edges
- Pits add challenge but shouldn't feel unfair

---

## Level Dimensions

**Current Window:** 800x600 pixels
**Typical Level Width:** 2000-4000 pixels (scrolling camera in Epic 6)
**Level Height:** 600 pixels (matches window height)

---

## Future Enhancements

The following features may be added in future epics:

- **Moving platforms** (position, movement pattern, speed)
- **Different enemy types** (flying, shooting, etc.)
- **Collectible items** (coins, stars)
- **Environmental hazards** (moving spikes, fire jets)
- **Checkpoints** (respawn points within level)
- **Locked doors and keys**
- **Boss encounters**

---

## Version History

- **v1.0** (2025-10-14): Initial format specification for US-021
  - Defined metadata, player, goal, platforms, enemies, powerups, pits
  - Support for Polocho enemies and Golden Arepa power-ups
