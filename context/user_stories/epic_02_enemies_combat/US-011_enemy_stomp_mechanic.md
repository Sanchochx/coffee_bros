# US-011: Enemy Stomp Mechanic

**As a** player
**I want** to defeat enemies by jumping on their heads
**So that** I can clear my path

## Acceptance Criteria
- [x] Jumping on enemy from above defeats the enemy
- [x] Enemy displays "squashed" state briefly before disappearing
- [x] Player bounces upward slightly after stomping
- [x] Stomping plays a sound effect (placeholder added, audio system in Epic 7)
- [x] Score increases when enemy is defeated
- [x] Enemy cannot damage player during stomp

## Technical Notes
- Check if player is falling (`velocity_y > 0`) during collision
- Check if player's bottom hits enemy's top half
- Apply small upward bounce: `player.velocity_y = -8`
- Remove enemy from game after squash animation
