# US-007: Platform Collision Detection

**As a** player
**I want** Sancho to land on and stand on platforms
**So that** I can navigate the level

## Acceptance Criteria
- [ ] Player lands on top of platforms when falling
- [ ] Player can walk along platform surfaces
- [ ] Player cannot pass through platforms from below
- [ ] Player cannot pass through platforms from sides
- [ ] Collision detection is precise with no gaps
- [ ] Player velocity stops when landing on platform

## Technical Notes
- Implement AABB collision detection
- Check collision separately for each axis (x, y)
- Set `velocity_y = 0` and `is_grounded = True` on landing
- Resolve collisions by adjusting player position
