"""
Sancho Bros - Main Game Entry Point
A 2D platformer game inspired by Super Mario Bros with Colombian cultural themes.
"""

import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE, BLACK, STOMP_SCORE, DEATH_DELAY, PLAYER_STARTING_LIVES
from src.entities import Player, Platform, Polocho


def setup_level():
    """
    Set up level entities and return them

    Returns:
        tuple: (player, all_sprites, platforms, enemies, initial_enemy_positions)
    """
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Create player at initial spawn position
    player = Player(100, 400)
    all_sprites.add(player)

    # Create platforms
    # Ground platform (full width at bottom of screen)
    ground = Platform(0, 550, WINDOW_WIDTH, 50)
    platforms.add(ground)
    all_sprites.add(ground)

    # Floating platforms at various positions
    platform1 = Platform(200, 450, 150, 20)
    platforms.add(platform1)
    all_sprites.add(platform1)

    platform2 = Platform(400, 350, 120, 20)
    platforms.add(platform2)
    all_sprites.add(platform2)

    platform3 = Platform(550, 250, 180, 20)
    platforms.add(platform3)
    all_sprites.add(platform3)

    platform4 = Platform(100, 200, 100, 20)
    platforms.add(platform4)
    all_sprites.add(platform4)

    # Store initial enemy spawn positions
    initial_enemy_positions = [
        (300, 400),
        (500, 300),
        (650, 200)
    ]

    # Create enemies at spawn positions
    for x, y in initial_enemy_positions:
        enemy = Polocho(x, y)
        enemies.add(enemy)
        all_sprites.add(enemy)

    return player, all_sprites, platforms, enemies, initial_enemy_positions


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

    # Set up level
    player, all_sprites, platforms, enemies, initial_enemy_positions = setup_level()

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

        # Get currently pressed keys for continuous input
        keys = pygame.key.get_pressed()

        # Handle death state
        if is_dead:
            # Increment death timer
            death_timer += 1

            # Check if it's time to respawn
            if death_timer >= DEATH_DELAY:
                # Respawn: reset level
                player, all_sprites, platforms, enemies, initial_enemy_positions = setup_level()
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

            # Check for pit/fall death (US-015)
            if player.rect.top > WINDOW_HEIGHT:
                # Player fell into a pit - lose one life immediately
                player.lives -= 1
                # TODO (US-045): Play fall death sound effect (audio system in Epic 7)

                # If still have lives left, respawn at spawn position
                if player.lives > 0:
                    player.rect.x = 100
                    player.rect.y = 400
                    player.velocity_y = 0
                    player.is_grounded = False
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

        # Update display
        pygame.display.flip()

        # Maintain consistent FPS
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
