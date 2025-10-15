# US-033: Powerup Timer Display

**As a** player
**I want** to see how long my powerup lasts
**So that** I can plan my actions

## Acceptance Criteria
- [x] Timer appears when powerup collected
- [x] Shows remaining seconds in powered state
- [x] Counts down in real-time
- [x] Positioned near player or in HUD
- [x] Changes color when timer low (warning)
- [x] Disappears when powerup expires

## Technical Notes
- Convert frame timer to seconds for display
- Use different color when < 3 seconds remaining
- Position: top-center or near player
