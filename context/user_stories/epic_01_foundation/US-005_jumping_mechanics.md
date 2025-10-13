# US-005: Jumping Mechanics

**As a** player
**I want** to make Sancho jump
**So that** I can navigate obstacles and platforms

## Acceptance Criteria
- [ ] Pressing UP/W/SPACE makes player jump when on ground
- [ ] Jump has initial upward velocity of -15 pixels/frame
- [ ] Player can only jump when touching a platform (no double-jump)
- [ ] Jump height varies based on how long button is held
- [ ] Releasing jump button early results in lower jump
- [ ] Jump feels responsive and natural

## Technical Notes
- Track `is_grounded` state
- Apply jump velocity when jump key pressed and grounded
- Implement variable jump by reducing upward velocity on key release
