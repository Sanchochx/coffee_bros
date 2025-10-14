# US-014: Death and Respawn

**As a** player
**I want** to respawn at the start when I die
**So that** I can retry the level

## Acceptance Criteria
- [x] Death occurs when lives reach 0
- [x] Player respawns at level start position
- [x] Lives reset to starting amount (3)
- [x] All enemies respawn in original positions
- [x] All collected powerups respawn
- [x] Brief death animation plays before respawn

## Technical Notes
- Store initial spawn positions for all entities
- Reset level state on death
- Add 1-2 second delay before respawn
