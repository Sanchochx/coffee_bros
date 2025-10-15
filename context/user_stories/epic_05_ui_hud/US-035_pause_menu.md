# US-035: Pause Menu

**As a** player
**I want** to pause the game
**So that** I can take breaks without losing progress

## Acceptance Criteria
- [x] Pressing ESC pauses the game
- [x] Game freezes (no updates) when paused
- [x] Pause menu overlays game screen
- [x] Shows "PAUSED" text
- [x] Includes "Resume" option
- [x] Includes "Restart Level" option
- [x] Includes "Return to Menu" option
- [x] Can unpause with ESC or selecting Resume

## Technical Notes
- Set game state to `PAUSED`
- Stop updating game entities while paused
- Darken/dim background for pause overlay
