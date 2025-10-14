# US-016: Golden Arepa Spawning

**As a** player
**I want** to see the Golden Arepa powerup in the level
**So that** I can collect it

## Acceptance Criteria
- [x] Golden Arepa appears at defined position
- [x] Powerup has distinct golden/yellow appearance
- [x] Powerup floats/hovers with animation
- [x] Powerup is larger or more noticeable than other objects
- [x] Multiple powerups can exist in a level

## Technical Notes
- Create GoldenArepa class extending `pygame.sprite.Sprite`
- Implement simple floating animation (sine wave motion)
- Size: approximately 30x30 pixels
