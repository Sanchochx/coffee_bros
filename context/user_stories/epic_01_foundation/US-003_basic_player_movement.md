# US-003: Basic Player Movement

**As a** player
**I want** to move Sancho left and right
**So that** I can navigate the level

## Acceptance Criteria
- [x] Pressing LEFT arrow/A key moves player left at 5 pixels/frame
- [x] Pressing RIGHT arrow/D key moves player right at 5 pixels/frame
- [x] Player stops moving when key is released
- [x] Player cannot move off-screen horizontally
- [x] Movement is smooth and responsive
- [x] Player can change direction instantly

## Technical Notes
- Implement keyboard input handling in update method
- Use `pygame.key.get_pressed()` for continuous input
- Clamp player position to screen boundaries
