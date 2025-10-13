# US-022: Level Loading System

**As a** developer
**I want** to load levels from JSON files
**So that** the game can create levels dynamically

## Acceptance Criteria
- [ ] Level class can load JSON file by level number
- [ ] All platforms are created from JSON data
- [ ] All enemies are spawned from JSON data
- [ ] All powerups are placed from JSON data
- [ ] Player spawns at correct position
- [ ] Loading errors are caught and reported

## Technical Notes
- Create Level class with `load_from_file()` method
- Parse JSON and instantiate game objects
- Store objects in appropriate sprite groups
