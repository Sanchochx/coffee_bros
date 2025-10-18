# US-071: Requirements File

**As a** developer
**I want** a requirements.txt file
**So that** dependencies are clear

## Acceptance Criteria
- [x] requirements.txt lists all dependencies
- [x] Version constraints are specified
- [x] File is in project root
- [x] `pip install -r requirements.txt` works

## Technical Notes
- Include pygame version
- Can generate with `pip freeze > requirements.txt`
- Specify minimum versions with >=
