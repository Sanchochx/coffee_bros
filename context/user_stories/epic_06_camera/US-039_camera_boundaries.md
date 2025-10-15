# US-039: Camera Boundaries

**As a** developer
**I want** the camera to stay within level bounds
**So that** no empty space is visible

## Acceptance Criteria
- [x] Camera cannot scroll past left edge of level (x=0)
- [x] Camera cannot scroll past right edge of level
- [x] Scrolling stops smoothly at boundaries
- [x] Player can still move near level edges
- [x] No black bars or empty space visible

## Technical Notes
- Calculate max camera offset: `level.width - SCREEN_WIDTH`
- Clamp camera offset each frame
- Test with levels of different widths
