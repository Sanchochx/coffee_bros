# Coffee Bros - Build Instructions

Quick guide to building a standalone executable for distribution.

## Prerequisites

1. **Python 3.8+** installed
2. **All game dependencies** installed

## Step-by-Step Build Process

### 1. Install Dependencies

First, make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

This will install:
- `pygame` - Game engine
- `numpy` - Audio generation utilities
- `psutil` - Performance monitoring
- `pyinstaller` - Build tool for creating executables

### 2. Run the Build Script

Simply run:

```bash
python build.py
```

### 3. Find Your Executable

After the build completes, you'll find:
- **Executable**: `dist/CoffeeBros.exe` (Windows) or `dist/CoffeeBros` (Mac/Linux)
- **Distribution Package**: `dist/CoffeeBros_[platform].zip` (or `.tar.gz`)

### 4. Test the Build

Before distributing, test the executable:

```bash
# Windows
dist\CoffeeBros.exe

# Mac/Linux
./dist/CoffeeBros
```

### 5. Distribute

Share the distribution archive (`.zip` or `.tar.gz`) from the `dist/` folder with end users.

---

## Alternative: Manual Build

If you prefer to build manually without the script:

### Windows
```bash
pyinstaller --name CoffeeBros --onefile --windowed --add-data "assets;assets" --add-data "config.py;." main.py
```

### macOS / Linux
```bash
pyinstaller --name CoffeeBros --onefile --windowed --add-data "assets:assets" --add-data "config.py:." main.py
```

---

## Troubleshooting

### PyInstaller not found
```bash
pip install pyinstaller
```

### Build fails with missing modules
Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Executable crashes on run
Build with console enabled to see errors:
```bash
pyinstaller --name CoffeeBros --onefile --console --add-data "assets;assets" --add-data "config.py;." main.py
```

---

## Platform-Specific Notes

### Windows
- Creates `CoffeeBros.exe`
- Users may see Windows Defender warning (normal for unsigned executables)
- Click "More info" → "Run anyway"

### macOS
- Creates `CoffeeBros` (no extension)
- Users may need to allow in Security & Privacy settings
- Make executable: `chmod +x CoffeeBros`

### Linux
- Creates `CoffeeBros` (no extension)
- Make executable: `chmod +x CoffeeBros`
- Works on most distributions

---

## What Gets Included

The build automatically bundles:
- ✅ Python runtime (no Python installation needed by users)
- ✅ All game code
- ✅ All assets (graphics, sounds, music, levels)
- ✅ Configuration files
- ✅ All dependencies (pygame, numpy, etc.)

---

## For End Users

Once built, users only need to:
1. Extract the archive
2. Double-click the executable
3. Play!

No Python or dependencies required on their system.

---

For more detailed information, see `DISTRIBUTION_GUIDE.md`.
