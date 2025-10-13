# US-049: Player Animation - Jumping

**As a** player
**I want** to see Sancho's jump animation
**So that** jumping looks dynamic

## Acceptance Criteria
- [ ] Jump animation shows when player in air
- [ ] Different frames for ascending vs descending
- [ ] Transitions smoothly from walk to jump
- [ ] Lands with appropriate frame

## Technical Notes
- Use jump frame when `velocity_y < 0` (going up)
- Use fall frame when `velocity_y > 0` (falling)
- 2 frames needed (jump, fall)
