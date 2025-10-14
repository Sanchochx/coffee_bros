# US-020: Laser-Enemy Collision

**As a** player
**I want** lasers to destroy enemies on contact
**So that** shooting is effective

## Acceptance Criteria
- [x] Laser hitting enemy destroys the enemy
- [x] Laser disappears after hitting enemy
- [x] Enemy defeat sound effect plays
- [x] Small explosion effect shows at impact point
- [x] Score increases when enemy defeated by laser
- [x] One laser can only hit one enemy

## Technical Notes
- Check collision between projectile and enemy sprites
- Remove both projectile and enemy on collision
- Award same points as stomp kill
- Create simple particle effect (optional)
