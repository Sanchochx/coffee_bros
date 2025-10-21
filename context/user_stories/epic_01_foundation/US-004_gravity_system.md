# US-004: Gravity System

**As a** player
**I want** Coffee to fall when not on solid ground
**So that** the game feels realistic

## Acceptance Criteria
- [x] Player falls downward when in air
- [x] Gravity acceleration is 0.8 pixels/frame²
- [x] Terminal velocity caps at 20 pixels/frame downward
- [x] Gravity applies continuously during gameplay
- [x] Player falls smoothly without jittering

## Technical Notes
- Implement velocity_y variable
- Apply gravity each frame: `velocity_y += GRAVITY`
- Cap velocity: `velocity_y = min(velocity_y, TERMINAL_VELOCITY)`
