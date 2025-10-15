# US-034: Main Menu

**As a** player
**I want** to see a main menu when starting the game
**So that** I can choose to start or configure settings

## Acceptance Criteria
- [x] Menu appears on game start
- [x] Shows game title "Sancho Bros"
- [x] Includes "Start Game" option
- [x] Includes "Settings" option
- [x] Includes "Quit" option
- [x] Options are selectable with arrow keys and Enter
- [x] Has Colombian-themed background
- [ ] Plays menu music (deferred to US-047: Background Music in Epic 7)

## Technical Notes
- Create menu state separate from gameplay
- Implement menu navigation with keyboard
- Transition to game state when Start selected
