"""
Sancho Bros - Main Game Entry Point
A 2D platformer game inspired by Super Mario Bros with Colombian cultural themes.
"""

import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE, BLACK, STOMP_SCORE, DEATH_DELAY, PLAYER_STARTING_LIVES, POWERUP_SCORE, MAX_LASERS, LEVEL_COMPLETE_DELAY
from src.entities import Player, Platform, Polocho, GoldenArepa, Laser, Goal
from src.level import Level
from src.menu import MainMenu, PauseMenu, GameOverMenu
from src.level_name_display import LevelNameDisplay
from src.audio_manager import AudioManager


def main():
    """Main game function"""
    # Initialize pygame
    pygame.init()

    # Create game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # Create clock for FPS control
    clock = pygame.time.Clock()

    # Initialize audio manager (US-040, US-041)
    audio_manager = AudioManager()

    # Game state management (US-034, US-035, US-036)
    game_state = "menu"  # Possible states: "menu", "playing", "paused", "settings", "game_over"
    main_menu = MainMenu()  # Initialize main menu
    pause_menu = PauseMenu()  # Initialize pause menu (US-035)
    game_over_menu = GameOverMenu()  # Initialize game over menu (US-036)

    # Initialize game state
    score = 0
    font = pygame.font.Font(None, 36)  # Default font, size 36
    current_level_number = 1  # Start with level 1 (US-025)
    max_level_number = 5  # Maximum level implemented (US-028)

    # Time tracking (for completion screen)
    level_start_time = pygame.time.get_ticks()  # milliseconds since pygame.init()
    level_start_score = 0  # Score at level start (for transition screen - US-029)

    # Death and respawn state
    is_dead = False
    death_timer = 0

    # Level completion state (US-023)
    is_level_complete = False
    completion_timer = 0
    completion_time = 0  # Time taken to complete level (in seconds)

    # Level transition state (US-029)
    is_transition_screen = False
    score_earned_in_level = 0  # Score earned specifically in completed level

    # Victory screen state (US-030)
    is_victory_screen = False
    total_game_time = 0  # Total time played across all levels (in seconds)

    # Camera system (US-038, US-039)
    camera_x = 0  # Camera horizontal offset for scrolling

    # Level name display (US-037)
    level_name_display = None

    # Level and entity references (initialized when game starts - US-034)
    level = None
    player = None
    all_sprites = None
    platforms = None
    enemies = None
    powerups = None
    goals = None
    lasers = pygame.sprite.Group()  # Create laser sprite group (US-019)

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle ESC key based on game state
                if event.key == pygame.K_ESCAPE:
                    print(f"ESC pressed! Current game state: {game_state}")
                    if game_state == "playing":
                        # ESC pauses the game (US-035)
                        game_state = "paused"
                        print("Game paused")
                        continue  # Skip rest of event handling to prevent pause menu from handling same event
                    elif game_state == "paused":
                        # ESC unpauses the game (US-035)
                        game_state = "playing"
                        print("Game resumed")
                        continue  # Skip rest of event handling
                    elif game_state == "menu":
                        # ESC quits from main menu
                        running = False
                    elif game_state == "settings":
                        # ESC returns to menu from settings
                        game_state = "menu"

            # Handle menu input when in menu state (US-034)
            if game_state == "menu":
                menu_action = main_menu.handle_input(event)
                if menu_action == "start":
                    # Start game - load first level
                    game_state = "playing"
                    current_level_number = 1
                    score = 0
                    total_game_time = 0
                    # Load level from JSON file (US-022, US-041)
                    try:
                        level = Level.load_from_file(current_level_number, audio_manager)
                        # Get references to level entities for easy access
                        player = level.player
                        all_sprites = level.all_sprites
                        platforms = level.platforms
                        enemies = level.enemies
                        powerups = level.powerups
                        goals = level.goals
                        lasers.empty()  # Clear any existing lasers
                        # Reset all game state flags
                        is_dead = False
                        is_level_complete = False
                        is_transition_screen = False
                        is_victory_screen = False
                        death_timer = 0
                        completion_timer = 0
                        camera_x = 0
                        level_start_time = pygame.time.get_ticks()
                        level_start_score = 0
                        # Create level name display (US-037)
                        level_name = level.metadata.get("name", f"Level {current_level_number}")
                        level_name_display = LevelNameDisplay(current_level_number, level_name)
                        # TODO (US-047): Stop menu music, start gameplay music (audio system in Epic 7)
                    except (FileNotFoundError, ValueError) as e:
                        print(f"Error loading level: {e}")
                        running = False
                elif menu_action == "settings":
                    # Go to settings (US-060: Settings Menu - for future)
                    game_state = "settings"
                    # TODO (US-060): Implement settings screen
                elif menu_action == "quit":
                    # Quit game
                    running = False
                # Skip rest of event handling when in menu
                continue

            # Handle pause menu input when in paused state (US-035)
            if game_state == "paused":
                menu_action = pause_menu.handle_input(event)
                if menu_action == "resume":
                    # Resume gameplay
                    game_state = "playing"
                elif menu_action == "restart":
                    # Restart current level
                    try:
                        level = Level.load_from_file(current_level_number, audio_manager)
                        # Get fresh references to level entities
                        player = level.player
                        all_sprites = level.all_sprites
                        platforms = level.platforms
                        enemies = level.enemies
                        powerups = level.powerups
                        goals = level.goals
                        lasers.empty()  # Clear all lasers
                        # Reset all state flags
                        is_dead = False
                        is_level_complete = False
                        is_transition_screen = False
                        completion_timer = 0
                        death_timer = 0
                        # Reset time tracking for restarted level
                        level_start_time = pygame.time.get_ticks()
                        # Keep current score (don't reset on restart)
                        # Reset camera
                        camera_x = 0
                        # Create level name display (US-037)
                        level_name = level.metadata.get("name", f"Level {current_level_number}")
                        level_name_display = LevelNameDisplay(current_level_number, level_name)
                        # Return to playing state
                        game_state = "playing"
                    except (FileNotFoundError, ValueError) as e:
                        print(f"Error restarting level {current_level_number}: {e}")
                        running = False
                elif menu_action == "menu":
                    # Return to main menu
                    game_state = "menu"
                    # Reset pause menu selection
                    pause_menu.selected_index = 0
                # Skip rest of event handling when in pause menu
                continue

            # Handle game over menu input when in game over state (US-036)
            if game_state == "game_over":
                menu_action = game_over_menu.handle_input(event)
                if menu_action == "retry":
                    # Retry current level - reload it completely
                    try:
                        level = Level.load_from_file(current_level_number, audio_manager)
                        # Get fresh references to level entities
                        player = level.player
                        all_sprites = level.all_sprites
                        platforms = level.platforms
                        enemies = level.enemies
                        powerups = level.powerups
                        goals = level.goals
                        lasers.empty()  # Clear all lasers
                        # Reset all state flags
                        is_dead = False
                        is_level_complete = False
                        is_transition_screen = False
                        completion_timer = 0
                        death_timer = 0
                        # Reset time tracking for restarted level
                        level_start_time = pygame.time.get_ticks()
                        # Reset score to 0 on game over retry (US-036 technical notes)
                        score = 0
                        level_start_score = 0
                        # Reset camera
                        camera_x = 0
                        # Create level name display (US-037)
                        level_name = level.metadata.get("name", f"Level {current_level_number}")
                        level_name_display = LevelNameDisplay(current_level_number, level_name)
                        # Return to playing state
                        game_state = "playing"
                    except (FileNotFoundError, ValueError) as e:
                        print(f"Error retrying level {current_level_number}: {e}")
                        running = False
                elif menu_action == "menu":
                    # Return to main menu
                    game_state = "menu"
                    # Reset game over menu selection
                    game_over_menu.selected_index = 0
                # Skip rest of event handling when in game over menu
                continue

            # Gameplay event handling (only when in playing state)
            if game_state == "playing" and event.type == pygame.KEYDOWN:
                # Handle transition screen continuation (US-029)
                if is_transition_screen:
                    # Any key press continues to next level
                    # Check if there's a next level available
                    if current_level_number < max_level_number:
                        # Load next level
                        current_level_number += 1
                        try:
                            level = Level.load_from_file(current_level_number, audio_manager)
                            # Get fresh references to level entities
                            player = level.player
                            all_sprites = level.all_sprites
                            platforms = level.platforms
                            enemies = level.enemies
                            powerups = level.powerups
                            goals = level.goals
                            lasers.empty()  # Clear all lasers from previous level
                            # Reset completion and transition state
                            is_level_complete = False
                            is_transition_screen = False
                            completion_timer = 0
                            # Reset time tracking for new level
                            level_start_time = pygame.time.get_ticks()
                            level_start_score = score  # Record starting score for next level
                            # Reset camera for new level (US-038)
                            camera_x = 0
                            # Create level name display (US-037)
                            level_name = level.metadata.get("name", f"Level {current_level_number}")
                            level_name_display = LevelNameDisplay(current_level_number, level_name)
                            # Score carries over between levels
                        except (FileNotFoundError, ValueError) as e:
                            print(f"Error loading level {current_level_number}: {e}")
                            running = False
                    else:
                        # No more levels - show victory screen! (US-030)
                        is_transition_screen = False
                        is_victory_screen = True
                        # total_game_time already includes all level times from transition screens
                        # TODO (US-047): Play victory music (audio system in Epic 7)
                # Handle victory screen options (US-030)
                elif is_victory_screen:
                    if event.key == pygame.K_r:
                        # Restart game from Level 1
                        current_level_number = 1
                        score = 0
                        total_game_time = 0
                        try:
                            level = Level.load_from_file(current_level_number, audio_manager)
                            # Get fresh references to level entities
                            player = level.player
                            all_sprites = level.all_sprites
                            platforms = level.platforms
                            enemies = level.enemies
                            powerups = level.powerups
                            goals = level.goals
                            lasers.empty()  # Clear all lasers
                            # Reset all state flags
                            is_victory_screen = False
                            is_level_complete = False
                            is_transition_screen = False
                            is_dead = False
                            completion_timer = 0
                            death_timer = 0
                            # Reset time tracking
                            level_start_time = pygame.time.get_ticks()
                            level_start_score = 0
                            # Reset camera (US-038)
                            camera_x = 0
                            # Create level name display (US-037)
                            level_name = level.metadata.get("name", f"Level {current_level_number}")
                            level_name_display = LevelNameDisplay(current_level_number, level_name)
                        except (FileNotFoundError, ValueError) as e:
                            print(f"Error loading level 1: {e}")
                            running = False
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        # Quit game
                        running = False

        # Update and draw based on game state (US-034, US-035)
        if game_state == "menu":
            # Menu state - update and draw menu
            main_menu.update()
            main_menu.draw(screen)
            # Update display
            pygame.display.flip()
            clock.tick(FPS)
            continue  # Skip gameplay logic

        # Paused state - freeze game and show pause menu (US-035)
        if game_state == "paused":
            # Don't update any game entities - game is frozen!
            # Just draw the current game state with pause overlay on top

            # Fill screen with black background
            screen.fill(BLACK)

            # Draw all sprites at their frozen positions with camera offset
            for sprite in all_sprites:
                offset_rect = sprite.rect.copy()
                offset_rect.x -= camera_x
                screen.blit(sprite.image, offset_rect)

            # Draw HUD elements (so player can see their current state)
            score_text = font.render(f"SCORE: {score:05d}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            lives_text = font.render(f"x{player.lives}", True, (255, 255, 255))
            lives_rect = lives_text.get_rect()
            lives_rect.topright = (WINDOW_WIDTH - 10, 10)
            screen.blit(lives_text, lives_rect)

            if player.is_powered_up:
                powerup_seconds = player.powerup_timer / 60
                if powerup_seconds < 3.0:
                    timer_color = (255, 50, 50)
                else:
                    timer_color = (255, 215, 0)
                timer_text = font.render(f"POWERUP: {powerup_seconds:.1f}s", True, timer_color)
                timer_rect = timer_text.get_rect()
                timer_rect.centerx = WINDOW_WIDTH // 2
                timer_rect.top = 10
                screen.blit(timer_text, timer_rect)

            # Draw pause menu overlay on top
            pause_menu.draw(screen)

            # Update display
            pygame.display.flip()
            clock.tick(FPS)
            continue  # Skip gameplay logic

        # Settings state placeholder (US-060)
        if game_state == "settings":
            # Settings screen - placeholder for future implementation
            screen.fill(BLACK)
            settings_font = pygame.font.Font(None, 48)
            settings_text = settings_font.render("Settings Screen - Coming Soon", True, (255, 255, 255))
            settings_rect = settings_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(settings_text, settings_rect)
            hint_text = settings_font.render("Press ESC to return to menu", True, (200, 200, 200))
            hint_rect = hint_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            screen.blit(hint_text, hint_rect)
            pygame.display.flip()
            clock.tick(FPS)
            continue  # Skip gameplay logic

        # Game over state - freeze game and show game over menu (US-036)
        if game_state == "game_over":
            # Don't update any game entities - game is frozen!
            # Update game over menu (for delay timer)
            game_over_menu.update()

            # Fill screen with black background
            screen.fill(BLACK)

            # Draw all sprites at their frozen positions with camera offset
            for sprite in all_sprites:
                offset_rect = sprite.rect.copy()
                offset_rect.x -= camera_x
                screen.blit(sprite.image, offset_rect)

            # Draw game over menu overlay on top
            game_over_menu.draw(screen, score)

            # Update display
            pygame.display.flip()
            clock.tick(FPS)
            continue  # Skip gameplay logic

        # Gameplay state - only execute when game_state == "playing"
        # Get currently pressed keys for continuous input
        keys = pygame.key.get_pressed()

        # Handle continuous shooting when powered up (US-019) - X or J key (only during normal gameplay)
        if not is_level_complete and not is_dead and not is_transition_screen and not is_victory_screen:
            if keys[pygame.K_x] or keys[pygame.K_j]:
                # Shoot unlimited lasers while powered up (no MAX_LASERS limit)
                laser_info = player.shoot()
                if laser_info is not None:
                    x, y, direction = laser_info
                    laser = Laser(x, y, direction)
                    lasers.add(laser)
                    all_sprites.add(laser)
                    # TODO (US-043): Play laser shoot sound effect (audio system in Epic 7)

        # Handle level completion state (US-023, US-029)
        if is_level_complete:
            # Increment completion timer
            completion_timer += 1

            # After LEVEL_COMPLETE_DELAY frames (3 seconds), show transition screen (US-029)
            if completion_timer >= LEVEL_COMPLETE_DELAY:
                # Transition to transition screen
                is_transition_screen = True
                is_level_complete = False  # Exit level complete state
                completion_timer = 0  # Reset timer for future use
                # Add level completion time to total game time (US-030)
                total_game_time += completion_time

        # Handle death state
        elif is_dead:
            # Increment death timer
            death_timer += 1

            # Check if it's time to respawn
            if death_timer >= DEATH_DELAY:
                # Respawn: reset level using Level.reset_level()
                level.reset_level()
                # Get fresh references to level entities
                player = level.player
                all_sprites = level.all_sprites
                platforms = level.platforms
                enemies = level.enemies
                powerups = level.powerups
                lasers.empty()  # Clear all lasers on respawn
                score = 0  # Reset score on respawn
                is_dead = False
                death_timer = 0
                camera_x = 0  # Reset camera (US-038)
                # TODO (US-045): Play respawn sound effect (audio system in Epic 7)

        else:
            # Normal gameplay when not dead
            # Update level name display if active (US-037)
            if level_name_display and level_name_display.is_active:
                level_name_display.update()

            # Update player with current key states, platform collision, and level width (US-038, US-039)
            level_width = level.metadata.get("width", WINDOW_WIDTH)
            player.update(keys, platforms, level_width)

            # Update all enemies with platform collision
            for enemy in enemies:
                enemy.update(platforms)

            # Update all power-ups (for floating animation)
            for powerup in powerups:
                powerup.update()

            # Update all lasers (US-019) - handles movement and off-screen removal
            for laser in lasers:
                laser.update(level_width)

            # Check for laser-enemy collisions (US-020)
            for laser in lasers:
                # Check collision with all enemies
                hit_enemies = pygame.sprite.spritecollide(laser, enemies, False)
                for enemy in hit_enemies:
                    if not enemy.is_squashed:  # Don't collide with already squashed enemies
                        # Laser hit an enemy!
                        laser.kill()  # Remove laser from sprite groups
                        enemy.squash()  # Mark enemy as squashed (will disappear after animation)
                        score += STOMP_SCORE  # Award same points as stomp kill
                        # TODO (US-042): Play enemy defeat sound effect (audio system in Epic 7)
                        # TODO (US-058): Add explosion particle effect at impact point (visual polish in Epic 8)
                        break  # One laser can only hit one enemy (exit inner loop)

            # Check for player-enemy collisions
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect) and not enemy.is_squashed:
                    # Check if player is falling and hitting enemy from above (stomp)
                    if player.velocity_y > 0 and player.rect.bottom < enemy.rect.centery:
                        # Player stomped the enemy!
                        if not enemy.is_squashed:  # Only count score once per enemy
                            enemy.squash()  # Mark as squashed (will disappear after animation)
                            player.velocity_y = -8  # Small upward bounce after stomp
                            score += STOMP_SCORE  # Increase score
                            # TODO (US-042): Play stomp sound effect (audio system in Epic 7)
                    else:
                        # Side or bottom collision - player takes damage
                        # Determine knockback direction based on relative positions
                        if player.rect.centerx < enemy.rect.centerx:
                            knockback_direction = -1  # Push player left
                        else:
                            knockback_direction = 1  # Push player right

                        player.take_damage(knockback_direction)
                        # TODO (US-045): Play damage sound effect (audio system in Epic 7)

            # Check for player-powerup collisions (US-017)
            for powerup in powerups:
                if player.rect.colliderect(powerup.rect):
                    # Player collected the power-up!
                    player.collect_powerup()  # Enter powered-up state
                    score += POWERUP_SCORE  # Increase score
                    powerup.kill()  # Remove from sprite groups (disappears)
                    # TODO (US-044): Play powerup collection sound effect (audio system in Epic 7)
                    # TODO (US-059): Add particle effect for powerup collection (visual polish in Epic 8)

            # Check for level completion (US-023, US-029)
            for goal in goals:
                if player.rect.colliderect(goal.rect):
                    # Player reached the goal - complete the level!
                    if not is_level_complete:  # Only trigger once
                        is_level_complete = True
                        completion_timer = 0
                        # Calculate time taken to complete level (in seconds)
                        completion_time = (pygame.time.get_ticks() - level_start_time) / 1000
                        # Calculate score earned in this level (US-029)
                        score_earned_in_level = score - level_start_score
                        # TODO (US-046): Play level complete sound/music (audio system in Epic 7)

            # Check for pit/fall death (US-015)
            if player.rect.top > WINDOW_HEIGHT:
                # Player fell into a pit - lose one life immediately
                player.lives -= 1
                # TODO (US-045): Play fall death sound effect (audio system in Epic 7)

                # If still have lives left, respawn at spawn position
                if player.lives > 0:
                    level.respawn_player()  # Use Level's respawn method
                # If no lives left, trigger death state

            # Check for death condition (US-014, US-036)
            if player.lives <= 0:
                # Player has run out of lives - trigger game over state (US-036)
                game_state = "game_over"
                game_over_menu.reset()  # Reset game over menu selection and delay timer
                # TODO (US-036): Play game over sound/music (audio system in Epic 7)

        # Update camera position (US-038, US-039)
        # Camera follows player horizontally, centered on player
        camera_x = player.rect.centerx - WINDOW_WIDTH // 2

        # Clamp camera to level boundaries (US-039)
        level_width = level.metadata.get("width", WINDOW_WIDTH)
        max_camera_x = max(0, level_width - WINDOW_WIDTH)  # Don't scroll if level smaller than screen
        camera_x = max(0, min(camera_x, max_camera_x))  # Clamp to [0, max_camera_x]

        # Fill screen with black background
        screen.fill(BLACK)

        # Draw all sprites with camera offset (US-038)
        for sprite in all_sprites:
            # Create a temporary rect with camera offset applied
            offset_rect = sprite.rect.copy()
            offset_rect.x -= camera_x
            screen.blit(sprite.image, offset_rect)

        # Draw HUD - Score Display (US-031)
        score_text = font.render(f"SCORE: {score:05d}", True, (255, 255, 255))  # White text, zero-padded to 5 digits
        screen.blit(score_text, (10, 10))  # Top-left corner

        # Draw HUD - Lives Display (US-032)
        lives_text = font.render(f"x{player.lives}", True, (255, 255, 255))  # White text in "x3" format
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 10, 10)  # Top-right corner with 10px margin
        screen.blit(lives_text, lives_rect)

        # Display powerup timer when powered up (US-033)
        if player.is_powered_up:
            # Convert frames to seconds (60 frames = 1 second at 60 FPS)
            powerup_seconds = player.powerup_timer / 60

            # Determine timer color based on remaining time
            # Warning color (red) when less than 3 seconds, gold otherwise
            if powerup_seconds < 3.0:
                timer_color = (255, 50, 50)  # Red warning color
            else:
                timer_color = (255, 215, 0)  # Gold color (normal)

            # Format timer text to show countdown
            timer_text = font.render(f"POWERUP: {powerup_seconds:.1f}s", True, timer_color)

            # Position at top-center of screen for visibility
            timer_rect = timer_text.get_rect()
            timer_rect.centerx = WINDOW_WIDTH // 2  # Centered horizontally
            timer_rect.top = 10  # 10px from top (same as score/lives)

            screen.blit(timer_text, timer_rect)

        # Display level name at level start (US-037)
        # Only show during normal gameplay, not during special screens
        if level_name_display and not is_level_complete and not is_transition_screen and not is_victory_screen:
            level_name_display.draw(screen)

        # Display level completion screen (US-023)
        if is_level_complete:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)  # Semi-transparent (0-255)
            overlay.fill((0, 0, 0))  # Black overlay
            screen.blit(overlay, (0, 0))

            # Create larger font for completion screen
            big_font = pygame.font.Font(None, 72)
            medium_font = pygame.font.Font(None, 48)

            # Display "LEVEL COMPLETE!" message
            complete_text = big_font.render("LEVEL COMPLETE!", True, (0, 255, 0))  # Bright green
            complete_rect = complete_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
            screen.blit(complete_text, complete_rect)

            # Display final score
            score_text = medium_font.render(f"Final Score: {score}", True, (255, 255, 255))  # White
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(score_text, score_rect)

            # Display completion time
            time_text = medium_font.render(f"Time: {completion_time:.1f}s", True, (255, 255, 255))  # White
            time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            screen.blit(time_text, time_rect)

        # Display level transition screen (US-029)
        if is_transition_screen:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)  # Slightly more opaque than completion screen
            overlay.fill((0, 0, 0))  # Black overlay
            screen.blit(overlay, (0, 0))

            # Create fonts for transition screen
            big_font = pygame.font.Font(None, 72)
            medium_font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 36)

            # Get level metadata for display
            level_name = level.metadata.get("name", f"Level {current_level_number}")

            # Display "Level Complete!" title
            title_text = big_font.render("Level Complete!", True, (0, 255, 0))  # Bright green
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6))
            screen.blit(title_text, title_rect)

            # Display level name and number
            level_info_text = medium_font.render(f"{level_name} (Level {current_level_number})", True, (255, 255, 255))  # White
            level_info_rect = level_info_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6 + 80))
            screen.blit(level_info_text, level_info_rect)

            # Display score earned in this level
            score_earned_text = medium_font.render(f"Score Earned: {score_earned_in_level}", True, (255, 215, 0))  # Gold
            score_earned_rect = score_earned_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            screen.blit(score_earned_text, score_earned_rect)

            # Display total score
            total_score_text = small_font.render(f"Total Score: {score}", True, (255, 255, 255))  # White
            total_score_rect = total_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            screen.blit(total_score_text, total_score_rect)

            # Display time taken
            time_text = medium_font.render(f"Time: {completion_time:.1f}s", True, (255, 255, 255))  # White
            time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            screen.blit(time_text, time_rect)

            # Display "Press any key to continue" prompt
            # Add blinking effect by alternating visibility every 30 frames
            if (pygame.time.get_ticks() // 500) % 2 == 0:  # Blink every 0.5 seconds
                continue_text = small_font.render("Press any key to continue", True, (200, 200, 200))  # Light gray
                continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
                screen.blit(continue_text, continue_rect)

            # TODO (US-029): Play transition music/fanfare (audio system in Epic 7)

        # Display victory screen (US-030)
        if is_victory_screen:
            # Create semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(220)  # Mostly opaque for clear victory screen
            overlay.fill((0, 0, 0))  # Black overlay
            screen.blit(overlay, (0, 0))

            # Create fonts for victory screen
            huge_font = pygame.font.Font(None, 96)  # Extra large for main title
            big_font = pygame.font.Font(None, 72)
            medium_font = pygame.font.Font(None, 48)
            small_font = pygame.font.Font(None, 36)

            # Colombian flag colors for celebration theme
            yellow_col = (255, 209, 0)  # Colombian yellow
            blue_col = (0, 56, 168)     # Colombian blue
            red_col = (206, 17, 38)     # Colombian red
            gold_col = (255, 215, 0)    # Gold for highlights

            # Display main congratulations message
            congrats_text = huge_font.render("¡FELICIDADES!", True, yellow_col)  # Spanish for "Congratulations!"
            congrats_rect = congrats_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
            screen.blit(congrats_text, congrats_rect)

            # Display "You completed Sancho Bros!" message
            completed_text = big_font.render("You completed Sancho Bros!", True, (255, 255, 255))  # White
            completed_rect = completed_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
            screen.blit(completed_text, completed_rect)

            # Display total score
            score_text = medium_font.render(f"Total Score: {score}", True, gold_col)  # Gold
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 270))
            screen.blit(score_text, score_rect)

            # Display total time played
            time_text = medium_font.render(f"Total Time: {total_game_time:.1f}s", True, gold_col)  # Gold
            time_rect = time_text.get_rect(center=(WINDOW_WIDTH // 2, 330))
            screen.blit(time_text, time_rect)

            # Colombian-themed celebration message
            celebration_text = small_font.render("¡Eres el mejor cafetero!", True, yellow_col)  # "You're the best coffee grower!"
            celebration_rect = celebration_text.get_rect(center=(WINDOW_WIDTH // 2, 400))
            screen.blit(celebration_text, celebration_rect)

            # Display options
            restart_text = small_font.render("Press R to Restart", True, (200, 200, 200))  # Light gray
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 480))
            screen.blit(restart_text, restart_rect)

            quit_text = small_font.render("Press Q or ESC to Quit", True, (200, 200, 200))  # Light gray
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, 530))
            screen.blit(quit_text, quit_rect)

            # TODO (US-047): Play victory music (audio system in Epic 7)

        # Update display
        pygame.display.flip()

        # Maintain consistent FPS
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
