# US-002: Player Character Creation

**As a** player
**I want** to see Coffee on screen
**So that** I can identify my character

## Acceptance Criteria
- [x] Player sprite/rectangle is displayed on screen
- [x] Player has initial spawn position (x=100, y=400)
- [x] Player has visible dimensions (40x60 pixels)
- [x] Player color/appearance is distinct from background
- [x] Player renders on top of other game elements

## Technical Notes
- Create Player class extending `pygame.sprite.Sprite`
- Use placeholder colored rectangle initially
- Store position as (x, y) coordinates
