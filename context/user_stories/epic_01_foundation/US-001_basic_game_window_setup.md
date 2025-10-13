# US-001: Basic Game Window Setup

**As a** developer
**I want** to set up the basic game window and main loop
**So that** I have a foundation to build the game upon

## Acceptance Criteria
- [ ] Pygame is installed and imported successfully
- [ ] Game window opens at 800x600 resolution
- [ ] Window title displays "Sancho Bros"
- [ ] Game loop runs at consistent 60 FPS
- [ ] Window can be closed using the X button or ESC key
- [ ] Black background is displayed initially

## Technical Notes
- Use `pygame.init()` and `pygame.display.set_mode()`
- Implement FPS control with `pygame.time.Clock()`
- Handle `QUIT` event properly
