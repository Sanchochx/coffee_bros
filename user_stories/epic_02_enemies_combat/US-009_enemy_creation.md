# US-009: Enemy Creation (Polocho)

**As a** player
**I want** to see Polocho enemies in the level
**So that** I have challenges to overcome

## Acceptance Criteria
- [ ] Polocho enemies spawn at defined positions
- [ ] Enemies have visible sprite/rectangle (40x40 pixels)
- [ ] Enemies appear distinct from player and platforms
- [ ] Multiple enemies can exist simultaneously
- [ ] Enemies are affected by gravity

## Technical Notes
- Create Polocho class extending `pygame.sprite.Sprite`
- Store enemies in sprite group
- Apply physics to enemies similar to player
