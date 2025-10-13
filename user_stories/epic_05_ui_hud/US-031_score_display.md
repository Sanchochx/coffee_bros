# US-031: Score Display

**As a** player
**I want** to see my current score
**So that** I know how well I'm performing

## Acceptance Criteria
- [ ] Score is displayed in top-left or top-center of screen
- [ ] Score updates immediately when points earned
- [ ] Score is clearly readable (large, contrasting color)
- [ ] Score persists across level transitions
- [ ] Score format: "SCORE: 00000"

## Technical Notes
- Render text using `pygame.font`
- Update score for: enemy defeat (+100), powerup collection (+50), level completion (+500)
- Store score in game state
