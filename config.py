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
PLAYER_STARTING_LIVES = 3  # number of lives player starts with
INVULNERABILITY_DURATION = 60  # frames (1 second at 60 FPS)
BLINK_INTERVAL = 5  # frames between blinks during invulnerability
KNOCKBACK_DISTANCE = 30  # pixels player is pushed when hit
KNOCKBACK_BOUNCE = -5  # upward velocity when hit

# Enemy constants
ENEMY_SPEED = 2  # pixels per frame - patrol speed for enemies

# Score constants
STOMP_SCORE = 100  # Points awarded for stomping an enemy

# Death and respawn constants
DEATH_DELAY = 120  # frames (2 seconds at 60 FPS) - delay before respawn after death
