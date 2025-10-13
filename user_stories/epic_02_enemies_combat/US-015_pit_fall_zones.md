# US-015: Pit/Fall Zones

**As a** player
**I want** to die when falling into pits
**So that** there are environmental hazards

## Acceptance Criteria
- [ ] Falling below screen bottom causes death
- [ ] Player loses one life when falling in pit
- [ ] Pit zones can be defined in level data
- [ ] Death is immediate upon entering pit zone
- [ ] Fall death sound effect plays

## Technical Notes
- Check if `player.y > SCREEN_HEIGHT`
- Can also define specific pit rectangles for mid-level pits
- Call player death method on pit collision
