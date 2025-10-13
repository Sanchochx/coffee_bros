# US-035: Pause Menu

**As a** player
**I want** to pause the game
**So that** I can take breaks without losing progress

## Acceptance Criteria
- [ ] Pressing ESC pauses the game
- [ ] Game freezes (no updates) when paused
- [ ] Pause menu overlays game screen
- [ ] Shows "PAUSED" text
- [ ] Includes "Resume" option
- [ ] Includes "Restart Level" option
- [ ] Includes "Return to Menu" option
- [ ] Can unpause with ESC or selecting Resume

## Technical Notes
- Set game state to `PAUSED`
- Stop updating game entities while paused
- Darken/dim background for pause overlay
