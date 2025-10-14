# US-015: Pit/Fall Zones

**As a** player
**I want** to die when falling into pits
**So that** there are environmental hazards

## Acceptance Criteria
- [x] Falling below screen bottom causes death
- [x] Player loses one life when falling in pit
- [x] Pit zones can be defined in level data
- [x] Death is immediate upon entering pit zone
- [x] Fall death sound effect plays

## Technical Notes
- Check if `player.y > SCREEN_HEIGHT`
- Can also define specific pit rectangles for mid-level pits
- Call player death method on pit collision
