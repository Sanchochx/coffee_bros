# US-038: Scrolling Camera Implementation

**As a** player
**I want** the camera to follow Coffee
**So that** I can see where I'm going in large levels

## Acceptance Criteria
- [x] Camera follows player horizontally
- [x] Camera scrolls when player passes screen center
- [x] Camera doesn't scroll beyond level boundaries
- [x] Camera movement is smooth (no sudden jumps)
- [x] Camera doesn't show areas outside level bounds
- [x] Vertical scrolling not needed (levels fit in screen height)

## Technical Notes
- Create Camera class to manage viewport offset
- Calculate camera position based on player position
- Clamp camera to `[0, level_width - SCREEN_WIDTH]`
- All rendering positions offset by camera position
