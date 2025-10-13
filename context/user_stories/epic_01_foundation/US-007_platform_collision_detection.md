# US-007: Platform Collision Detection

**As a** player
**I want** Sancho to land on and stand on platforms
**So that** I can navigate the level

## Acceptance Criteria
- [x] Player lands on top of platforms when falling
- [x] Player can walk along platform surfaces
- [x] Player cannot pass through platforms from below
- [x] Player cannot pass through platforms from sides
- [x] Collision detection is precise with no gaps
- [x] Player velocity stops when landing on platform

## Technical Notes
- Implement AABB collision detection
- Check collision separately for each axis (x, y)
- Set `velocity_y = 0` and `is_grounded = True` on landing
- Resolve collisions by adjusting player position
