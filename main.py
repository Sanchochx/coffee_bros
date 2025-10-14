"""
Sancho Bros - Main Game Entry Point
A 2D platformer game inspired by Super Mario Bros with Colombian cultural themes.
"""

import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE, BLACK, STOMP_SCORE, DEATH_DELAY, PLAYER_STARTING_LIVES, POWERUP_SCORE, MAX_LASERS
from src.entities import Player, Platform, Polocho, GoldenArepa, Laser
from src.level import Level


def main():
    """Main game function"""
    # Initialize pygame
    pygame.init()

    # Create game window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)

    # Create clock for FPS control
    clock = pygame.time.Clock()

    # Initialize game state
    score = 0
    font = pygame.font.Font(None, 36)  # Default font, size 36

    # Death and respawn state
    is_dead = False
    death_timer = 0

    # Load level from JSON file (US-022)
    try:
        level = Level.load_from_file(1)  # Load level 1
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading level: {e}")
        pygame.quit()
        sys.exit()

    # Get references to level entities for easy access
    player = level.player
    all_sprites = level.all_sprites
    platforms = level.platforms
    enemies = level.enemies
    powerups = level.powerups

    # Create laser sprite group (US-019)
    lasers = pygame.sprite.Group()

    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Handle shooting (US-019) - X or J key
                elif event.key == pygame.K_x or event.key == pygame.K_j:
                    # Only shoot if powered up and not at max lasers
                    if len(lasers) < MAX_LASERS:
                        laser_info = player.shoot()
                        if laser_info is not None:
                            x, y, direction = laser_info
                            laser = Laser(x, y, direction)
                            lasers.add(laser)
                            all_sprites.add(laser)
                            # TODO (US-043): Play laser shoot sound effect (audio system in Epic 7)

        # Get currently pressed keys for continuous input
        keys = pygame.key.get_pressed()

        # Handle death state
        if is_dead:
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
                # TODO (US-045): Play respawn sound effect (audio system in Epic 7)

        else:
            # Normal gameplay when not dead
            # Update player with current key states and platform collision
            player.update(keys, platforms)

            # Update all enemies with platform collision
            for enemy in enemies:
                enemy.update(platforms)

            # Update all power-ups (for floating animation)
            for powerup in powerups:
                powerup.update()

            # Update all lasers (US-019) - handles movement and off-screen removal
            for laser in lasers:
                laser.update()

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

            # Check for pit/fall death (US-015)
            if player.rect.top > WINDOW_HEIGHT:
                # Player fell into a pit - lose one life immediately
                player.lives -= 1
                # TODO (US-045): Play fall death sound effect (audio system in Epic 7)

                # If still have lives left, respawn at spawn position
                if player.lives > 0:
                    level.respawn_player()  # Use Level's respawn method
                # If no lives left, trigger death state

            # Check for death condition (US-014)
            if player.lives <= 0:
                is_dead = True
                death_timer = 0
                # TODO (US-045): Play death sound effect (audio system in Epic 7)

        # Fill screen with black background
        screen.fill(BLACK)

        # Draw all sprites
        all_sprites.draw(screen)

        # Draw HUD (simple text display for now, will be improved in Epic 5)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
        screen.blit(score_text, (10, 10))  # Top-left corner

        lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))  # White text
        screen.blit(lives_text, (10, 50))  # Below score

        # Display powerup timer when powered up (US-018)
        if player.is_powered_up:
            # Convert frames to seconds (60 frames = 1 second)
            powerup_seconds = player.powerup_timer / 60
            powerup_text = font.render(f"Powerup: {powerup_seconds:.1f}s", True, (255, 215, 0))  # Gold text
            screen.blit(powerup_text, (10, 90))  # Below lives

        # Update display
        pygame.display.flip()

        # Maintain consistent FPS
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
