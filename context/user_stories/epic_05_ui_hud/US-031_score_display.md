# US-031: Score Display

**As a** player
**I want** to see my current score
**So that** I know how well I'm performing

## Acceptance Criteria
- [x] Score is displayed in top-left or top-center of screen
- [x] Score updates immediately when points earned
- [x] Score is clearly readable (large, contrasting color)
- [x] Score persists across level transitions
- [x] Score format: "SCORE: 00000"

## Technical Notes
- Render text using `pygame.font`
- Update score for: enemy defeat (+100), powerup collection (+50), level completion (+500)
- Store score in game state
