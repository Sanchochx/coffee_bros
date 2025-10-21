# COFFEE BROS - USER STORIES

## Epic 1: Game Foundation and Core Mechanics

### US-001: Basic Game Window Setup
**As a** developer
**I want** to set up the basic game window and main loop
**So that** I have a foundation to build the game upon

**Acceptance Criteria:**
- [ ] Pygame is installed and imported successfully
- [ ] Game window opens at 800x600 resolution
- [ ] Window title displays "Coffee Bros"
- [ ] Game loop runs at consistent 60 FPS
- [ ] Window can be closed using the X button or ESC key
- [ ] Black background is displayed initially

**Technical Notes:**
- Use `pygame.init()` and `pygame.display.set_mode()`
- Implement FPS control with `pygame.time.Clock()`
- Handle `QUIT` event properly

---

### US-002: Player Character Creation
**As a** player
**I want** to see Coffee on screen
**So that** I can identify my character

**Acceptance Criteria:**
- [ ] Player sprite/rectangle is displayed on screen
- [ ] Player has initial spawn position (x=100, y=400)
- [ ] Player has visible dimensions (40x60 pixels)
- [ ] Player color/appearance is distinct from background
- [ ] Player renders on top of other game elements

**Technical Notes:**
- Create Player class extending `pygame.sprite.Sprite`
- Use placeholder colored rectangle initially
- Store position as (x, y) coordinates

---

### US-003: Basic Player Movement
**As a** player
**I want** to move Coffee left and right
**So that** I can navigate the level

**Acceptance Criteria:**
- [ ] Pressing LEFT arrow/A key moves player left at 5 pixels/frame
- [ ] Pressing RIGHT arrow/D key moves player right at 5 pixels/frame
- [ ] Player stops moving when key is released
- [ ] Player cannot move off-screen horizontally
- [ ] Movement is smooth and responsive
- [ ] Player can change direction instantly

**Technical Notes:**
- Implement keyboard input handling in update method
- Use `pygame.key.get_pressed()` for continuous input
- Clamp player position to screen boundaries

---

### US-004: Gravity System
**As a** player
**I want** Coffee to fall when not on solid ground
**So that** the game feels realistic

**Acceptance Criteria:**
- [ ] Player falls downward when in air
- [ ] Gravity acceleration is 0.8 pixels/frame²
- [ ] Terminal velocity caps at 20 pixels/frame downward
- [ ] Gravity applies continuously during gameplay
- [ ] Player falls smoothly without jittering

**Technical Notes:**
- Implement velocity_y variable
- Apply gravity each frame: `velocity_y += GRAVITY`
- Cap velocity: `velocity_y = min(velocity_y, TERMINAL_VELOCITY)`

---

### US-005: Jumping Mechanics
**As a** player
**I want** to make Coffee jump
**So that** I can navigate obstacles and platforms

**Acceptance Criteria:**
- [ ] Pressing UP/W/SPACE makes player jump when on ground
- [ ] Jump has initial upward velocity of -15 pixels/frame
- [ ] Player can only jump when touching a platform (no double-jump)
- [ ] Jump height varies based on how long button is held
- [ ] Releasing jump button early results in lower jump
- [ ] Jump feels responsive and natural

**Technical Notes:**
- Track `is_grounded` state
- Apply jump velocity when jump key pressed and grounded
- Implement variable jump by reducing upward velocity on key release

---

### US-006: Platform Creation
**As a** player
**I want** to see platforms in the level
**So that** I have surfaces to walk and jump on

