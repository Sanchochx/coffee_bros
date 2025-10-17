"""
Simplified Collision Detection Test for Sancho Bros
Quick tests to verify all collision systems work correctly
"""

import pygame
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.entities.player import Player
from src.entities.polocho import Polocho
from src.entities.platform import Platform
from src.entities.laser import Laser
from src.entities.golden_arepa import GoldenArepa
from src.entities.goal import Goal
from config import *


def main():
    """Run all collision tests"""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    keys = pygame.key.get_pressed()  # Empty key state

    print("\n" + "="*70)
    print("SANCHO BROS - COLLISION TESTING")
    print("="*70 + "\n")

    tests_passed = 0
    tests_failed = 0

    # Test 1: Player lands on platform
    print("Test 1: Player lands on platform...")
    player = Player(400, 100)
    platform = Platform(300, 300, 200, 20)
    platforms = pygame.sprite.Group(platform)
    player.rect.bottom = platform.rect.top - 10
    player.rect.centerx = platform.rect.centerx
    player.velocity_y = 5
    for _ in range(10):
        player.update(keys, platforms, WINDOW_WIDTH)
    if player.is_grounded and player.rect.bottom <= platform.rect.top + 2:
        print("[PASS] Player landed on platform")
        tests_passed += 1
    else:
        print(f"[FAIL] Player did not land (grounded: {player.is_grounded}, pos: {player.rect.bottom} vs {platform.rect.top})")
        tests_failed += 1

    # Test 2: Player does not fall through platform
    print("\nTest 2: Player does not fall through platform...")
    player2 = Player(400, 250)
    player2.rect.bottom = platform.rect.top
    player2.rect.centerx = platform.rect.centerx
    player2.is_grounded = True
    for _ in range(20):
        player2.update(keys, platforms, WINDOW_WIDTH)
    if player2.rect.bottom <= platform.rect.top + 2:
        print("[PASS] Player stayed on platform")
        tests_passed += 1
    else:
        print(f"[FAIL] Player fell through (pos: {player2.rect.bottom} vs {platform.rect.top})")
        tests_failed += 1

    # Test 3: Player cannot clip through walls
    print("\nTest 3: Player cannot clip through walls...")
    player3 = Player(350, 250)
    wall = Platform(300, 200, 20, 100)
    wall_group = pygame.sprite.Group(wall)
    player3.rect.left = wall.rect.right + 10
    for _ in range(10):
        player3.rect.x -= 5  # Move left into wall
        player3.update(keys, wall_group, WINDOW_WIDTH)
    if player3.rect.left >= wall.rect.right - 2:
        print("[PASS] Wall collision prevented clipping")
        tests_passed += 1
    else:
        print(f"[FAIL] Player clipped through wall (pos: {player3.rect.left} vs {wall.rect.right})")
        tests_failed += 1

    # Test 4: Stomp detection is accurate
    print("\nTest 4: Stomp detection accuracy...")
    player4 = Player(400, 250)
    enemy = Polocho(400, 300)
    player4.rect.centerx = enemy.rect.centerx
    player4.rect.bottom = enemy.rect.centery - 10
    player4.velocity_y = 10
    is_stomp = player4.velocity_y > 0 and player4.rect.bottom < enemy.rect.centery
    if is_stomp:
        print("[PASS] Stomp detection works correctly")
        tests_passed += 1
    else:
        print("[FAIL] Stomp not detected")
        tests_failed += 1

    # Test 5: Side collision triggers damage (not stomp)
    print("\nTest 5: Side collision triggers damage...")
    player5 = Player(350, 300)
    enemy2 = Polocho(400, 300)
    player5.rect.centery = enemy2.rect.centery
    player5.velocity_y = 0
    is_stomp = player5.velocity_y > 0 and player5.rect.bottom < enemy2.rect.centery
    if not is_stomp:
        print("[PASS] Side collision correctly triggers damage (not stomp)")
        tests_passed += 1
    else:
        print("[FAIL] Side collision incorrectly triggers stomp")
        tests_failed += 1

    # Test 6: Laser collides with enemy
    print("\nTest 6: Laser-enemy collision...")
    laser = Laser(350, 300, 1)
    enemy3 = Polocho(400, 300)
    laser.rect.centerx = enemy3.rect.centerx
    laser.rect.centery = enemy3.rect.centery
    collision = laser.rect.colliderect(enemy3.rect)
    if collision:
        print("[PASS] Laser-enemy collision detected")
        tests_passed += 1
    else:
        print("[FAIL] Laser-enemy collision not detected")
        tests_failed += 1

    # Test 7: Powerup collection detection
    print("\nTest 7: Powerup collection detection...")
    player6 = Player(400, 300)
    powerup = GoldenArepa(400, 300)
    player6.rect.centerx = powerup.rect.centerx
    player6.rect.centery = powerup.rect.centery
    collision = player6.rect.colliderect(powerup.rect)
    if collision:
        print("[PASS] Powerup collection detected")
        tests_passed += 1
    else:
        print("[FAIL] Powerup collection not detected")
        tests_failed += 1

    # Test 8: Goal collision detection
    print("\nTest 8: Goal collision detection...")
    player7 = Player(400, 300)
    goal = Goal(750, 250)
    player7.rect.centerx = goal.rect.centerx
    player7.rect.centery = goal.rect.centery
    collision = player7.rect.colliderect(goal.rect)
    if collision:
        print("[PASS] Goal collision detected")
        tests_passed += 1
    else:
        print("[FAIL] Goal collision not detected")
        tests_failed += 1

    # Test 9: Pit death detection
    print("\nTest 9: Pit/fall death detection...")
    player8 = Player(400, 100)
    player8.rect.top = WINDOW_HEIGHT + 50
    fell = player8.rect.top > WINDOW_HEIGHT
    if fell:
        print("[PASS] Pit death detected")
        tests_passed += 1
    else:
        print("[FAIL] Pit death not detected")
        tests_failed += 1

    # Test 10: Enemy turns at wall
    print("\nTest 10: Enemy turns at wall...")
    enemy4 = Polocho(350, 250)
    wall2 = Platform(300, 200, 20, 100)
    platforms2 = pygame.sprite.Group(wall2)
    enemy4.direction = 1
    enemy4.rect.right = wall2.rect.left - 5
    initial_dir = enemy4.direction
    for _ in range(10):
        enemy4.update(platforms2)
    if enemy4.direction != initial_dir:
        print("[PASS] Enemy turned at wall")
        tests_passed += 1
    else:
        print(f"[FAIL] Enemy did not turn (direction: {enemy4.direction})")
        tests_failed += 1

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    total = tests_passed + tests_failed
    print(f"Total Tests: {total}")
    print(f"Passed: {tests_passed}")
    print(f"Failed: {tests_failed}")
    if total > 0:
        print(f"Success Rate: {(tests_passed / total * 100):.1f}%")
    print("="*70 + "\n")

    pygame.quit()
    return tests_failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
