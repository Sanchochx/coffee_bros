# US-047: Background Music

**As a** player
**I want** to hear music during gameplay
**So that** the game has atmosphere

## Acceptance Criteria
- [ ] Different music for menu and gameplay
- [ ] Music loops seamlessly
- [ ] Music volume is adjustable
- [ ] Music doesn't overpower sound effects
- [ ] Music can be muted in settings
- [ ] Music matches Colombian/upbeat theme

## Technical Notes
- Use `pygame.mixer.music` for background tracks
- Load OGG format for better compression
- Set music volume lower than SFX (0.3-0.5)
