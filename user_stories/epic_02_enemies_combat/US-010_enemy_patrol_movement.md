# US-010: Enemy Patrol Movement

**As a** player
**I want** enemies to move back and forth
**So that** they present a moving challenge

## Acceptance Criteria
- [ ] Enemies walk left and right automatically
- [ ] Each enemy has defined patrol boundaries
- [ ] Enemy turns around when reaching patrol boundary
- [ ] Enemy movement speed is consistent
- [ ] Enemies stay on platforms (don't walk off edges)
- [ ] Enemy can turn around when hitting walls

## Technical Notes
- Store `patrol_start` and `patrol_end` for each enemy
- Check boundaries each frame and reverse direction
- Movement speed: 2 pixels/frame
