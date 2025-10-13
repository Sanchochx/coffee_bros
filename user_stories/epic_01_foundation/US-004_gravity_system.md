# US-004: Gravity System

**As a** player
**I want** Sancho to fall when not on solid ground
**So that** the game feels realistic

## Acceptance Criteria
- [ ] Player falls downward when in air
- [ ] Gravity acceleration is 0.8 pixels/frame²
- [ ] Terminal velocity caps at 20 pixels/frame downward
- [ ] Gravity applies continuously during gameplay
- [ ] Player falls smoothly without jittering

## Technical Notes
- Implement velocity_y variable
- Apply gravity each frame: `velocity_y += GRAVITY`
- Cap velocity: `velocity_y = min(velocity_y, TERMINAL_VELOCITY)`
