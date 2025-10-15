# US-047: Background Music

**As a** player
**I want** to hear music during gameplay
**So that** the game has atmosphere

## Acceptance Criteria
- [x] Different music for menu and gameplay
- [x] Music loops seamlessly
- [x] Music volume is adjustable
- [x] Music doesn't overpower sound effects
- [x] Music can be muted in settings
- [x] Music matches Colombian/upbeat theme

## Technical Notes
- Use `pygame.mixer.music` for background tracks
- Load OGG format for better compression
- Set music volume lower than SFX (0.3-0.5)
