# US-019: Laser Shooting Mechanic

**As a** player
**I want** to shoot laser beams while powered up
**So that** I can defeat enemies from a distance

## Acceptance Criteria
- [ ] Pressing X or J fires laser in facing direction
- [ ] Laser only fires when powered up
- [ ] Laser travels horizontally across screen
- [ ] Laser has visible projectile sprite/effect
- [ ] Shooting sound effect plays
- [ ] Can shoot multiple lasers rapidly (cooldown: 0.5 seconds)
- [ ] Lasers disappear when leaving screen

## Technical Notes
- Create Projectile class
- Store player's facing direction
- Laser speed: 10 pixels/frame
- Maximum 5 active projectiles at once
- Remove projectile when `x < 0` or `x > level_width`
