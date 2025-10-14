# US-019: Laser Shooting Mechanic

**As a** player
**I want** to shoot laser beams while powered up
**So that** I can defeat enemies from a distance

## Acceptance Criteria
- [x] Pressing X or J fires laser in facing direction
- [x] Laser only fires when powered up
- [x] Laser travels horizontally across screen
- [x] Laser has visible projectile sprite/effect
- [x] Shooting sound effect plays (placeholder added - audio in Epic 7)
- [x] Can shoot multiple lasers rapidly (cooldown: 0.5 seconds)
- [x] Lasers disappear when leaving screen

## Technical Notes
- Create Projectile class
- Store player's facing direction
- Laser speed: 10 pixels/frame
- Maximum 5 active projectiles at once
- Remove projectile when `x < 0` or `x > level_width`
