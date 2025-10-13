# US-016: Golden Arepa Spawning

**As a** player
**I want** to see the Golden Arepa powerup in the level
**So that** I can collect it

## Acceptance Criteria
- [ ] Golden Arepa appears at defined position
- [ ] Powerup has distinct golden/yellow appearance
- [ ] Powerup floats/hovers with animation
- [ ] Powerup is larger or more noticeable than other objects
- [ ] Multiple powerups can exist in a level

## Technical Notes
- Create GoldenArepa class extending `pygame.sprite.Sprite`
- Implement simple floating animation (sine wave motion)
- Size: approximately 30x30 pixels
