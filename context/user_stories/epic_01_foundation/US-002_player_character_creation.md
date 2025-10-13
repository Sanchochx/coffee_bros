# US-002: Player Character Creation

**As a** player
**I want** to see Sancho on screen
**So that** I can identify my character

## Acceptance Criteria
- [ ] Player sprite/rectangle is displayed on screen
- [ ] Player has initial spawn position (x=100, y=400)
- [ ] Player has visible dimensions (40x60 pixels)
- [ ] Player color/appearance is distinct from background
- [ ] Player renders on top of other game elements

## Technical Notes
- Create Player class extending `pygame.sprite.Sprite`
- Use placeholder colored rectangle initially
- Store position as (x, y) coordinates
