# US-005: Jumping Mechanics

**As a** player
**I want** to make Sancho jump
**So that** I can navigate obstacles and platforms

## Acceptance Criteria
- [x] Pressing UP/W/SPACE makes player jump when on ground
- [x] Jump has initial upward velocity of -15 pixels/frame
- [x] Player can only jump when touching a platform (no double-jump)
- [x] Jump height varies based on how long button is held
- [x] Releasing jump button early results in lower jump
- [x] Jump feels responsive and natural

## Technical Notes
- Track `is_grounded` state
- Apply jump velocity when jump key pressed and grounded
- Implement variable jump by reducing upward velocity on key release