**Acceptance Criteria:**
- [ ] Ground platform exists at bottom of screen
- [ ] Multiple floating platforms can be placed
- [ ] Platforms have defined position and size
- [ ] Platforms are visually distinct from background
- [ ] Platforms remain static (don't move)

**Technical Notes:**
- Create Platform class
- Store platforms in sprite group
- Define platform rectangles with (x, y, width, height)

---

### US-007: Platform Collision Detection
**As a** player
**I want** Coffee to land on and stand on platforms
**So that** I can navigate the level

**Acceptance Criteria:**
- [ ] Player lands on top of platforms when falling
- [ ] Player can walk along platform surfaces
- [ ] Player cannot pass through platforms from below
- [ ] Player cannot pass through platforms from sides
- [ ] Collision detection is precise with no gaps
- [ ] Player velocity stops when landing on platform

**Technical Notes:**
- Implement AABB collision detection
- Check collision separately for each axis (x, y)
- Set `velocity_y = 0` and `is_grounded = True` on landing
- Resolve collisions by adjusting player position

---

### US-008: Project Structure Setup
**As a** developer
**I want** to organize code into proper modules
**So that** the codebase is maintainable

**Acceptance Criteria:**
- [ ] `src/` directory contains all game modules
- [ ] `config.py` contains all game constants
- [ ] `main.py` serves as entry point
- [ ] Each class is in its own file
- [ ] `__init__.py` files exist in appropriate directories
- [ ] Code follows consistent naming conventions

**Technical Notes:**
- Follow project structure from implementation plan
- Use absolute imports where possible
- Keep config values separate from logic

---

## Epic 2: Enemies and Combat

### US-009: Enemy Creation (Polocho)
**As a** player
**I want** to see Polocho enemies in the level
**So that** I have challenges to overcome

**Acceptance Criteria:**
- [ ] Polocho enemies spawn at defined positions
- [ ] Enemies have visible sprite/rectangle (40x40 pixels)
- [ ] Enemies appear distinct from player and platforms
- [ ] Multiple enemies can exist simultaneously
- [ ] Enemies are affected by gravity

**Technical Notes:**
- Create Polocho class extending `pygame.sprite.Sprite`
- Store enemies in sprite group
- Apply physics to enemies similar to player

---

### US-010: Enemy Patrol Movement
**As a** player
**I want** enemies to move back and forth
**So that** they present a moving challenge

**Acceptance Criteria:**
- [ ] Enemies walk left and right automatically
- [ ] Each enemy has defined patrol boundaries
- [ ] Enemy turns around when reaching patrol boundary
- [ ] Enemy movement speed is consistent
- [ ] Enemies stay on platforms (don't walk off edges)
- [ ] Enemy can turn around when hitting walls

**Technical Notes:**
- Store `patrol_start` and `patrol_end` for each enemy
- Check boundaries each frame and reverse direction
- Movement speed: 2 pixels/frame

---

### US-011: Enemy Stomp Mechanic
**As a** player
**I want** to defeat enemies by jumping on their heads
**So that** I can clear my path

**Acceptance Criteria:**
- [ ] Jumping on enemy from above defeats the enemy
- [ ] Enemy displays "squashed" state briefly before disappearing
- [ ] Player bounces upward slightly after stomping
- [ ] Stomping plays a sound effect
- [ ] Score increases when enemy is defeated
- [ ] Enemy cannot damage player during stomp

**Technical Notes:**
- Check if player is falling (`velocity_y > 0`) during collision
- Check if player's bottom hits enemy's top half
- Apply small upward bounce: `player.velocity_y = -8`
- Remove enemy from game after squash animation

---

### US-012: Enemy Collision Damage
**As a** player
**I want** to lose a life when touching an enemy incorrectly
**So that** there are consequences for mistakes

**Acceptance Criteria:**
- [ ] Touching enemy from side damages player
- [ ] Touching enemy from below damages player
- [ ] Player loses one life when damaged
- [ ] Player briefly becomes invulnerable after taking damage (1 second)
- [ ] Player blinks during invulnerability period
- [ ] Damage sound effect plays
- [ ] Player is pushed back slightly when hit

**Technical Notes:**
- Implement invulnerability timer (60 frames at 60 FPS)
- Flash player sprite every 5 frames during invulnerability
- Prevent further damage while invulnerable

---

### US-013: Lives System
**As a** player
**I want** to have multiple lives
**So that** I have multiple chances to complete the level

**Acceptance Criteria:**
- [ ] Player starts with 3 lives
- [ ] Current lives are displayed on screen (HUD)
- [ ] Lives decrease when player takes damage
- [ ] Lives decrease when player falls in pit
- [ ] Game over occurs when lives reach 0
- [ ] Lives persist within the same level attempt

**Technical Notes:**
- Store lives count in player or game state
- Display lives as hearts or numeric value
- Trigger game over state when lives <= 0

---

### US-014: Death and Respawn
**As a** player
**I want** to respawn at the start when I die
**So that** I can retry the level

**Acceptance Criteria:**
- [ ] Death occurs when lives reach 0
- [ ] Player respawns at level start position
- [ ] Lives reset to starting amount (3)
- [ ] All enemies respawn in original positions
- [ ] All collected powerups respawn
- [ ] Brief death animation plays before respawn

**Technical Notes:**
- Store initial spawn positions for all entities
- Reset level state on death
- Add 1-2 second delay before respawn

---

### US-015: Pit/Fall Zones
**As a** player
**I want** to die when falling into pits
**So that** there are environmental hazards

**Acceptance Criteria:**
- [ ] Falling below screen bottom causes death
- [ ] Player loses one life when falling in pit
- [ ] Pit zones can be defined in level data
- [ ] Death is immediate upon entering pit zone
- [ ] Fall death sound effect plays

**Technical Notes:**
- Check if `player.y > SCREEN_HEIGHT`
- Can also define specific pit rectangles for mid-level pits
- Call player death method on pit collision

---

## Epic 3: Power-ups and Special Abilities

### US-016: Golden Arepa Spawning
**As a** player
**I want** to see the Golden Arepa powerup in the level
**So that** I can collect it

**Acceptance Criteria:**
- [ ] Golden Arepa appears at defined position
- [ ] Powerup has distinct golden/yellow appearance
- [ ] Powerup floats/hovers with animation
- [ ] Powerup is larger or more noticeable than other objects
- [ ] Multiple powerups can exist in a level

**Technical Notes:**
- Create GoldenArepa class extending `pygame.sprite.Sprite`
- Implement simple floating animation (sine wave motion)
- Size: approximately 30x30 pixels

---

### US-017: Powerup Collection
**As a** player
**I want** to collect the Golden Arepa by touching it
**So that** I gain its power

**Acceptance Criteria:**
- [ ] Walking into powerup collects it
- [ ] Powerup disappears when collected
- [ ] Collection sound effect plays
- [ ] Visual effect shows collection (sparkle/flash)
- [ ] Player enters powered-up state immediately
- [ ] Score increases when powerup collected

**Technical Notes:**
- Check collision between player and powerup sprites
- Remove powerup from sprite group on collection
- Call player's `collect_powerup()` method

---

### US-018: Powered-Up State
**As a** player
**I want** to know when I'm powered up
**So that** I know I can shoot lasers

**Acceptance Criteria:**
- [ ] Player appearance changes when powered up (glow/color change)
- [ ] Timer appears showing remaining powerup time
- [ ] Powered-up state lasts 10 seconds
- [ ] State automatically expires after timer ends
- [ ] Visual warning when powerup about to expire (last 3 seconds)
- [ ] Player returns to normal appearance after expiry

**Technical Notes:**
- Implement powerup timer (600 frames at 60 FPS)
- Add boolean flag `is_powered_up`
- Decrement timer each frame
- Flash player sprite when timer < 180 frames

---

### US-019: Laser Shooting Mechanic
**As a** player
**I want** to shoot laser beams while powered up
**So that** I can defeat enemies from a distance

**Acceptance Criteria:**
- [ ] Pressing X or J fires laser in facing direction
- [ ] Laser only fires when powered up
- [ ] Laser travels horizontally across screen
- [ ] Laser has visible projectile sprite/effect
- [ ] Shooting sound effect plays
- [ ] Can shoot multiple lasers rapidly (cooldown: 0.5 seconds)
- [ ] Lasers disappear when leaving screen

**Technical Notes:**
- Create Projectile class
- Store player's facing direction
- Laser speed: 10 pixels/frame
- Maximum 5 active projectiles at once
- Remove projectile when `x < 0` or `x > level_width`

---

### US-020: Laser-Enemy Collision
**As a** player
**I want** lasers to destroy enemies on contact
**So that** shooting is effective

**Acceptance Criteria:**
- [ ] Laser hitting enemy destroys the enemy
- [ ] Laser disappears after hitting enemy
- [ ] Enemy defeat sound effect plays
- [ ] Small explosion effect shows at impact point
- [ ] Score increases when enemy defeated by laser
- [ ] One laser can only hit one enemy

**Technical Notes:**
- Check collision between projectile and enemy sprites
- Remove both projectile and enemy on collision
- Award same points as stomp kill
- Create simple particle effect (optional)

---

## Epic 4: Level System and Progression

### US-021: Level Data Format
**As a** developer
**I want** to define levels using JSON files
**So that** levels are easy to create and modify

**Acceptance Criteria:**
- [ ] Level data is stored in JSON format
- [ ] JSON includes platforms, enemies, powerups, pits
- [ ] JSON specifies player spawn and goal positions
- [ ] JSON includes level metadata (name, size, background)
- [ ] Level files are located in `assets/levels/` directory
- [ ] JSON structure follows documented format

**Technical Notes:**
- Use Python's `json` module to load data
- Validate required fields when loading
- Handle missing or malformed JSON gracefully

---

### US-022: Level Loading System
**As a** developer
**I want** to load levels from JSON files
**So that** the game can create levels dynamically

**Acceptance Criteria:**
- [ ] Level class can load JSON file by level number
- [ ] All platforms are created from JSON data
- [ ] All enemies are spawned from JSON data
- [ ] All powerups are placed from JSON data
- [ ] Player spawns at correct position
- [ ] Loading errors are caught and reported

**Technical Notes:**
- Create Level class with `load_from_file()` method
- Parse JSON and instantiate game objects
- Store objects in appropriate sprite groups

---

### US-023: Level Goal/Completion
**As a** player
**I want** to reach a goal to complete the level
**So that** I can progress to the next level

**Acceptance Criteria:**
- [ ] Goal object/zone exists at end of level
- [ ] Goal is visually distinct (flag, door, etc.)
- [ ] Touching goal completes the level
- [ ] Level completion sound/music plays
- [ ] Completion screen shows before next level
- [ ] Score and time are displayed on completion

**Technical Notes:**
- Create goal as rectangle or sprite at level end
- Check collision between player and goal
- Transition to `LEVEL_COMPLETE` state
- Load next level after brief delay (2-3 seconds)

---

### US-024: Level 1 - Coffee Hills (Tutorial)
**As a** player
**I want** to play an introductory tutorial level
**So that** I can learn the game mechanics

**Acceptance Criteria:**
- [ ] Level is 3200 pixels wide
- [ ] Contains 5 Polochos with easy patrol patterns
- [ ] Contains 1 Golden Arepa for introduction
- [ ] Has simple platform layouts for learning jumping
- [ ] Has at least one small pit to introduce danger
- [ ] Completable in 1-2 minutes
- [ ] Background shows Colombian highlands theme

**Technical Notes:**
- Design level to gradually introduce mechanics
- Place powerup early so player learns shooting
- Keep enemy density low

---

### US-025: Level 2 - Mountain Paths
**As a** player
**I want** to play a level focused on platforming
**So that** I can practice precision jumping

**Acceptance Criteria:**
- [ ] Level is 4000 pixels wide
- [ ] Contains 8 Polochos
- [ ] Contains 2 Golden Arepas
- [ ] Features multiple floating platforms requiring precision
- [ ] Has wider gaps between platforms
- [ ] Includes some vertical platforming sections
- [ ] Difficulty is easy-medium

**Technical Notes:**
- Focus on platforming challenges over combat
- Place powerups to reward exploration
- Test all jumps are possible

---

### US-026: Level 3 - Bean Valley
**As a** player
**I want** to play a combat-focused level
**So that** I can master fighting enemies

**Acceptance Criteria:**
- [ ] Level is 4800 pixels wide
- [ ] Contains 12 Polochos placed close together
- [ ] Contains 2 Golden Arepas strategically placed
- [ ] Features sections with multiple enemies in succession
- [ ] Requires both stomping and shooting strategies
- [ ] Medium difficulty
- [ ] Includes some tight spaces with enemies

**Technical Notes:**
- Group enemies to create challenging sections
- Ensure powerups available when needed most
- Balance stomp-able vs shoot-able encounters

---

### US-027: Level 4 - Harvest Heights
**As a** player
**I want** to play a challenging combined level
**So that** I can use all my skills together

**Acceptance Criteria:**
- [ ] Level is 5000 pixels wide
- [ ] Contains 15 Polochos with complex patterns
- [ ] Contains 3 Golden Arepas
- [ ] Combines difficult platforming with dense enemies
- [ ] Requires strategic powerup usage
- [ ] Medium-hard difficulty
- [ ] Has multiple paths/routes to goal

**Technical Notes:**
- Design requires mastery of both platforming and combat
- Place enemies on platforms to combine challenges
- Include optional harder paths for skilled players

---

### US-028: Level 5 - El Pico del Café (Final)
**As a** player
**I want** to play an epic final level
**So that** I have a satisfying conclusion

**Acceptance Criteria:**
- [ ] Level is 6000 pixels wide (longest level)
- [ ] Contains 20 Polochos with challenging placement
- [ ] Contains 3 Golden Arepas
- [ ] Features most difficult platforming sections
- [ ] Combines all game mechanics learned
- [ ] Hard difficulty
- [ ] Has climactic feel with peak mountain background
- [ ] Victory screen shows after completion

**Technical Notes:**
- Design as culmination of all previous challenges
- Use full vertical space of level
- Create memorable final section before goal

---

### US-029: Level Transition Screen
**As a** player
**I want** to see my progress between levels
**So that** I feel a sense of advancement

**Acceptance Criteria:**
- [ ] Screen shows after completing level
- [ ] Displays level name and number
- [ ] Shows score earned in level
- [ ] Shows time taken to complete
- [ ] Shows "Press any key to continue" prompt
- [ ] Transitions to next level smoothly
- [ ] Plays transition music or fanfare

**Technical Notes:**
- Create UI screen with level stats
- Pause game state during transition
- Store completion time for display

---

### US-030: Victory Screen
**As a** player
**I want** to see a victory screen after beating all levels
**So that** I feel accomplished

**Acceptance Criteria:**
- [ ] Victory screen shows after Level 5 completion
- [ ] Displays total score across all levels
- [ ] Shows total time played
- [ ] Shows congratulations message
- [ ] Includes Colombian-themed celebration visuals
- [ ] Plays victory music
- [ ] Offers option to restart game or return to menu

**Technical Notes:**
- Track cumulative score and time
- Create dedicated victory state
- Allow player to restart from menu

---

## Epic 5: User Interface and HUD

### US-031: Score Display
**As a** player
**I want** to see my current score
**So that** I know how well I'm performing

**Acceptance Criteria:**
- [ ] Score is displayed in top-left or top-center of screen
- [ ] Score updates immediately when points earned
- [ ] Score is clearly readable (large, contrasting color)
- [ ] Score persists across level transitions
- [ ] Score format: "SCORE: 00000"

**Technical Notes:**
- Render text using `pygame.font`
- Update score for: enemy defeat (+100), powerup collection (+50), level completion (+500)
- Store score in game state

---

### US-032: Lives Display
**As a** player
**I want** to see my remaining lives
**So that** I know how many chances I have left

**Acceptance Criteria:**
- [ ] Lives displayed in top-right of screen
- [ ] Shows as hearts or "x3" format
- [ ] Updates immediately when life lost
- [ ] Remains visible at all times during gameplay
- [ ] Uses clear iconography or text

**Technical Notes:**
- Render hearts as sprites or text
- Position in corner to not obstruct gameplay
- Update when player takes damage

---

### US-033: Powerup Timer Display
**As a** player
**I want** to see how long my powerup lasts
**So that** I can plan my actions

**Acceptance Criteria:**
- [ ] Timer appears when powerup collected
- [ ] Shows remaining seconds in powered state
- [ ] Counts down in real-time
- [ ] Positioned near player or in HUD
- [ ] Changes color when timer low (warning)
- [ ] Disappears when powerup expires

**Technical Notes:**
- Convert frame timer to seconds for display
- Use different color when < 3 seconds remaining
- Position: top-center or near player

---

### US-034: Main Menu
**As a** player
**I want** to see a main menu when starting the game
**So that** I can choose to start or configure settings

**Acceptance Criteria:**
- [ ] Menu appears on game start
- [ ] Shows game title "Coffee Bros"
- [ ] Includes "Start Game" option
- [ ] Includes "Settings" option
- [ ] Includes "Quit" option
- [ ] Options are selectable with arrow keys and Enter
- [ ] Has Colombian-themed background
- [ ] Plays menu music

**Technical Notes:**
- Create menu state separate from gameplay
- Implement menu navigation with keyboard
- Transition to game state when Start selected

---

### US-035: Pause Menu
**As a** player
**I want** to pause the game
**So that** I can take breaks without losing progress

**Acceptance Criteria:**
- [ ] Pressing ESC pauses the game
- [ ] Game freezes (no updates) when paused
- [ ] Pause menu overlays game screen
- [ ] Shows "PAUSED" text
- [ ] Includes "Resume" option
- [ ] Includes "Restart Level" option
- [ ] Includes "Return to Menu" option
- [ ] Can unpause with ESC or selecting Resume

**Technical Notes:**
- Set game state to `PAUSED`
- Stop updating game entities while paused
- Darken/dim background for pause overlay

---

### US-036: Game Over Screen
**As a** player
**I want** to see a game over screen when I run out of lives
**So that** I understand I've failed and can retry

**Acceptance Criteria:**
- [ ] "GAME OVER" text displays prominently
- [ ] Shows final score
- [ ] Includes "Retry Level" option
- [ ] Includes "Return to Menu" option
- [ ] Plays game over music/sound
- [ ] Prevents accidental immediate retry (brief delay)

**Technical Notes:**
- Create game over state
- Allow player to restart current level or return to menu
- Reset score on restart

---

### US-037: Level Name Display
**As a** player
**I want** to see the level name when starting a level
**So that** I know which level I'm playing

**Acceptance Criteria:**
- [ ] Level name displays briefly at level start
- [ ] Shows level number and name (e.g., "Level 1 - Coffee Hills")
- [ ] Appears for 2-3 seconds then fades
- [ ] Centered on screen
- [ ] Doesn't block important gameplay elements

**Technical Notes:**
- Display as overlay at level start
- Use fade-in/fade-out animation
- Remove after timer expires

---

## Epic 6: Camera and Viewport

### US-038: Scrolling Camera Implementation
**As a** player
**I want** the camera to follow Coffee
**So that** I can see where I'm going in large levels

**Acceptance Criteria:**
- [ ] Camera follows player horizontally
- [ ] Camera scrolls when player passes screen center
- [ ] Camera doesn't scroll beyond level boundaries
- [ ] Camera movement is smooth (no sudden jumps)
- [ ] Camera doesn't show areas outside level bounds
- [ ] Vertical scrolling not needed (levels fit in screen height)

**Technical Notes:**
- Create Camera class to manage viewport offset
- Calculate camera position based on player position
- Clamp camera to `[0, level_width - SCREEN_WIDTH]`
- All rendering positions offset by camera position

---

### US-039: Camera Boundaries
**As a** developer
**I want** the camera to stay within level bounds
**So that** no empty space is visible

**Acceptance Criteria:**
- [ ] Camera cannot scroll past left edge of level (x=0)
- [ ] Camera cannot scroll past right edge of level
- [ ] Scrolling stops smoothly at boundaries
- [ ] Player can still move near level edges
- [ ] No black bars or empty space visible

**Technical Notes:**
- Calculate max camera offset: `level.width - SCREEN_WIDTH`
- Clamp camera offset each frame
- Test with levels of different widths

---

## Epic 7: Audio System

### US-040: Sound Effects System
**As a** developer
**I want** to implement sound effect playback
**So that** game actions have audio feedback

**Acceptance Criteria:**
- [ ] Sound effects can be loaded from files
- [ ] Sounds play when triggered by events
- [ ] Multiple sounds can play simultaneously
- [ ] Sound volume is adjustable
- [ ] Missing sound files don't crash game
- [ ] Sounds are in appropriate format (WAV)

**Technical Notes:**
- Use `pygame.mixer` for audio
- Create audio manager class
- Load all sounds at game start
- Handle file not found errors gracefully

---

### US-041: Jump Sound Effect
**As a** player
**I want** to hear a sound when Coffee jumps
**So that** jumping feels responsive

**Acceptance Criteria:**
- [ ] Sound plays every time player jumps
- [ ] Sound is short and snappy (< 0.5 seconds)
- [ ] Sound doesn't overlap itself awkwardly
- [ ] Volume is balanced with other sounds

**Technical Notes:**
- Play sound in player's `jump()` method
- Use whoosh or boing sound effect

---

### US-042: Stomp Sound Effect
**As a** player
**I want** to hear a sound when stomping enemies
**So that** I get satisfying combat feedback

**Acceptance Criteria:**
- [ ] Sound plays when enemy is stomped
- [ ] Sound is distinct from other combat sounds
- [ ] Sound is satisfying (squish/pop style)

**Technical Notes:**
- Play in enemy's `get_stomped()` method
- Use squish or pop sound effect

---

### US-043: Laser Shoot Sound Effect
**As a** player
**I want** to hear a sound when shooting lasers
**So that** shooting feels impactful

**Acceptance Criteria:**
- [ ] Sound plays each time laser is fired
- [ ] Sound is sci-fi/energy beam style
- [ ] Sound doesn't overlap muddy when rapid-firing
- [ ] Volume is appropriate

**Technical Notes:**
- Play in player's `shoot()` method
- Use laser zap or pew sound effect

---

### US-044: Powerup Collection Sound
**As a** player
**I want** to hear a sound when collecting Golden Arepa
**So that** collection feels rewarding

**Acceptance Criteria:**
- [ ] Sound plays when powerup is collected
- [ ] Sound is positive and rewarding (chime/sparkle)
- [ ] Sound is longer and more prominent than other effects
- [ ] Sound conveys "special item" feeling

**Technical Notes:**
- Play when powerup collected
- Use magical chime or power-up jingle

---

### US-045: Death Sound Effect
**As a** player
**I want** to hear a sound when Coffee dies
**So that** failure is clearly communicated

**Acceptance Criteria:**
- [ ] Sound plays when player takes fatal damage
- [ ] Sound is descending or sad tone
- [ ] Sound doesn't play during invulnerability
- [ ] Sound is distinct from damage sound

**Technical Notes:**
- Play in player's death method
- Use descending tone or "ouch" sound

---

### US-046: Level Complete Sound
**As a** player
**I want** to hear music when completing a level
**So that** success feels rewarding

**Acceptance Criteria:**
- [ ] Fanfare plays when reaching goal
- [ ] Sound is triumphant and celebratory
- [ ] Sound plays fully before transition
- [ ] Background music stops when fanfare plays

**Technical Notes:**
- Play when level goal reached
- Use victory fanfare (2-4 seconds)
- Stop level music before playing

---

### US-047: Background Music
**As a** player
**I want** to hear music during gameplay
**So that** the game has atmosphere

**Acceptance Criteria:**
- [ ] Different music for menu and gameplay
- [ ] Music loops seamlessly
- [ ] Music volume is adjustable
- [ ] Music doesn't overpower sound effects
- [ ] Music can be muted in settings
- [ ] Music matches Colombian/upbeat theme

**Technical Notes:**
- Use `pygame.mixer.music` for background tracks
- Load OGG format for better compression
- Set music volume lower than SFX (0.3-0.5)

---

## Epic 8: Visual Polish and Animation

### US-048: Player Animation - Walking
**As a** player
**I want** to see Coffee's walking animation
**So that** movement looks natural

**Acceptance Criteria:**
- [ ] Walking animation plays when moving left/right
- [ ] Animation cycles through frames smoothly
- [ ] Animation speed matches movement speed
- [ ] Character faces correct direction
- [ ] Animation stops when player stops moving

**Technical Notes:**
- Load sprite sheet with walk frames
- Cycle through frames based on timer
- Flip sprite horizontally for left/right directions
- 6 frames for walk cycle

---

### US-049: Player Animation - Jumping
**As a** player
**I want** to see Coffee's jump animation
**So that** jumping looks dynamic

**Acceptance Criteria:**
- [ ] Jump animation shows when player in air
- [ ] Different frames for ascending vs descending
- [ ] Transitions smoothly from walk to jump
- [ ] Lands with appropriate frame

**Technical Notes:**
- Use jump frame when `velocity_y < 0` (going up)
- Use fall frame when `velocity_y > 0` (falling)
- 2 frames needed (jump, fall)

---

### US-050: Player Animation - Idle
**As a** player
**I want** to see Coffee's idle animation when standing still
**So that** the character feels alive

**Acceptance Criteria:**
- [ ] Idle animation plays when not moving
- [ ] Animation is subtle (breathing, blinking)
- [ ] Loops seamlessly
- [ ] Doesn't distract from gameplay

**Technical Notes:**
- Use 4-frame idle animation
- Slower cycle speed than walk (animate every 10-15 frames)

---

### US-051: Player Animation - Shooting
**As a** player
**I want** to see Coffee's shooting animation
**So that** firing lasers looks cool

**Acceptance Criteria:**
- [ ] Shooting animation plays when firing
- [ ] Shows laser emanating from hands
- [ ] Animation is brief (returns to normal quickly)
- [ ] Can play while walking or standing
- [ ] Faces correct direction

**Technical Notes:**
- 4-frame shooting animation
- Play once per shot, then return to idle/walk
- Show for 10-15 frames total

---

### US-052: Enemy Animation - Walking
**As a** player
**I want** to see Polochos walking
**So that** enemies look animated

**Acceptance Criteria:**
- [ ] Walking animation plays continuously
- [ ] Animation cycles smoothly
- [ ] Enemies face movement direction
- [ ] Animation speed matches movement speed

**Technical Notes:**
- 4-frame walk cycle for Polocho
- Flip sprite based on direction
- Animate every 8-10 frames

---

### US-053: Enemy Animation - Squashed
**As a** player
**I want** to see enemies get squashed when stomped
**So that** defeating them is satisfying

**Acceptance Criteria:**
- [ ] Squashed sprite shows when enemy defeated
- [ ] Sprite is flattened/compressed vertically
- [ ] Shows briefly before enemy disappears
- [ ] Clearly conveys defeat

**Technical Notes:**
- Single squashed frame
- Display for 10-15 frames before removal
- Reduce height, increase width for squash effect

---

### US-054: Powerup Animation - Floating
**As a** player
**I want** to see the Golden Arepa floating
**So that** it's attractive and noticeable

**Acceptance Criteria:**
- [ ] Powerup bobs up and down smoothly
- [ ] Animation is continuous loop
- [ ] Movement is subtle (not distracting)
- [ ] Easy to spot in level

**Technical Notes:**
- Use sine wave for vertical position offset
- Amplitude: 10 pixels
- Speed: slow (0.05 radians/frame)
- Optional: add rotation

---

### US-055: Powerup Animation - Glowing
**As a** player
**I want** to see the Golden Arepa glowing
**So that** it looks special and magical

**Acceptance Criteria:**
- [ ] Powerup has glowing effect
- [ ] Glow pulses smoothly
- [ ] Effect draws attention without being garish
- [ ] Animation loops seamlessly

**Technical Notes:**
- 6-frame glow animation
- Vary alpha/brightness of outer glow
- Cycle through frames every 5-8 frames

---

### US-056: Background Graphics
**As a** player
**I want** to see themed backgrounds
**So that** levels have atmosphere

**Acceptance Criteria:**
- [ ] Each level has appropriate background image
- [ ] Backgrounds show Colombian highlands theme
- [ ] Backgrounds don't interfere with gameplay visibility
- [ ] Images are high quality and attractive
- [ ] Sky, mountains, and coffee plants visible

**Technical Notes:**
- Load background image per level from JSON
- Render behind all game objects
- Scale to screen size if needed
- Use parallax scrolling (optional enhancement)

---

### US-057: Platform/Tile Graphics
**As a** player
**I want** to see textured platforms
**So that** levels look polished

**Acceptance Criteria:**
- [ ] Platforms have earth/stone texture
- [ ] Tiles connect seamlessly
- [ ] Different platform types have different appearances
- [ ] Graphics don't obscure platform boundaries

**Technical Notes:**
- Create 50x50 pixel tile sprites
- Use tiling system for larger platforms
- Ground platforms vs floating platforms distinct

---

### US-058: Particle Effects - Stomping
**As a** player
**I want** to see particles when stomping enemies
**So that** combat feels impactful

**Acceptance Criteria:**
- [ ] Small particles emit when enemy stomped
- [ ] Particles spread outward from impact point
- [ ] Particles fade out over time
- [ ] Effect is brief and doesn't lag game

**Technical Notes:**
- Create 5-10 small particle sprites
- Give random velocities outward
- Remove after 20-30 frames
- Use simple colored squares/circles

---

### US-059: Particle Effects - Powerup Collection
**As a** player
**I want** to see sparkles when collecting powerup
**So that** collection feels special

**Acceptance Criteria:**
- [ ] Sparkle effect appears at collection point
- [ ] Effect is bright and noticeable
- [ ] Particles rise and fade out
- [ ] Effect conveys "power acquired" feeling

**Technical Notes:**
- Create sparkle/star particles
- Move upward with fade
- Yellow/gold colors
- Display for 30-45 frames

---

## Epic 9: Settings and Configuration

### US-060: Settings Menu
**As a** player
**I want** to adjust game settings
**So that** I can customize my experience

**Acceptance Criteria:**
- [ ] Settings accessible from main menu
- [ ] Settings accessible from pause menu
- [ ] Shows current setting values
- [ ] Changes take effect immediately
- [ ] Can return to previous menu

**Technical Notes:**
- Create settings state/screen
- Store settings in config or save file
- Apply settings when changed

---

### US-061: Volume Controls
**As a** player
**I want** to control music and sound volume
**So that** audio suits my preference

**Acceptance Criteria:**
- [ ] Separate sliders for music and SFX volume
- [ ] Volume range: 0-100%
- [ ] Changes apply immediately
- [ ] Settings persist between sessions
- [ ] Can mute completely (0%)

**Technical Notes:**
- Use slider or percentage display
- Apply to `pygame.mixer.music.set_volume()` and sound volumes
- Save to config file

---

### US-062: Controls Display
**As a** player
**I want** to see the control scheme
**So that** I know how to play

**Acceptance Criteria:**
- [ ] Shows all keyboard controls
- [ ] Accessible from menu or pause screen
- [ ] Clear visual representation of keys
- [ ] Lists all actions (move, jump, shoot, pause)

**Technical Notes:**
- Create help/controls screen
- Display text or icons for keys
- Include controller info if implemented

---

## Epic 10: Testing and Quality Assurance

### US-063: Performance Optimization
**As a** developer
**I want** the game to run smoothly
**So that** players have good experience

**Acceptance Criteria:**
- [ ] Game maintains 60 FPS consistently
- [ ] No frame drops during normal gameplay
- [ ] Memory usage is stable (no leaks)
- [ ] Loading times are minimal (< 2 seconds per level)
- [ ] Works on mid-range hardware

**Technical Notes:**
- Profile code to find bottlenecks
- Optimize collision detection (spatial partitioning if needed)
- Limit active particles
- Preload all assets at start

---

### US-064: Collision Testing
**As a** QA tester
**I want** to verify collision detection works correctly
**So that** gameplay is fair and bug-free

**Acceptance Criteria:**
- [ ] Player never falls through platforms
- [ ] Player cannot clip through walls
- [ ] Stomp detection is accurate
- [ ] Damage detection is accurate
- [ ] Projectile collision is precise
- [ ] No collision bugs in any level

**Technical Notes:**
- Write unit tests for collision functions
- Test edge cases (corners, multiple collisions)
- Playtest all levels thoroughly

---

### US-065: Level Completability Testing
**As a** QA tester
**I want** to verify all levels can be completed
**So that** game is fair and not broken

**Acceptance Criteria:**
- [ ] All 5 levels can be completed
- [ ] No impossible jumps exist
- [ ] No soft-lock situations possible
- [ ] All powerups are reachable
- [ ] Goal is always accessible

**Technical Notes:**
- Playtest each level multiple times
- Test with and without powerups
- Verify all gaps are jumpable
- Check minimum required skills

---

### US-066: Edge Case Testing
**As a** QA tester
**I want** to test unusual scenarios
**So that** the game handles edge cases gracefully

**Acceptance Criteria:**
- [ ] Multiple simultaneous collisions handled
- [ ] Powerup expiry during shooting handled
- [ ] Death during invulnerability prevented
- [ ] Pausing during transitions works
- [ ] Rapid input doesn't break game
- [ ] Boundary conditions tested (edges, corners)

**Technical Notes:**
- Create test cases for known edge cases
- Attempt to break game with unusual inputs
- Fix any crashes or unexpected behavior

---

### US-067: Cross-Platform Testing
**As a** developer
**I want** to test on different operating systems
**So that** game works for all players

**Acceptance Criteria:**
- [ ] Game runs on Windows
- [ ] Game runs on macOS
- [ ] Game runs on Linux
- [ ] Controls work on all platforms
- [ ] File paths work on all platforms
- [ ] Performance is acceptable on all platforms

**Technical Notes:**
- Use os-agnostic path handling (`os.path.join`)
- Test keyboard input on different keyboards
- Verify pygame compatibility

---

### US-068: Save Progress System (Optional)
**As a** player
**I want** my progress to be saved
**So that** I can continue later

**Acceptance Criteria:**
- [ ] Highest completed level is saved
- [ ] High score is saved
- [ ] Settings preferences are saved
- [ ] Save persists between game sessions
- [ ] Save file is human-readable (JSON)

**Technical Notes:**
- Save to JSON file in user directory
- Load on game start
- Save on level completion and game exit
- Handle missing save file gracefully

---

## Epic 11: Documentation and Deployment

### US-069: README Documentation
**As a** developer or user
**I want** clear README documentation
**So that** I understand how to run and play the game

**Acceptance Criteria:**
- [ ] README includes game description
- [ ] Installation instructions included
- [ ] How to run the game explained
- [ ] Controls listed
- [ ] Requirements specified (Python version, Pygame)
- [ ] Credits and attribution included

**Technical Notes:**
- Create comprehensive README.md
- Include setup instructions for virtual environment
- Add screenshots (optional but nice)

---

### US-070: Code Documentation
**As a** developer
**I want** well-documented code
**So that** the codebase is maintainable

**Acceptance Criteria:**
- [ ] All classes have docstrings
- [ ] All public methods have docstrings
- [ ] Complex algorithms are commented
- [ ] Config constants are explained
- [ ] Code follows PEP 8 style guidelines

**Technical Notes:**
- Use Google or NumPy docstring format
- Comment "why" not just "what"
- Keep comments up-to-date with code

---

### US-071: Requirements File
**As a** developer
**I want** a requirements.txt file
**So that** dependencies are clear

**Acceptance Criteria:**
- [ ] requirements.txt lists all dependencies
- [ ] Version constraints are specified
- [ ] File is in project root
- [ ] `pip install -r requirements.txt` works

**Technical Notes:**
- Include pygame version
- Can generate with `pip freeze > requirements.txt`
- Specify minimum versions with >=

---

### US-072: Game Distribution
**As a** developer
**I want** to package the game for distribution
**So that** non-technical users can play

**Acceptance Criteria:**
- [ ] Game can run without Python installation (optional)
- [ ] All assets are included in distribution
- [ ] Clear instructions for end users
- [ ] Executable created for target platforms (optional)

**Technical Notes:**
- Use PyInstaller or similar for standalone executables
- Include all asset files in package
- Test on clean system without Python

---

## Summary Statistics

**Total User Stories:** 72
**Total Epics:** 11

**Epic Breakdown:**
- Epic 1: Foundation - 8 stories
- Epic 2: Enemies - 7 stories
- Epic 3: Power-ups - 5 stories
- Epic 4: Level System - 10 stories
- Epic 5: UI/HUD - 7 stories
- Epic 6: Camera - 2 stories
- Epic 7: Audio - 7 stories
- Epic 8: Visuals - 12 stories
- Epic 9: Settings - 3 stories
- Epic 10: Testing - 6 stories
- Epic 11: Documentation - 4 stories

**Estimated Implementation Order:**
1. Foundation stories (US-001 to US-008)
2. Core gameplay (US-009 to US-015)
3. Power-ups (US-016 to US-020)
4. Level system (US-021 to US-030)
5. UI elements (US-031 to US-037)
6. Camera (US-038 to US-039)
7. Audio (US-040 to US-047)
8. Visual polish (US-048 to US-059)
9. Settings (US-060 to US-062)
10. Testing (US-063 to US-068)
11. Documentation (US-069 to US-072)

---

**Prioritization Legend:**
- **Must Have:** Critical for basic gameplay (stories in Epics 1-4)
- **Should Have:** Important for polish (stories in Epics 5-8)
- **Nice to Have:** Enhancement features (stories in Epic 9, US-068)
- **Future:** Post-launch improvements (marked as optional)
