"""
Sancho Bros - Game Configuration Constants
All game configuration values and constants.
"""

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Sancho Bros"

# Color constants
BLACK = (0, 0, 0)
YELLOW = (255, 209, 0)  # Colombian yellow for Sancho
GREEN = (34, 139, 34)  # Forest green for platforms
RED = (220, 20, 60)  # Crimson red for Polocho enemies

# Player constants
PLAYER_SPEED = 5  # pixels per frame
GRAVITY = 0.8  # pixels per frame² - acceleration due to gravity
TERMINAL_VELOCITY = 20  # pixels per frame - maximum fall speed
JUMP_VELOCITY = -15  # pixels per frame - initial upward velocity when jumping
JUMP_CUTOFF_VELOCITY = -3  # velocity threshold for variable jump height

# Enemy constants
ENEMY_SPEED = 2  # pixels per frame - patrol speed for enemies
