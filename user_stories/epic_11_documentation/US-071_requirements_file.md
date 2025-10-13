# US-071: Requirements File

**As a** developer
**I want** a requirements.txt file
**So that** dependencies are clear

## Acceptance Criteria
- [ ] requirements.txt lists all dependencies
- [ ] Version constraints are specified
- [ ] File is in project root
- [ ] `pip install -r requirements.txt` works

## Technical Notes
- Include pygame version
- Can generate with `pip freeze > requirements.txt`
- Specify minimum versions with >=
