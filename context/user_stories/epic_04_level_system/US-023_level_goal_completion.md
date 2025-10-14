# US-023: Level Goal/Completion

**As a** player
**I want** to reach a goal to complete the level
**So that** I can progress to the next level

## Acceptance Criteria
- [x] Goal object/zone exists at end of level
- [x] Goal is visually distinct (flag, door, etc.)
- [x] Touching goal completes the level
- [x] Level completion sound/music plays
- [x] Completion screen shows before next level
- [x] Score and time are displayed on completion

## Technical Notes
- Create goal as rectangle or sprite at level end
- Check collision between player and goal
- Transition to `LEVEL_COMPLETE` state
- Load next level after brief delay (2-3 seconds)
