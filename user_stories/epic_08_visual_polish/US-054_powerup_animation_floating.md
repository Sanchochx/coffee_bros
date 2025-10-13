# US-054: Powerup Animation - Floating

**As a** player
**I want** to see the Golden Arepa floating
**So that** it's attractive and noticeable

## Acceptance Criteria
- [ ] Powerup bobs up and down smoothly
- [ ] Animation is continuous loop
- [ ] Movement is subtle (not distracting)
- [ ] Easy to spot in level

## Technical Notes
- Use sine wave for vertical position offset
- Amplitude: 10 pixels
- Speed: slow (0.05 radians/frame)
- Optional: add rotation
