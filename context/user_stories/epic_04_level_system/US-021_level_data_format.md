# US-021: Level Data Format

**As a** developer
**I want** to define levels using JSON files
**So that** levels are easy to create and modify

## Acceptance Criteria
- [x] Level data is stored in JSON format
- [x] JSON includes platforms, enemies, powerups, pits
- [x] JSON specifies player spawn and goal positions
- [x] JSON includes level metadata (name, size, background)
- [x] Level files are located in `assets/levels/` directory
- [x] JSON structure follows documented format

## Technical Notes
- Use Python's `json` module to load data
- Validate required fields when loading
- Handle missing or malformed JSON gracefully
