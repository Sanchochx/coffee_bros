# US-010: Enemy Patrol Movement

**As a** player
**I want** enemies to move back and forth
**So that** they present a moving challenge

## Acceptance Criteria
- [x] Enemies walk left and right automatically
- [x] Each enemy has defined patrol boundaries
- [x] Enemy turns around when reaching patrol boundary
- [x] Enemy movement speed is consistent
- [x] Enemies stay on platforms (don't walk off edges)
- [x] Enemy can turn around when hitting walls

## Technical Notes
- Store `patrol_start` and `patrol_end` for each enemy
- Check boundaries each frame and reverse direction
- Movement speed: 2 pixels/frame
