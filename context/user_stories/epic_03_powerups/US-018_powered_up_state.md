# US-018: Powered-Up State

**As a** player
**I want** to know when I'm powered up
**So that** I know I can shoot lasers

## Acceptance Criteria
- [x] Player appearance changes when powered up (glow/color change)
- [x] Timer appears showing remaining powerup time
- [x] Powered-up state lasts 10 seconds
- [x] State automatically expires after timer ends
- [x] Visual warning when powerup about to expire (last 3 seconds)
- [x] Player returns to normal appearance after expiry

## Technical Notes
- Implement powerup timer (600 frames at 60 FPS)
- Add boolean flag `is_powered_up`
- Decrement timer each frame
- Flash player sprite when timer < 180 frames
