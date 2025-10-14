# US-013: Lives System

**As a** player
**I want** to have multiple lives
**So that** I have multiple chances to complete the level

## Acceptance Criteria
- [x] Player starts with 3 lives
- [x] Current lives are displayed on screen (HUD)
- [x] Lives decrease when player takes damage
- [ ] Lives decrease when player falls in pit (will be implemented in US-015)
- [x] Game over occurs when lives reach 0
- [x] Lives persist within the same level attempt

## Technical Notes
- Store lives count in player or game state
- Display lives as hearts or numeric value
- Trigger game over state when lives <= 0
