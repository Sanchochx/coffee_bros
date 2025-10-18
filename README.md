# Sancho Bros

A 2D platformer game inspired by Super Mario Bros, featuring Colombian cultural themes. Guide Sancho through five exciting levels filled with challenges, enemies, and power-ups as you journey from Coffee Hills to the legendary El Pico del Café.

## Game Description

**Sancho Bros** is a classic 2D platformer that combines nostalgic gameplay with Colombian cultural elements. Play as Sancho, jump on enemies (Polochos), collect Golden Arepas for power-ups, and navigate through beautifully themed levels inspired by Colombia's coffee regions.

### Features

- **5 Unique Levels**: From tutorial Coffee Hills to the challenging El Pico del Café
- **Power-Up System**: Collect Golden Arepas to gain laser shooting abilities
- **Enemy Combat**: Stomp on Polochos or blast them with lasers
- **Lives System**: Start with 3 hearts and earn more through gameplay
- **Score Tracking**: Compete for high scores across levels
- **Save System**: Your progress is automatically saved
- **Settings**: Customizable music and sound effect volumes
- **Colombian Theme**: Enjoy cultural elements throughout the game

## Requirements

- **Python**: Version 3.7 or higher
- **Pygame**: Version 2.5.0 or higher

## Installation

### Step 1: Clone or Download the Repository

```bash
git clone <repository-url>
cd sancho_bros
```

### Step 2: Set Up Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install Pygame 2.5.0 and any other required packages.

## How to Run the Game

### Running the Game

Once dependencies are installed, run the game with:

```bash
python main.py
```

### Deactivating Virtual Environment

When you're done playing, deactivate the virtual environment:

```bash
deactivate
```

## Controls

### Basic Movement
- **Arrow Keys** or **A/D**: Move left/right
- **SPACE**: Jump
- **ESC**: Pause game / Return to menu

### Combat & Actions
- **X** or **J**: Shoot lasers (when powered up)

### Menu Navigation
- **Arrow Keys** or **W/S**: Navigate menu options
- **ENTER**: Select menu option

### Debug
- **F3**: Toggle performance overlay (shows FPS and performance metrics)

## Gameplay

### Objective
Complete all 5 levels by reaching the goal flag at the end of each level while collecting points and avoiding enemies.

### Levels
1. **Coffee Hills** - Tutorial level to learn the basics
2. **Mountain Paths** - Increased difficulty with more platforming
3. **Bean Valley** - Complex enemy patterns
4. **Harvest Heights** - Challenging vertical gameplay
5. **El Pico del Café** - Final level with ultimate challenges

### Scoring
- **Stomp Enemy**: 100 points
- **Laser Enemy**: 100 points
- **Collect Golden Arepa**: 200 points

### Power-Ups
- **Golden Arepa**: Grants Sancho the ability to shoot lasers for a limited time (indicated by golden color and timer)

### Lives System
- Start with 3 hearts
- Lose a heart when hit by enemies
- Game over when all hearts are lost
- Progress is saved automatically

## Credits and Attribution

### Development
- **Game Design & Development**: Created as a learning project
- **Inspired By**: Super Mario Bros (Nintendo)
- **Theme**: Colombian coffee culture

### Technology
- **Engine**: Pygame 2.5.0
- **Language**: Python 3.x
- **Development Tool**: Claude Code (claude.ai/code)

### Audio
- Sound effects and music generated using procedural audio synthesis

### Cultural Elements
- Colombian-themed levels and cultural references
- Spanish language elements (e.g., "¡Felicidades!", "¡Eres el mejor cafetero!")

## Project Structure

```
sancho_bros/
├── main.py                 # Main game entry point
├── config.py              # Game configuration and constants
├── requirements.txt       # Python dependencies
├── build.py               # Build script for creating executables
├── assets/               # Game assets (images, sounds)
│   ├── images/          # Sprite and background images
│   └── sounds/          # Sound effects and music
├── src/                 # Source code modules
│   ├── entities/        # Game entities (Player, Enemy, etc.)
│   ├── menu/           # Menu systems
│   └── ...             # Other game systems
└── context/            # Project documentation and user stories
```

## Building for Distribution

Want to share the game with friends who don't have Python installed? You can create a standalone executable!

### Quick Build

```bash
# Install build dependencies
pip install -r requirements.txt

# Run the build script
python build.py
```

The executable will be in the `dist/` folder, ready to share!

### For End Users (No Python Required)

If you received the game as a standalone executable:
1. Extract the downloaded archive
2. Double-click `SanchoBros.exe` (Windows) or `SanchoBros` (Mac/Linux)
3. Enjoy the game!

For detailed build instructions, see:
- `BUILD_INSTRUCTIONS.md` - Quick build guide
- `DISTRIBUTION_GUIDE.md` - Comprehensive distribution manual

## Troubleshooting

### Game won't start
- Ensure Python 3.7+ is installed: `python --version`
- Ensure Pygame is installed: `pip list | grep pygame`
- Try reinstalling dependencies: `pip install -r requirements.txt --force-reinstall`

### Performance issues
- Press F3 to view performance metrics
- Close other applications to free up system resources
- Reduce volume settings in the settings menu if audio is causing issues

### Sound not working
- Check that your system audio is not muted
- Adjust volume in the game's settings menu
- Verify Pygame mixer is working: `python -c "import pygame; pygame.mixer.init()"`

## License

This is an educational project created for learning purposes.

## Acknowledgments

Special thanks to the Pygame community for excellent documentation and examples that helped bring Sancho Bros to life.

---

**Enjoy the adventure and good luck reaching El Pico del Café!** ☕🎮
