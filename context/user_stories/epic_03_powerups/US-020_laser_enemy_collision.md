# US-020: Laser-Enemy Collision

**As a** player
**I want** lasers to destroy enemies on contact
**So that** shooting is effective

## Acceptance Criteria
- [ ] Laser hitting enemy destroys the enemy
- [ ] Laser disappears after hitting enemy
- [ ] Enemy defeat sound effect plays
- [ ] Small explosion effect shows at impact point
- [ ] Score increases when enemy defeated by laser
- [ ] One laser can only hit one enemy

## Technical Notes
- Check collision between projectile and enemy sprites
- Remove both projectile and enemy on collision
- Award same points as stomp kill
- Create simple particle effect (optional)
