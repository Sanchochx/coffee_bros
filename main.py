"""
Sancho Bros - Main Game Entry Point
A 2D platformer game inspired by Super Mario Bros with Colombian cultural themes.
"""

import pygame
import sys
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE, BLACK, STOMP_SCORE
from src.entities import Player, Platform, Polocho


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

    # Create player at initial spawn position
    player = Player(100, 400)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create platforms
    platforms = pygame.sprite.Group()

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

    # Create enemies
    enemies = pygame.sprite.Group()

    # Spawn multiple Polocho enemies at different positions
    enemy1 = Polocho(300, 400)
    enemies.add(enemy1)
    all_sprites.add(enemy1)

    enemy2 = Polocho(500, 300)
    enemies.add(enemy2)
    all_sprites.add(enemy2)

    enemy3 = Polocho(650, 200)
    enemies.add(enemy3)
    all_sprites.add(enemy3)

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
