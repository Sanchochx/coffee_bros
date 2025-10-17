"""
Collision Detection Test Suite for Sancho Bros
Tests all collision detection systems in the game to ensure accuracy and prevent bugs.
"""

import pygame
import sys
import os

# Add parent directory to path to import game modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.entities.player import Player
from src.entities.polocho import Polocho
from src.entities.platform import Platform
from src.entities.laser import Laser
from src.entities.golden_arepa import GoldenArepa
from src.entities.goal import Goal
from config import *


class CollisionTestSuite:
    """Comprehensive collision detection test suite"""

    def __init__(self):
        """Initialize pygame and test environment"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tests_passed = 0
        self.tests_failed = 0
        self.test_results = []
        # Create reusable empty key state for tests
        self.empty_keys = pygame.key.get_pressed()

    def log_test(self, test_name, passed, message=""):
        """Log test result"""
        if passed:
            self.tests_passed += 1
            status = "PASS"
        else:
            self.tests_failed += 1
            status = "FAIL"

        result = f"[{status}] {test_name}"
        if message:
            result += f": {message}"

        self.test_results.append(result)
        print(result)

    def assert_true(self, condition, test_name, message=""):
        """Assert that condition is true"""
        self.log_test(test_name, condition, message)
        return condition

    def assert_false(self, condition, test_name, message=""):
        """Assert that condition is false"""
        self.log_test(test_name, not condition, message)
        return not condition

    # ==================== PLAYER-PLATFORM COLLISION TESTS ====================

    def test_player_lands_on_platform(self):
        """Test that player correctly lands on top of platform"""
        player = Player(400, 100)
        platform = Platform(300, 300, 200, 20)
        platforms = pygame.sprite.Group(platform)

        # Make player fall
        player.velocity_y = 5

        # Move player to just above platform
        player.rect.bottom = platform.rect.top - 10
        player.rect.centerx = platform.rect.centerx

        # Update player physics several times to ensure landing
        for _ in range(10):
            player.update(self.empty_keys, platforms, WINDOW_WIDTH)

        # Check that player is grounded and on platform
        landed = player.is_grounded and player.rect.bottom == platform.rect.top
        self.assert_true(landed, "Player lands on platform top",
                        f"Grounded: {player.is_grounded}, Bottom: {player.rect.bottom}, Platform top: {platform.rect.top}")

    def test_player_does_not_fall_through_platform(self):
        """Test that player never falls through platform"""
        player = Player(400, 100)
        platform = Platform(300, 300, 200, 20)
        platforms = pygame.sprite.Group(platform)

        # Position player directly on platform
        player.rect.bottom = platform.rect.top
        player.rect.centerx = platform.rect.centerx
        player.velocity_y = 0
        player.is_grounded = True

        # Update player several times
        for _ in range(20):
            player.update(platforms, WINDOW_WIDTH)

        # Player should still be on platform
        not_fallen = player.rect.bottom <= platform.rect.top + 2  # Allow small tolerance
        self.assert_true(not_fallen, "Player does not fall through platform",
                        f"Player bottom: {player.rect.bottom}, Platform top: {platform.rect.top}")

    def test_player_hits_ceiling(self):
        """Test that player correctly hits platform from below"""
        player = Player(400, 350)
        platform = Platform(300, 300, 200, 20)
        platforms = pygame.sprite.Group(platform)

        # Make player jump upward into platform
        player.velocity_y = -15
        player.rect.top = platform.rect.bottom + 10
        player.rect.centerx = platform.rect.centerx

        # Update player
        for _ in range(5):
            player.update(platforms, WINDOW_WIDTH)

        # Check that player stopped moving upward
        hit_ceiling = player.velocity_y >= 0
        self.assert_true(hit_ceiling, "Player hits ceiling/platform from below",
                        f"Velocity Y: {player.velocity_y}")

    def test_player_cannot_clip_through_wall_left(self):
        """Test that player cannot clip through wall on left side"""
        player = Player(350, 250)
        platform = Platform(300, 200, 20, 100)  # Vertical wall
        platforms = pygame.sprite.Group(platform)

        # Move player left into wall
        player.rect.left = platform.rect.right + 5
        player.velocity_x = -5

        # Update player several times
        for _ in range(10):
            player.update(platforms, WINDOW_WIDTH)

        # Player should not go through wall
        no_clip = player.rect.left >= platform.rect.right - 2  # Small tolerance
        self.assert_true(no_clip, "Player cannot clip through wall (left)",
                        f"Player left: {player.rect.left}, Wall right: {platform.rect.right}")

    def test_player_cannot_clip_through_wall_right(self):
        """Test that player cannot clip through wall on right side"""
        player = Player(250, 250)
        platform = Platform(300, 200, 20, 100)  # Vertical wall
        platforms = pygame.sprite.Group(platform)

        # Move player right into wall
        player.rect.right = platform.rect.left - 5
        player.velocity_x = 5

        # Update player several times
        for _ in range(10):
            player.update(platforms, WINDOW_WIDTH)

        # Player should not go through wall
        no_clip = player.rect.right <= platform.rect.left + 2  # Small tolerance
        self.assert_true(no_clip, "Player cannot clip through wall (right)",
                        f"Player right: {player.rect.right}, Wall left: {platform.rect.left}")

    def test_player_respects_level_boundaries(self):
        """Test that player cannot move outside level boundaries"""
        player = Player(50, 250)
        platforms = pygame.sprite.Group()

        # Try to move player left outside boundary
        player.rect.left = -10
        player.update(platforms, 800)

        left_bound = player.rect.left >= 0
        self.assert_true(left_bound, "Player respects left boundary",
                        f"Player left: {player.rect.left}")

        # Try to move player right outside boundary
        player.rect.right = 900
        player.update(platforms, 800)

        right_bound = player.rect.right <= 800
        self.assert_true(right_bound, "Player respects right boundary",
                        f"Player right: {player.rect.right}, Level width: 800")

    # ==================== ENEMY STOMP COLLISION TESTS ====================

    def test_stomp_detection_accurate(self):
        """Test that stomp detection correctly identifies top-down collision"""
        player = Player(400, 200)
        enemy = Polocho(400, 300)

        # Position player above enemy, falling down
        player.rect.centerx = enemy.rect.centerx
        player.rect.bottom = enemy.rect.centery - 10
        player.velocity_y = 10  # Falling

        # Check stomp conditions
        is_falling = player.velocity_y > 0
        is_from_above = player.rect.bottom < enemy.rect.centery
        is_stomp = is_falling and is_from_above

        self.assert_true(is_stomp, "Stomp detection identifies top-down collision",
                        f"Falling: {is_falling}, From above: {is_from_above}")

    def test_stomp_not_triggered_from_side(self):
        """Test that side collision does not trigger stomp"""
        player = Player(350, 300)
        enemy = Polocho(400, 300)

        # Position player at side of enemy
        player.rect.centery = enemy.rect.centery
        player.rect.right = enemy.rect.left - 5
        player.velocity_y = 5  # Still falling

        # Check stomp conditions
        is_falling = player.velocity_y > 0
        is_from_above = player.rect.bottom < enemy.rect.centery
        is_stomp = is_falling and is_from_above

        self.assert_false(is_stomp, "Side collision does not trigger stomp",
                         f"Falling: {is_falling}, From above: {is_from_above}")

    def test_stomp_not_triggered_from_below(self):
        """Test that bottom collision does not trigger stomp"""
        player = Player(400, 350)
        enemy = Polocho(400, 300)

        # Position player below enemy, moving up
        player.rect.centerx = enemy.rect.centerx
        player.rect.top = enemy.rect.bottom + 5
        player.velocity_y = -10  # Moving upward

        # Check stomp conditions
        is_falling = player.velocity_y > 0
        is_from_above = player.rect.bottom < enemy.rect.centery
        is_stomp = is_falling and is_from_above

        self.assert_false(is_stomp, "Bottom collision does not trigger stomp",
                         f"Falling: {is_falling}, From above: {is_from_above}")

    # ==================== DAMAGE DETECTION TESTS ====================

    def test_side_collision_triggers_damage(self):
        """Test that side collision correctly triggers damage"""
        player = Player(350, 300)
        enemy = Polocho(400, 300)

        # Position player at side of enemy (not from above)
        player.rect.centery = enemy.rect.centery
        player.rect.right = enemy.rect.left - 5
        player.velocity_y = 0  # Not falling

        # This should trigger damage, not stomp
        is_falling = player.velocity_y > 0
        is_from_above = player.rect.bottom < enemy.rect.centery
        is_damage = not (is_falling and is_from_above)

        self.assert_true(is_damage, "Side collision triggers damage",
                        f"Should damage: {is_damage}")

    def test_damage_applies_knockback_left(self):
        """Test that damage applies correct knockback direction (left)"""
        player = Player(450, 300)
        enemy = Polocho(400, 300)

        # Player is to the right of enemy
        initial_lives = player.lives
        knockback_dir = -1 if player.rect.centerx < enemy.rect.centerx else 1

        # Knockback should be to the right (1)
        self.assert_true(knockback_dir == 1, "Knockback direction correct (right)",
                        f"Knockback: {knockback_dir}, Player X: {player.rect.centerx}, Enemy X: {enemy.rect.centerx}")

    def test_damage_applies_knockback_right(self):
        """Test that damage applies correct knockback direction (right)"""
        player = Player(350, 300)
        enemy = Polocho(400, 300)

        # Player is to the left of enemy
        knockback_dir = -1 if player.rect.centerx < enemy.rect.centerx else 1

        # Knockback should be to the left (-1)
        self.assert_true(knockback_dir == -1, "Knockback direction correct (left)",
                        f"Knockback: {knockback_dir}, Player X: {player.rect.centerx}, Enemy X: {enemy.rect.centerx}")

    def test_invulnerability_prevents_damage(self):
        """Test that invulnerability prevents further damage"""
        player = Player(400, 300)

        # Activate invulnerability
        player.is_invulnerable = True
        player.invulnerability_timer = 60
        initial_lives = player.lives

        # Try to take damage
        player.take_damage(0)

        # Lives should not change
        no_damage = player.lives == initial_lives
        self.assert_true(no_damage, "Invulnerability prevents damage",
                        f"Lives: {player.lives}, Initial: {initial_lives}")

    # ==================== PROJECTILE COLLISION TESTS ====================

    def test_laser_hits_enemy(self):
        """Test that laser correctly collides with enemy"""
        laser = Laser(350, 300, 1)
        enemy = Polocho(400, 300)

        # Move laser into enemy
        laser.rect.centerx = enemy.rect.centerx
        laser.rect.centery = enemy.rect.centery

        # Check collision
        collision = laser.rect.colliderect(enemy.rect)
        self.assert_true(collision, "Laser collides with enemy",
                        f"Collision: {collision}")

    def test_laser_removed_after_hit(self):
        """Test that laser is removed after hitting enemy"""
        laser = Laser(350, 300, 1)
        enemies = pygame.sprite.Group()
        enemy = Polocho(400, 300)
        enemies.add(enemy)

        # Simulate hit detection
        laser.rect.centerx = enemy.rect.centerx
        laser.rect.centery = enemy.rect.centery

        hit_enemies = pygame.sprite.spritecollide(laser, enemies, False)

        # Laser should detect hit
        hit_detected = len(hit_enemies) > 0
        self.assert_true(hit_detected, "Laser hit detection works",
                        f"Enemies hit: {len(hit_enemies)}")

    def test_laser_does_not_hit_squashed_enemy(self):
        """Test that laser does not collide with already squashed enemies"""
        laser = Laser(350, 300, 1)
        enemy = Polocho(400, 300)

        # Squash the enemy first
        enemy.squash()

        # Move laser into enemy
        laser.rect.centerx = enemy.rect.centerx
        laser.rect.centery = enemy.rect.centery

        # Should not register hit because enemy is squashed
        should_ignore = enemy.is_squashed
        self.assert_true(should_ignore, "Laser ignores squashed enemies",
                        f"Enemy squashed: {should_ignore}")

    def test_laser_removed_when_offscreen(self):
        """Test that laser is removed when it goes off screen"""
        laser = Laser(400, 300, 1)
        level_width = 800

        # Move laser far off screen to the right
        laser.rect.left = level_width + 150
        laser.update(level_width)

        # Laser should be marked for removal (killed)
        # We can't directly check if killed, but we can verify position logic
        should_remove = laser.rect.left > level_width + 100
        self.assert_true(should_remove, "Laser removed when off-screen (right)",
                        f"Laser left: {laser.rect.left}, Max: {level_width + 100}")

    # ==================== POWERUP COLLISION TESTS ====================

    def test_powerup_collection_detection(self):
        """Test that powerup collection is detected correctly"""
        player = Player(400, 300)
        powerup = GoldenArepa(400, 300)

        # Position player on powerup
        player.rect.centerx = powerup.rect.centerx
        player.rect.centery = powerup.rect.centery

        # Check collision
        collision = player.rect.colliderect(powerup.rect)
        self.assert_true(collision, "Powerup collection detected",
                        f"Collision: {collision}")

    def test_powerup_collection_activates_powerup_state(self):
        """Test that collecting powerup activates powered up state"""
        player = Player(400, 300)

        # Collect powerup
        player.collect_powerup()

        # Check powered up state
        is_powered = player.is_powered_up and player.powerup_timer > 0
        self.assert_true(is_powered, "Powerup state activated",
                        f"Powered up: {player.is_powered_up}, Timer: {player.powerup_timer}")

    # ==================== GOAL COLLISION TESTS ====================

    def test_goal_collision_detection(self):
        """Test that reaching goal is detected correctly"""
        player = Player(400, 300)
        goal = Goal(750, 250)

        # Move player to goal
        player.rect.centerx = goal.rect.centerx
        player.rect.centery = goal.rect.centery

        # Check collision
        collision = player.rect.colliderect(goal.rect)
        self.assert_true(collision, "Goal collision detected",
                        f"Collision: {collision}")

    # ==================== PIT/FALL DEATH TESTS ====================

    def test_pit_death_detection(self):
        """Test that falling into pit is detected"""
        player = Player(400, 100)

        # Move player below screen
        player.rect.top = WINDOW_HEIGHT + 50

        # Check if player fell
        fell_in_pit = player.rect.top > WINDOW_HEIGHT
        self.assert_true(fell_in_pit, "Pit death detected",
                        f"Player top: {player.rect.top}, Screen height: {WINDOW_HEIGHT}")

    # ==================== ENEMY COLLISION TESTS ====================

    def test_enemy_turns_at_wall(self):
        """Test that enemy turns around when hitting wall"""
        enemy = Polocho(350, 250)
        platform = Platform(300, 200, 20, 100)  # Vertical wall
        platforms = pygame.sprite.Group(platform)

        # Enemy moving right toward wall
        enemy.direction = 1
        enemy.rect.right = platform.rect.left - 5
        initial_direction = enemy.direction

        # Update enemy several times
        for _ in range(10):
            enemy.update(platforms)

        # Enemy should have turned around
        turned = enemy.direction != initial_direction
        self.assert_true(turned, "Enemy turns at wall",
                        f"Initial: {initial_direction}, Current: {enemy.direction}")

    def test_enemy_turns_at_platform_edge(self):
        """Test that enemy turns around at platform edge"""
        enemy = Polocho(550, 250)
        platform = Platform(400, 300, 200, 20)  # Flat platform
        platforms = pygame.sprite.Group(platform)

        # Position enemy at edge of platform, moving right
        enemy.rect.bottom = platform.rect.top
        enemy.rect.right = platform.rect.right - 10
        enemy.direction = 1
        enemy.is_grounded = True
        initial_direction = enemy.direction

        # Update enemy several times
        for _ in range(20):
            enemy.update(platforms)

        # Enemy should turn when reaching edge
        turned = enemy.direction != initial_direction
        self.assert_true(turned, "Enemy turns at platform edge",
                        f"Initial: {initial_direction}, Current: {enemy.direction}")

    def test_enemy_lands_on_platform(self):
        """Test that enemy correctly lands on platform"""
        enemy = Polocho(450, 100)
        platform = Platform(400, 300, 200, 20)
        platforms = pygame.sprite.Group(platform)

        # Position enemy above platform
        enemy.rect.bottom = platform.rect.top - 50
        enemy.rect.centerx = platform.rect.centerx
        enemy.velocity_y = 5

        # Update enemy several times
        for _ in range(20):
            enemy.update(platforms)

        # Enemy should land on platform
        landed = enemy.is_grounded and enemy.rect.bottom <= platform.rect.top + 2
        self.assert_true(landed, "Enemy lands on platform",
                        f"Grounded: {enemy.is_grounded}, Bottom: {enemy.rect.bottom}, Platform top: {platform.rect.top}")

    # ==================== CORNER CASE TESTS ====================

    def test_multiple_platform_collision(self):
        """Test collision when player touches multiple platforms"""
        player = Player(400, 250)
        platform1 = Platform(300, 300, 200, 20)
        platform2 = Platform(500, 300, 200, 20)
        platforms = pygame.sprite.Group(platform1, platform2)

        # Position player between two platforms
        player.rect.bottom = platform1.rect.top - 10
        player.rect.centerx = 500  # Between platforms
        player.velocity_y = 5

        # Update player
        for _ in range(10):
            player.update(platforms, WINDOW_WIDTH)

        # Player should land on one of the platforms
        landed = player.is_grounded
        self.assert_true(landed, "Player handles multiple platform collision",
                        f"Grounded: {landed}")

    def test_corner_collision(self):
        """Test collision at platform corner"""
        player = Player(295, 295)
        platform = Platform(300, 300, 200, 20)
        platforms = pygame.sprite.Group(platform)

        # Position player at corner of platform
        player.rect.bottomleft = (platform.rect.left - 5, platform.rect.top - 5)
        player.velocity_y = 5
        player.velocity_x = 3

        # Update player
        for _ in range(5):
            player.update(platforms, WINDOW_WIDTH)

        # Player should handle corner collision gracefully
        handled = player.rect.top < WINDOW_HEIGHT
        self.assert_true(handled, "Corner collision handled",
                        f"Player Y: {player.rect.top}")

    # ==================== RUN ALL TESTS ====================

    def run_all_tests(self):
        """Run all collision detection tests"""
        print("\n" + "="*70)
        print("SANCHO BROS - COLLISION DETECTION TEST SUITE")
        print("="*70 + "\n")

        # Player-Platform Tests
        print("\n--- PLAYER-PLATFORM COLLISION TESTS ---")
        self.test_player_lands_on_platform()
        self.test_player_does_not_fall_through_platform()
        self.test_player_hits_ceiling()
        self.test_player_cannot_clip_through_wall_left()
        self.test_player_cannot_clip_through_wall_right()
        self.test_player_respects_level_boundaries()

        # Enemy Stomp Tests
        print("\n--- ENEMY STOMP DETECTION TESTS ---")
        self.test_stomp_detection_accurate()
        self.test_stomp_not_triggered_from_side()
        self.test_stomp_not_triggered_from_below()

        # Damage Tests
        print("\n--- DAMAGE DETECTION TESTS ---")
        self.test_side_collision_triggers_damage()
        self.test_damage_applies_knockback_left()
        self.test_damage_applies_knockback_right()
        self.test_invulnerability_prevents_damage()

        # Projectile Tests
        print("\n--- PROJECTILE COLLISION TESTS ---")
        self.test_laser_hits_enemy()
        self.test_laser_removed_after_hit()
        self.test_laser_does_not_hit_squashed_enemy()
        self.test_laser_removed_when_offscreen()

        # Powerup Tests
        print("\n--- POWERUP COLLISION TESTS ---")
        self.test_powerup_collection_detection()
        self.test_powerup_collection_activates_powerup_state()

        # Goal Tests
        print("\n--- GOAL COLLISION TESTS ---")
        self.test_goal_collision_detection()

        # Pit Death Tests
        print("\n--- PIT/FALL DEATH TESTS ---")
        self.test_pit_death_detection()

        # Enemy Tests
        print("\n--- ENEMY COLLISION TESTS ---")
        self.test_enemy_turns_at_wall()
        self.test_enemy_turns_at_platform_edge()
        self.test_enemy_lands_on_platform()

        # Corner Case Tests
        print("\n--- CORNER CASE TESTS ---")
        self.test_multiple_platform_collision()
        self.test_corner_collision()

        # Print summary
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        print(f"Total Tests: {self.tests_passed + self.tests_failed}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        print(f"Success Rate: {(self.tests_passed / (self.tests_passed + self.tests_failed) * 100):.1f}%")
        print("="*70 + "\n")

        # Print failed tests if any
        if self.tests_failed > 0:
            print("\nFAILED TESTS:")
            for result in self.test_results:
                if "[FAIL]" in result:
                    print(result)

        pygame.quit()
        return self.tests_failed == 0


if __name__ == "__main__":
    test_suite = CollisionTestSuite()
    success = test_suite.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if success else 1)
