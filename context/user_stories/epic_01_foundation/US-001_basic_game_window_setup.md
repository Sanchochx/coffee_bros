# US-001: Basic Game Window Setup

**As a** developer
**I want** to set up the basic game window and main loop
**So that** I have a foundation to build the game upon

## Acceptance Criteria
- [x] Pygame is installed and imported successfully
- [x] Game window opens at 800x600 resolution
- [x] Window title displays "Coffee Bros"
- [x] Game loop runs at consistent 60 FPS
- [x] Window can be closed using the X button or ESC key
- [x] Black background is displayed initially

## Technical Notes
- Use `pygame.init()` and `pygame.display.set_mode()`
- Implement FPS control with `pygame.time.Clock()`
- Handle `QUIT` event properly
