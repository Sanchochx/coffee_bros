# US-049: Player Animation - Jumping

**As a** player
**I want** to see Sancho's jump animation
**So that** jumping looks dynamic

## Acceptance Criteria
- [x] Jump animation shows when player in air
- [x] Different frames for ascending vs descending
- [x] Transitions smoothly from walk to jump
- [x] Lands with appropriate frame

## Technical Notes
- Use jump frame when `velocity_y < 0` (going up)
- Use fall frame when `velocity_y > 0` (falling)
- 2 frames needed (jump, fall)
