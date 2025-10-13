# US-013: Lives System

**As a** player
**I want** to have multiple lives
**So that** I have multiple chances to complete the level

## Acceptance Criteria
- [ ] Player starts with 3 lives
- [ ] Current lives are displayed on screen (HUD)
- [ ] Lives decrease when player takes damage
- [ ] Lives decrease when player falls in pit
- [ ] Game over occurs when lives reach 0
- [ ] Lives persist within the same level attempt

## Technical Notes
- Store lives count in player or game state
- Display lives as hearts or numeric value
- Trigger game over state when lives <= 0
