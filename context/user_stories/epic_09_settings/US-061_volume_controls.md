# US-061: Volume Controls

**As a** player
**I want** to control music and sound volume
**So that** audio suits my preference

## Acceptance Criteria
- [x] Separate sliders for music and SFX volume
- [x] Volume range: 0-100%
- [x] Changes apply immediately
- [x] Settings persist between sessions
- [x] Can mute completely (0%)

## Technical Notes
- Use slider or percentage display
- Apply to `pygame.mixer.music.set_volume()` and sound volumes
- Save to config file
