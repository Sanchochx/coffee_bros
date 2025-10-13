# US-011: Enemy Stomp Mechanic

**As a** player
**I want** to defeat enemies by jumping on their heads
**So that** I can clear my path

## Acceptance Criteria
- [ ] Jumping on enemy from above defeats the enemy
- [ ] Enemy displays "squashed" state briefly before disappearing
- [ ] Player bounces upward slightly after stomping
- [ ] Stomping plays a sound effect
- [ ] Score increases when enemy is defeated
- [ ] Enemy cannot damage player during stomp

## Technical Notes
- Check if player is falling (`velocity_y > 0`) during collision
- Check if player's bottom hits enemy's top half
- Apply small upward bounce: `player.velocity_y = -8`
- Remove enemy from game after squash animation
