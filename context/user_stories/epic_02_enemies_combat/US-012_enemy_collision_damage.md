# US-012: Enemy Collision Damage

**As a** player
**I want** to lose a life when touching an enemy incorrectly
**So that** there are consequences for mistakes

## Acceptance Criteria
- [x] Touching enemy from side damages player
- [x] Touching enemy from below damages player
- [x] Player loses one life when damaged
- [x] Player briefly becomes invulnerable after taking damage (1 second)
- [x] Player blinks during invulnerability period
- [x] Damage sound effect plays (placeholder added for Epic 7)
- [x] Player is pushed back slightly when hit

## Technical Notes
- Implement invulnerability timer (60 frames at 60 FPS)
- Flash player sprite every 5 frames during invulnerability
- Prevent further damage while invulnerable
