# US-017: Powerup Collection

**As a** player
**I want** to collect the Golden Arepa by touching it
**So that** I gain its power

## Acceptance Criteria
- [ ] Walking into powerup collects it
- [ ] Powerup disappears when collected
- [ ] Collection sound effect plays
- [ ] Visual effect shows collection (sparkle/flash)
- [ ] Player enters powered-up state immediately
- [ ] Score increases when powerup collected

## Technical Notes
- Check collision between player and powerup sprites
- Remove powerup from sprite group on collection
- Call player's `collect_powerup()` method
