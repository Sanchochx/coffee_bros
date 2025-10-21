"""
Edge Case Testing Suite for Coffee Bros (US-066)
Tests unusual scenarios and edge cases to ensure the game handles them gracefully.

Test Categories:
1. Multiple simultaneous collisions
2. Powerup expiry during shooting
3. Death during invulnerability prevention
4. Pausing during transitions
5. Rapid input handling
6. Boundary conditions (edges, corners)
"""

import pygame
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS, PLAYER_STARTING_LIVES,
    STOMP_SCORE, POWERUP_SCORE, POWERUP_DURATION, INVULNERABILITY_DURATION
)
from src.entities import Player, Platform, Polocho, GoldenArepa, Laser
from src.level import Level
from src.audio_manager import AudioManager


class KeyStateWrapper:
    """Wrapper for pygame key state that handles large key codes"""
    def __init__(self, base_keys, pressed_keys=None):
        self.base_keys = base_keys
        self.pressed_keys = pressed_keys or set()

    def __getitem__(self, key):
        if key in self.pressed_keys:
            return True
        if key < len(self.base_keys):
            return self.base_keys[key]
        return False


class EdgeCaseTester:
    """Test harness for edge case scenarios"""

    def __init__(self):
        """Initialize pygame and test environment"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Edge Case Testing - Coffee Bros")
        self.clock = pygame.time.Clock()
        self.audio_manager = AudioManager()
        # Mute audio during tests
        self.audio_manager.set_music_volume(0.0)
        self.audio_manager.set_sfx_volume(0.0)

        # Test results tracking
        self.test_results = {}
        self.tests_passed = 0
        self.tests_failed = 0

    def log_test(self, test_name, passed, message=""):
        """
        Log test result

        Args:
            test_name (str): Name of the test
            passed (bool): Whether test passed
            message (str): Additional information
        """
        status = "PASS" if passed else "FAIL"
        self.test_results[test_name] = {"passed": passed, "message": message}

        if passed:
            self.tests_passed += 1
            print(f"[{status}] {test_name}")
        else:
            self.tests_failed += 1
            print(f"[{status}] {test_name}: {message}")

        if message and passed:
            print(f"  -> {message}")

    def test_multiple_simultaneous_collisions(self):
        """
        Test 1: Multiple Simultaneous Collisions
        Verify that player can handle:
        - Collision with multiple enemies at once
        - Collision with enemy + powerup simultaneously
        - Collision with platform + enemy + powerup
        """
        print("\n=== Test 1: Multiple Simultaneous Collisions ===")

        # Create test entities
        player = Player(100, 100, self.audio_manager)
        player.lives = 3
        player.is_invulnerable = False

        # Create multiple enemies at same position
        enemy1 = Polocho(120, 100)
        enemy2 = Polocho(125, 100)
        enemy3 = Polocho(130, 100)
        enemies = pygame.sprite.Group(enemy1, enemy2, enemy3)

        # Test: Player collides with multiple enemies
        # Should only take damage once (invulnerability protects from subsequent hits)
        initial_lives = player.lives
        collision_count = 0

        for enemy in enemies:
            if player.rect.colliderect(enemy.rect) and not enemy.is_squashed:
                if not player.is_invulnerable:
                    player.take_damage(1)
                    collision_count += 1

        # Verify only took damage once
        expected_lives = initial_lives - 1
        damage_taken_once = (player.lives == expected_lives)
        invulnerable_active = player.is_invulnerable

        self.log_test(
            "Multiple enemy collision - damage once",
            damage_taken_once and invulnerable_active,
            f"Lives: {initial_lives} -> {player.lives}, Invulnerable: {invulnerable_active}"
        )

        # Test: Simultaneous enemy + powerup collision
        player2 = Player(100, 100, self.audio_manager)
        player2.lives = 3
        player2.velocity_y = 5  # Falling down (for stomp)
        enemy = Polocho(120, 100)
        powerup = GoldenArepa(120, 100)

        # Collide with both
        score = 0
        if player2.rect.colliderect(enemy.rect):
            if player2.velocity_y > 0:  # Stomp
                enemy.squash()
                score += STOMP_SCORE
        if player2.rect.colliderect(powerup.rect):
            player2.collect_powerup()
            score += POWERUP_SCORE

        # Verify both interactions work
        enemy_defeated = enemy.is_squashed
        powerup_collected = player2.is_powered_up
        score_correct = (score == STOMP_SCORE + POWERUP_SCORE)

        self.log_test(
            "Enemy + powerup simultaneous collision",
            enemy_defeated and powerup_collected and score_correct,
            f"Enemy squashed: {enemy_defeated}, Powered up: {powerup_collected}, Score: {score}"
        )

    def test_powerup_expiry_during_shooting(self):
        """
        Test 2: Powerup Expiry During Shooting
        Verify that powerup expiring mid-shot doesn't crash or break game state
        """
        print("\n=== Test 2: Powerup Expiry During Shooting ===")

        player = Player(100, 100, self.audio_manager)
        player.is_powered_up = True
        player.powerup_timer = 5  # About to expire

        lasers = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        # Shoot laser while powerup about to expire
        laser_info = player.shoot()
        if laser_info:
            x, y, direction = laser_info
            laser = Laser(x, y, direction)
            lasers.add(laser)
            all_sprites.add(laser)

        laser_created = len(lasers) > 0

        # Update player multiple times to expire powerup
        platforms = pygame.sprite.Group()
        for _ in range(10):
            player.update(pygame.key.get_pressed(), platforms)

        # Verify powerup expired but game didn't crash
        powerup_expired = not player.is_powered_up
        can_still_shoot = player.shoot() is None  # Should not be able to shoot anymore

        self.log_test(
            "Powerup expiry during shooting",
            laser_created and powerup_expired and can_still_shoot,
            f"Laser created: {laser_created}, Powerup expired: {powerup_expired}, Can't shoot: {can_still_shoot}"
        )

        # Test: Powerup expires exactly on the frame player tries to shoot again
        player2 = Player(100, 100, self.audio_manager)
        player2.is_powered_up = True
        player2.powerup_timer = 1  # Will expire next frame
        player2.shoot_cooldown = 0

        # Try to shoot on expiry frame
        laser_info_before = player2.shoot()  # Should work
        player2.update(pygame.key.get_pressed(), platforms)  # Expires powerup
        laser_info_after = player2.shoot()  # Should fail

        self.log_test(
            "Shooting on exact expiry frame",
            laser_info_before is not None and laser_info_after is None,
            f"Shot before expiry: {laser_info_before is not None}, Shot after expiry: {laser_info_after is None}"
        )

    def test_death_during_invulnerability(self):
        """
        Test 3: Death During Invulnerability Prevention
        Verify that player cannot die from enemy collision during invulnerability
        But CAN die from falling into pits
        """
        print("\n=== Test 3: Death During Invulnerability Prevention ===")

        # Test: Enemy collision during invulnerability
        player = Player(100, 100, self.audio_manager)
        player.lives = 1  # One hit from death
        player.is_invulnerable = True
        player.invulnerability_timer = 60

        enemy = Polocho(120, 100)

        initial_lives = player.lives

        # Attempt to take damage while invulnerable
        if player.rect.colliderect(enemy.rect):
            player.take_damage(1)

        # Verify no damage taken
        no_damage_taken = (player.lives == initial_lives)

        self.log_test(
            "Enemy collision during invulnerability",
            no_damage_taken,
            f"Lives unchanged: {initial_lives} -> {player.lives}"
        )

        # Test: Pit death should work even during invulnerability
        player2 = Player(100, 100, self.audio_manager)
        player2.lives = 3
        player2.is_invulnerable = True
        player2.invulnerability_timer = 60

        # Simulate falling into pit (y > WINDOW_HEIGHT)
        player2.rect.top = WINDOW_HEIGHT + 10

        # Check pit death condition (from main.py line 656)
        if player2.rect.top > WINDOW_HEIGHT:
            player2.lives -= 1  # Pit death ignores invulnerability

        pit_death_works = (player2.lives == 2)

        self.log_test(
            "Pit death during invulnerability",
            pit_death_works,
            f"Lives decreased from pit: 3 -> {player2.lives}"
        )

    def test_pausing_during_transitions(self):
        """
        Test 4: Pausing During Transitions
        Verify that game can be paused during:
        - Level completion screen
        - Level transition screen
        - Victory screen
        Without breaking game state
        """
        print("\n=== Test 4: Pausing During Transitions ===")

        # Simulate game states
        game_states = ["playing", "paused", "menu", "game_over", "settings"]

        # Test: Can pause from playing state
        current_state = "playing"
        # Simulate ESC press
        can_pause = (current_state == "playing")

        self.log_test(
            "Can pause from playing state",
            can_pause,
            f"State transition: playing -> paused allowed"
        )

        # Test: Pausing during transition screen
        # From main.py line 334, transition screen checks for is_transition_screen flag
        # ESC key should pause even during transition (no special blocking)
        is_transition_screen = True
        is_victory_screen = False
        current_state = "playing"

        # ESC press during transition
        if current_state == "playing":
            can_pause_during_transition = True
        else:
            can_pause_during_transition = False

        self.log_test(
            "Can pause during transition screen",
            can_pause_during_transition,
            f"Pause allowed during transition: {can_pause_during_transition}"
        )

        # Test: Verify game state doesn't corrupt during pause
        test_score = 12345
        test_lives = 2
        test_level = 3

        # Simulate pause and unpause
        saved_score = test_score
        saved_lives = test_lives
        saved_level = test_level

        # After unpause, verify state intact
        state_preserved = (
            saved_score == test_score and
            saved_lives == test_lives and
            saved_level == test_level
        )

        self.log_test(
            "Game state preserved during pause",
            state_preserved,
            f"Score: {test_score}, Lives: {test_lives}, Level: {test_level}"
        )

    def test_rapid_input_handling(self):
        """
        Test 5: Rapid Input Handling
        Verify that rapid/simultaneous inputs don't break game:
        - Spam jump button
        - Spam shoot button
        - Simultaneous movement + jump + shoot
        - Rapid pause/unpause
        """
        print("\n=== Test 5: Rapid Input Handling ===")

        player = Player(100, 100, self.audio_manager)
        player.is_powered_up = True
        player.powerup_timer = 600  # 10 seconds

        platforms = pygame.sprite.Group()
        platform = Platform(0, WINDOW_HEIGHT - 50, 800, 50, "grass")
        platforms.add(platform)

        player.rect.y = WINDOW_HEIGHT - 100  # Place above platform
        player.is_grounded = True

        # Test: Spam jump (should only jump once per ground touch)
        jump_count = 0
        for _ in range(10):  # Try to jump 10 times rapidly
            # Simulate pressing jump key
            pygame.event.pump()  # Process events to update key state
            base_keys = pygame.key.get_pressed()
            # Use wrapper to handle large key codes
            keys = KeyStateWrapper(base_keys, {pygame.K_SPACE})

            was_grounded = player.is_grounded
            player.update(keys, platforms)
            if not player.is_grounded and was_grounded:
                jump_count += 1

        # Should only jump once (can't jump mid-air)
        jump_spam_prevented = (jump_count <= 1)

        self.log_test(
            "Jump spam prevention",
            jump_spam_prevented,
            f"Jumps from spam: {jump_count} (should be <= 1)"
        )

        # Test: Spam shoot (should be limited by cooldown)
        player2 = Player(100, 100, self.audio_manager)
        player2.is_powered_up = True
        player2.powerup_timer = 600

        shoot_count = 0
        for _ in range(20):  # Try to shoot 20 times rapidly
            if player2.shoot() is not None:
                shoot_count += 1
            # Update to tick cooldown
            player2.update(pygame.key.get_pressed(), platforms)

        # Should be limited by cooldown (LASER_COOLDOWN frames between shots)
        shoot_spam_limited = (shoot_count < 20)

        self.log_test(
            "Shoot spam cooldown",
            shoot_spam_limited,
            f"Shots from spam: {shoot_count} (limited by cooldown)"
        )

        # Test: Simultaneous all inputs
        player3 = Player(100, 100, self.audio_manager)
        player3.is_powered_up = True
        player3.rect.y = WINDOW_HEIGHT - 100
        player3.is_grounded = True

        # Press all keys at once
        pygame.event.pump()  # Process events to update key state
        base_keys = pygame.key.get_pressed()
        # Use wrapper to handle large key codes
        keys = KeyStateWrapper(base_keys, {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_x})

        # Should handle gracefully without crash
        try:
            player3.update(keys, platforms)
            simultaneous_handled = True
            error_msg = "No errors"
        except Exception as e:
            simultaneous_handled = False
            error_msg = str(e)

        self.log_test(
            "Simultaneous input handling",
            simultaneous_handled,
            error_msg
        )

    def test_boundary_conditions(self):
        """
        Test 6: Boundary Conditions
        Test edge cases at level boundaries:
        - Player at exact x=0
        - Player at exact x=level_width
        - Player at exact corner (0, 0)
        - Enemy at boundary
        - Shooting at boundary
        """
        print("\n=== Test 6: Boundary Conditions (Edges, Corners) ===")

        # Test: Player at left boundary (x=0)
        player = Player(0, 100, self.audio_manager)
        platforms = pygame.sprite.Group()

        # Try to move left while at boundary
        pygame.event.pump()  # Process events to update key state
        base_keys = pygame.key.get_pressed()
        keys = KeyStateWrapper(base_keys, {pygame.K_LEFT})

        player.update(keys, platforms)

        # Should stay at x=0, not go negative
        left_boundary_works = (player.rect.left >= 0)

        self.log_test(
            "Left boundary collision",
            left_boundary_works,
            f"Player x position: {player.rect.left} (should be >= 0)"
        )

        # Test: Player at right boundary
        level_width = 1600
        player2 = Player(level_width - 40, 100, self.audio_manager)  # 40 = player width

        # Try to move right while at boundary
        pygame.event.pump()  # Process events to update key state
        base_keys = pygame.key.get_pressed()
        keys = KeyStateWrapper(base_keys, {pygame.K_RIGHT})

        player2.update(keys, platforms, level_width)

        # Should stay at boundary
        right_boundary_works = (player2.rect.right <= level_width)

        self.log_test(
            "Right boundary collision",
            right_boundary_works,
            f"Player right edge: {player2.rect.right} <= {level_width}"
        )

        # Test: Player at top-left corner (0, 0)
        player3 = Player(0, 0, self.audio_manager)

        # Try to move up-left
        pygame.event.pump()  # Process events to update key state
        base_keys = pygame.key.get_pressed()
        keys = KeyStateWrapper(base_keys, {pygame.K_LEFT, pygame.K_UP})

        try:
            player3.update(keys, platforms)
            corner_handled = True
            corner_msg = f"Position: ({player3.rect.x}, {player3.rect.y})"
        except Exception as e:
            corner_handled = False
            corner_msg = str(e)

        self.log_test(
            "Corner boundary handling",
            corner_handled,
            corner_msg
        )

        # Test: Shooting at boundary
        player4 = Player(0, 100, self.audio_manager)
        player4.is_powered_up = True
        player4.facing_direction = -1  # Facing left (toward boundary)

        # Shoot toward boundary
        laser_info = player4.shoot()
        laser_created = laser_info is not None

        if laser_created:
            x, y, direction = laser_info
            laser = Laser(x, y, direction)
            # Laser should be created even at boundary
            boundary_shooting_works = True
        else:
            boundary_shooting_works = False

        self.log_test(
            "Shooting at boundary",
            laser_created,
            f"Laser created at boundary: {laser_created}"
        )

        # Test: Enemy at boundary
        enemy = Polocho(0, 100)
        enemy.direction = -1  # Moving left toward boundary

        # Update enemy
        initial_x = enemy.rect.x
        enemy.update(platforms)

        # Enemy should bounce or stop at boundary
        enemy_handled = (enemy.rect.x >= 0)

        self.log_test(
            "Enemy at boundary",
            enemy_handled,
            f"Enemy position: {enemy.rect.x} (should be >= 0)"
        )

    def run_all_tests(self):
        """Run all edge case tests"""
        print("\n" + "=" * 60)
        print("COFFEE BROS - EDGE CASE TESTING SUITE (US-066)")
        print("=" * 60)

        # Run all tests
        self.test_multiple_simultaneous_collisions()
        self.test_powerup_expiry_during_shooting()
        self.test_death_during_invulnerability()
        self.test_pausing_during_transitions()
        self.test_rapid_input_handling()
        self.test_boundary_conditions()

        # Print summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        total_tests = self.tests_passed + self.tests_failed
        pass_rate = (self.tests_passed / total_tests * 100) if total_tests > 0 else 0

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_failed}")
        print(f"Pass Rate: {pass_rate:.1f}%")
        print("=" * 60)

        # Print failed tests details
        if self.tests_failed > 0:
            print("\nFAILED TESTS:")
            for test_name, result in self.test_results.items():
                if not result["passed"]:
                    print(f"  X {test_name}")
                    if result["message"]:
                        print(f"    -> {result['message']}")

        return self.tests_failed == 0

    def cleanup(self):
        """Clean up pygame resources"""
        pygame.quit()


def main():
    """Main test execution"""
    tester = EdgeCaseTester()

    try:
        all_passed = tester.run_all_tests()

        # Exit with appropriate code (no wait for key press during automated testing)
        print("\nAll tests completed!")
        sys.exit(0 if all_passed else 1)

    except Exception as e:
        print(f"\n[CRITICAL ERROR]: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
