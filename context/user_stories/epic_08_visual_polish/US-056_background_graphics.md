# US-056: Background Graphics

**As a** player
**I want** to see themed backgrounds
**So that** levels have atmosphere

## Acceptance Criteria
- [x] Each level has appropriate background image
- [x] Backgrounds show Colombian highlands theme
- [x] Backgrounds don't interfere with gameplay visibility
- [x] Images are high quality and attractive
- [x] Sky, mountains, and coffee plants visible

## Technical Notes
- Load background image per level from JSON
- Render behind all game objects
- Scale to screen size if needed
- Use parallax scrolling (optional enhancement)
