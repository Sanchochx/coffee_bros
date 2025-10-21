# Coffee Bros - Distribution Guide

This guide explains how to package and distribute Coffee Bros for end users.

## Table of Contents

- [Quick Start](#quick-start)
- [Building the Executable](#building-the-executable)
- [Manual Build with PyInstaller](#manual-build-with-pyinstaller)
- [Distribution Package Contents](#distribution-package-contents)
- [Platform-Specific Notes](#platform-specific-notes)
- [Testing the Build](#testing-the-build)

---

## Quick Start

### For Developers

**1. Install build dependencies:**
```bash
pip install -r requirements.txt
```

**2. Run the build script:**
```bash
python build.py
```

**3. Find your distribution package:**
- The executable and distribution archive will be in the `dist/` folder
- Share the `.zip` (Windows) or `.tar.gz` (Mac/Linux) file with users

---

## Building the Executable

### Automated Build (Recommended)

Use the included `build.py` script for an automated build process:

```bash
python build.py
```

This script will:
1. Clean previous build directories
2. Create a standalone executable using PyInstaller
3. Package all necessary assets
4. Create a distribution archive
5. Generate user instructions

### What Gets Packaged

The build script automatically includes:
- **Executable**: Single-file executable (`CoffeeBros.exe` on Windows, `CoffeeBros` on Mac/Linux)
- **Assets**: All game assets (graphics, sounds, music, levels)
- **Configuration**: Game configuration files
- **Documentation**: README and user instructions

---

## Manual Build with PyInstaller

If you prefer manual control, use PyInstaller directly:

### Windows

```bash
pyinstaller --name CoffeeBros ^
            --onefile ^
            --windowed ^
            --add-data "assets;assets" ^
            --add-data "config.py;." ^
            main.py
```

### macOS / Linux

```bash
pyinstaller --name CoffeeBros \
            --onefile \
            --windowed \
            --add-data "assets:assets" \
            --add-data "config.py:." \
            main.py
```

### PyInstaller Options Explained

- `--name CoffeeBros`: Name of the executable
- `--onefile`: Bundle everything into a single executable
- `--windowed`: Hide the console window (use `--console` for debugging)
- `--clean`: Clean PyInstaller cache before building
- `--add-data`: Include asset files (format: `source;destination` on Windows, `source:destination` on Mac/Linux)

---

## Distribution Package Contents

A complete distribution package includes:

```
CoffeeBros_windows/
├── CoffeeBros.exe          # Game executable
├── HOW_TO_PLAY.txt         # User instructions
└── README.md               # Full project documentation
```

### Creating the Package Manually

1. Create a folder: `CoffeeBros_[platform]`
2. Copy the executable from `dist/CoffeeBros[.exe]`
3. Copy `README.md` and create `HOW_TO_PLAY.txt` with user instructions
4. Create a ZIP or TAR.GZ archive

---

## Platform-Specific Notes

### Windows

- **Executable Format**: `.exe`
- **Archive Format**: `.zip`
- **Notes**:
  - May trigger Windows Defender SmartScreen on first run (expected for unsigned executables)
  - Users can click "More info" → "Run anyway"
  - Consider code signing for commercial distribution

### macOS

- **Executable Format**: Unix executable (no extension)
- **Archive Format**: `.tar.gz` or `.dmg`
- **Notes**:
  - Users may need to allow the app in Security & Privacy settings
  - Make the file executable: `chmod +x CoffeeBros`
  - Consider creating a `.dmg` or `.app` bundle for better user experience
  - May need to code sign for Gatekeeper compatibility

### Linux

- **Executable Format**: Unix executable (no extension)
- **Archive Format**: `.tar.gz` or `.AppImage`
- **Notes**:
  - Make the file executable: `chmod +x CoffeeBros`
  - Works on most distributions with standard libraries
  - Consider creating an AppImage for better portability

---

## Testing the Build

### Pre-Distribution Checklist

Before distributing, test the build thoroughly:

1. **Clean System Test**
   - Test on a system WITHOUT Python installed
   - Verify the executable runs independently
   - Check that all assets load correctly

2. **Functionality Test**
   - Play through all 5 levels
   - Test all game features (jumping, shooting, power-ups)
   - Verify audio works (music and sound effects)
   - Check menu navigation (main menu, pause, settings)
   - Test save/load functionality

3. **Performance Test**
   - Monitor frame rate (should maintain 60 FPS)
   - Check memory usage
   - Verify no crashes or errors

4. **Cross-Platform Test** (if distributing for multiple platforms)
   - Build and test on each target platform
   - Verify platform-specific features work

### Testing Commands

**Run the executable directly:**
```bash
# Windows
dist\CoffeeBros.exe

# macOS/Linux
./dist/CoffeeBros
```

**Check for missing dependencies:**
```bash
# On the target system (should show "Python not found" is OK)
python --version
```

---

## Troubleshooting

### Build Issues

**Issue**: PyInstaller not found
- **Solution**: Install with `pip install pyinstaller`

**Issue**: Missing assets in build
- **Solution**: Check `--add-data` paths in build command
- Verify assets exist in source directory

**Issue**: Build succeeds but executable crashes
- **Solution**: Build with `--console` flag to see error messages
- Check for missing Python dependencies

### Distribution Issues

**Issue**: "File not found" errors when running
- **Solution**: Assets weren't included in build
- Rebuild with correct `--add-data` parameters

**Issue**: Import errors
- **Solution**: Missing dependencies in PyInstaller
- Add hidden imports: `--hidden-import module_name`

**Issue**: Executable too large
- **Solution**: Normal for PyInstaller (includes Python runtime)
- Typical size: 30-100 MB depending on dependencies

---

## Advanced Options

### Creating a Windows Installer

Use a tool like **Inno Setup** or **NSIS** to create a professional installer:

1. Build the executable with PyInstaller
2. Create an installer script
3. Include shortcuts, uninstaller, file associations

### Code Signing

For professional distribution:

- **Windows**: Use `signtool.exe` with a code signing certificate
- **macOS**: Use Apple Developer certificate and `codesign`
- **Linux**: Generally not required

### Custom Icons

Add a custom icon to the executable:

```bash
# Windows
pyinstaller ... --icon=assets/icon.ico main.py

# macOS
pyinstaller ... --icon=assets/icon.icns main.py
```

Icon requirements:
- **Windows**: `.ico` file (recommended: 256x256)
- **macOS**: `.icns` file (multiple sizes)

---

## File Size Optimization

The executable will be large (30-100 MB) because it includes:
- Python runtime (~15-20 MB)
- Pygame library (~10-15 MB)
- Game assets (varies)
- Other dependencies

To reduce size:
1. Compress assets (use compressed audio formats)
2. Use `--exclude-module` for unused libraries
3. Use UPX compression: `pyinstaller --upx-dir /path/to/upx ...`

---

## Distribution Checklist

Before releasing:

- [ ] Build executable for all target platforms
- [ ] Test on clean systems (no Python)
- [ ] Create user documentation (HOW_TO_PLAY.txt)
- [ ] Package with README and license
- [ ] Test all game features in distributed version
- [ ] Create release notes
- [ ] Upload to distribution platform (itch.io, Steam, etc.)
- [ ] Consider code signing (optional but recommended)

---

## Support and Updates

When distributing updates:

1. **Version Numbering**: Use semantic versioning (e.g., 1.0.0, 1.1.0)
2. **Change Log**: Document what's new/fixed
3. **Backward Compatibility**: Ensure save files work with new version
4. **Update Distribution**: Replace old files on distribution platform

---

## Additional Resources

- **PyInstaller Documentation**: https://pyinstaller.org/
- **Pygame Documentation**: https://www.pygame.org/docs/
- **Python Packaging Guide**: https://packaging.python.org/

---

**Happy Distributing! ☕🎮**
