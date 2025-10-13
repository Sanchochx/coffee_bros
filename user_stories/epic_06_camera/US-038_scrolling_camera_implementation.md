# US-038: Scrolling Camera Implementation

**As a** player
**I want** the camera to follow Sancho
**So that** I can see where I'm going in large levels

## Acceptance Criteria
- [ ] Camera follows player horizontally
- [ ] Camera scrolls when player passes screen center
- [ ] Camera doesn't scroll beyond level boundaries
- [ ] Camera movement is smooth (no sudden jumps)
- [ ] Camera doesn't show areas outside level bounds
- [ ] Vertical scrolling not needed (levels fit in screen height)

## Technical Notes
- Create Camera class to manage viewport offset
- Calculate camera position based on player position
- Clamp camera to `[0, level_width - SCREEN_WIDTH]`
- All rendering positions offset by camera position
