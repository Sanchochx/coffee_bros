"""
Sancho Bros - Build Script for Game Distribution
Creates standalone executables using PyInstaller for Windows, macOS, and Linux.
"""

import os
import shutil
import subprocess
import sys
import platform

# Build configuration
APP_NAME = "SanchoBros"
MAIN_SCRIPT = "main.py"
ICON_FILE = None  # Set to path of .ico file if you have one (Windows)

# Paths
DIST_DIR = "dist"
BUILD_DIR = "build"
SPEC_FILE = f"{APP_NAME}.spec"

# Asset directories to include
DATA_FILES = [
    ('assets', 'assets'),
    ('config.py', '.'),
]


def clean_build_directories():
    """Remove previous build and dist directories."""
    print("Cleaning previous build directories...")
    for directory in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"  Removed {directory}/")

    # Remove spec file if it exists
    if os.path.exists(SPEC_FILE):
        os.remove(SPEC_FILE)
        print(f"  Removed {SPEC_FILE}")


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print(f"PyInstaller version: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("ERROR: PyInstaller is not installed!")
        print("Please install it with: pip install pyinstaller")
        return False


def build_executable():
    """Build the standalone executable using PyInstaller."""
    print(f"\nBuilding {APP_NAME} executable...")
    print(f"Platform: {platform.system()}")

    # Build PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window (use --console for debugging)
        "--clean",  # Clean PyInstaller cache
    ]

    # Add icon if specified (Windows only)
    if ICON_FILE and os.path.exists(ICON_FILE) and platform.system() == "Windows":
        cmd.extend(["--icon", ICON_FILE])

    # Add data files (assets, config, etc.)
    for src, dest in DATA_FILES:
        if os.path.exists(src):
            cmd.extend(["--add-data", f"{src}{os.pathsep}{dest}"])
        else:
            print(f"WARNING: {src} not found, skipping...")

    # Add the main script
    cmd.append(MAIN_SCRIPT)

    # Print command for debugging
    print(f"Running: {' '.join(cmd)}")

    # Run PyInstaller
    try:
        result = subprocess.run(cmd, check=True)
        print("\nBuild completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Build failed with return code {e.returncode}")
        return False


def create_distribution_package():
    """Create a distribution package with the executable and necessary files."""
    print("\nCreating distribution package...")

    # Determine executable extension based on platform
    exe_ext = ".exe" if platform.system() == "Windows" else ""
    exe_name = f"{APP_NAME}{exe_ext}"

    # Create distribution directory name with platform
    platform_name = platform.system().lower()
    dist_package_name = f"{APP_NAME}_{platform_name}"
    dist_package_path = os.path.join(DIST_DIR, dist_package_name)

    # Create package directory
    os.makedirs(dist_package_path, exist_ok=True)

    # Copy executable
    exe_src = os.path.join(DIST_DIR, exe_name)
    exe_dest = os.path.join(dist_package_path, exe_name)
    if os.path.exists(exe_src):
        shutil.copy2(exe_src, exe_dest)
        print(f"  Copied {exe_name}")
    else:
        print(f"ERROR: Executable not found at {exe_src}")
        return False

    # Copy README
    readme_src = "README.md"
    if os.path.exists(readme_src):
        shutil.copy2(readme_src, os.path.join(dist_package_path, readme_src))
        print(f"  Copied {readme_src}")

    # Create user instructions file
    create_user_instructions(dist_package_path)

    # Create archive (zip for Windows, tar.gz for others)
    print(f"\nCreating archive: {dist_package_name}")
    if platform.system() == "Windows":
        # Create ZIP archive
        shutil.make_archive(
            os.path.join(DIST_DIR, dist_package_name),
            'zip',
            dist_package_path
        )
        print(f"  Created {dist_package_name}.zip")
    else:
        # Create TAR.GZ archive for Unix-like systems
        shutil.make_archive(
            os.path.join(DIST_DIR, dist_package_name),
            'gztar',
            dist_package_path
        )
        print(f"  Created {dist_package_name}.tar.gz")

    print(f"\nDistribution package ready at: {dist_package_path}")
    return True


def create_user_instructions(package_path):
    """Create a simple user instructions file."""
    instructions = """
SANCHO BROS - HOW TO PLAY
=========================

Thank you for downloading Sancho Bros!

QUICK START
-----------
1. Double-click the SanchoBros executable to start the game
2. Use arrow keys to move and jump
3. Press X or J to shoot (when powered up)
4. Collect Golden Arepas for power-ups!
5. Stomp on enemies or shoot them with lasers
6. Reach the goal flag at the end of each level

CONTROLS
--------
- Arrow Left/Right: Move left/right
- Arrow Up/Space: Jump
- X or J: Shoot laser (when powered up)
- ESC: Pause game / Return to menu
- F3: Toggle performance overlay (for debugging)

GAME FEATURES
-------------
- 5 exciting levels with Colombian themes
- Power-ups that give you laser shooting abilities
- Enemy stomping mechanics like classic platformers
- Score tracking and level completion times
- Save system to track your progress

SYSTEM REQUIREMENTS
-------------------
- Operating System: Windows, macOS, or Linux
- RAM: 512 MB minimum
- Disk Space: 100 MB
- Display: 800x600 or higher resolution

TROUBLESHOOTING
---------------
If the game doesn't start:
1. Make sure you have extracted all files from the archive
2. On macOS/Linux, you may need to mark the file as executable:
   chmod +x SanchoBros
3. Check that your system meets the minimum requirements
4. Try running from terminal/command prompt to see error messages

For more information, see the README.md file.

CREDITS
-------
Game Design & Development: Sancho Bros Team
Technology: Python with Pygame
Inspired by: Super Mario Bros

Enjoy the game!
"""

    instructions_path = os.path.join(package_path, "HOW_TO_PLAY.txt")
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write(instructions.strip())
    print(f"  Created HOW_TO_PLAY.txt")


def main():
    """Main build process."""
    print("=" * 60)
    print(f"SANCHO BROS - BUILD SCRIPT")
    print("=" * 60)

    # Check if PyInstaller is installed
    if not check_pyinstaller():
        sys.exit(1)

    # Clean previous builds
    clean_build_directories()

    # Build executable
    if not build_executable():
        print("\nBuild failed!")
        sys.exit(1)

    # Create distribution package
    if not create_distribution_package():
        print("\nPackaging failed!")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\nYour game is ready for distribution in the '{DIST_DIR}' folder.")
    print("Share the archive file with players!")


if __name__ == "__main__":
    main()
