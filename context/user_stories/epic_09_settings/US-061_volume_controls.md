# US-061: Volume Controls

**As a** player
**I want** to control music and sound volume
**So that** audio suits my preference

## Acceptance Criteria
- [ ] Separate sliders for music and SFX volume
- [ ] Volume range: 0-100%
- [ ] Changes apply immediately
- [ ] Settings persist between sessions
- [ ] Can mute completely (0%)

## Technical Notes
- Use slider or percentage display
- Apply to `pygame.mixer.music.set_volume()` and sound volumes
- Save to config file
