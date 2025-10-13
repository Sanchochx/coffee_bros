# US-009: Enemy Creation (Polocho)

**As a** player
**I want** to see Polocho enemies in the level
**So that** I have challenges to overcome

## Acceptance Criteria
- [x] Polocho enemies spawn at defined positions
- [x] Enemies have visible sprite/rectangle (40x40 pixels)
- [x] Enemies appear distinct from player and platforms
- [x] Multiple enemies can exist simultaneously
- [x] Enemies are affected by gravity

## Technical Notes
- Create Polocho class extending `pygame.sprite.Sprite`
- Store enemies in sprite group
- Apply physics to enemies similar to player
