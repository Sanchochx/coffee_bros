# US-017: Powerup Collection

**As a** player
**I want** to collect the Golden Arepa by touching it
**So that** I gain its power

## Acceptance Criteria
- [x] Walking into powerup collects it
- [x] Powerup disappears when collected
- [x] Collection sound effect plays
- [x] Visual effect shows collection (sparkle/flash)
- [x] Player enters powered-up state immediately
- [x] Score increases when powerup collected

## Technical Notes
- Check collision between player and powerup sprites
- Remove powerup from sprite group on collection
- Call player's `collect_powerup()` method
