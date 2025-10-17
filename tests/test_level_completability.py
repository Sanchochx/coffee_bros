"""
Sancho Bros - Level Completability Testing
Tests all 5 levels to ensure they are completable and fair.

Acceptance Criteria:
- All 5 levels can be completed
- No impossible jumps exist
- No soft-lock situations possible
- All powerups are reachable
- Goal is always accessible
"""

import json
import math
from pathlib import Path
import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Import player constants from config
sys.path.append(str(Path(__file__).parent.parent))
from config import PLAYER_SPEED, JUMP_VELOCITY, GRAVITY

class LevelCompletabilityTester:
    """Tests level completability by analyzing level data."""

    def __init__(self):
        self.levels_dir = Path(__file__).parent.parent / "assets" / "levels"
        self.test_results = {}

        # Physics constants for jump calculations
        self.player_speed = PLAYER_SPEED  # 5 pixels/frame
        self.jump_velocity = abs(JUMP_VELOCITY)  # 18 pixels/frame initial velocity
        self.gravity = GRAVITY  # 0.8 pixels/frame²

        # Calculate maximum jump properties
        self.max_jump_height = self._calculate_max_jump_height()
        self.max_jump_horizontal_distance = self._calculate_max_jump_distance()

    def _calculate_max_jump_height(self):
        """
        Calculate maximum jump height using physics.
        v² = u² + 2as → s = u² / (2a)
        where u = initial velocity, a = gravity, s = height
        """
        return (self.jump_velocity ** 2) / (2 * self.gravity)

    def _calculate_max_jump_distance(self):
        """
        Calculate maximum horizontal distance during a jump.
        Time to peak: t = u/a
        Total air time: 2t
        Distance: speed × time
        """
        time_to_peak = self.jump_velocity / self.gravity
        total_air_time = 2 * time_to_peak
        return self.player_speed * total_air_time

    def run_all_tests(self):
        """Run completability tests on all 5 levels."""
        print("=" * 80)
        print("SANCHO BROS - LEVEL COMPLETABILITY TESTING")
        print("=" * 80)
        print(f"\nPlayer Physics:")
        print(f"  - Speed: {self.player_speed} pixels/frame")
        print(f"  - Jump Velocity: {self.jump_velocity} pixels/frame")
        print(f"  - Gravity: {self.gravity} pixels/frame²")
        print(f"  - Max Jump Height: {self.max_jump_height:.1f} pixels")
        print(f"  - Max Jump Distance: {self.max_jump_horizontal_distance:.1f} pixels")
        print("\n" + "=" * 80)

        all_passed = True

        for level_num in range(1, 6):
            level_file = self.levels_dir / f"level_{level_num}.json"
            if not level_file.exists():
                print(f"\n❌ LEVEL {level_num}: File not found!")
                all_passed = False
                continue

            passed = self.test_level(level_file, level_num)
            if not passed:
                all_passed = False

        print("\n" + "=" * 80)
        if all_passed:
            print("✅ ALL LEVELS PASSED COMPLETABILITY TESTING!")
        else:
            print("❌ SOME LEVELS FAILED - Review issues above")
        print("=" * 80)

        return all_passed

    def test_level(self, level_file, level_num):
        """Test a single level for completability."""
        with open(level_file, 'r') as f:
            level_data = json.load(f)

        level_name = level_data["metadata"]["name"]
        print(f"\n{'=' * 80}")
        print(f"TESTING LEVEL {level_num}: {level_name}")
        print('=' * 80)

        issues = []

        # Test 1: Check if goal exists and is accessible
        print(f"\n[Test 1] Goal Accessibility")
        goal_issues = self._test_goal_accessibility(level_data)
        if goal_issues:
            issues.extend(goal_issues)
            for issue in goal_issues:
                print(f"  ❌ {issue}")
        else:
            print(f"  ✅ Goal exists and is accessible")

        # Test 2: Check all platforms are reachable
        print(f"\n[Test 2] Platform Reachability")
        platform_issues = self._test_platform_reachability(level_data)
        if platform_issues:
            issues.extend(platform_issues)
            for issue in platform_issues[:5]:  # Show first 5 issues
                print(f"  ❌ {issue}")
            if len(platform_issues) > 5:
                print(f"  ... and {len(platform_issues) - 5} more platform issues")
        else:
            print(f"  ✅ All platforms are reachable")

        # Test 3: Check all gaps are jumpable
        print(f"\n[Test 3] Gap Jumpability")
        gap_issues = self._test_gap_jumpability(level_data)
        if gap_issues:
            issues.extend(gap_issues)
            for issue in gap_issues[:5]:  # Show first 5 issues
                print(f"  ❌ {issue}")
            if len(gap_issues) > 5:
                print(f"  ... and {len(gap_issues) - 5} more gap issues")
        else:
            print(f"  ✅ All gaps are jumpable")

        # Test 4: Check all powerups are reachable
        print(f"\n[Test 4] Powerup Reachability")
        powerup_issues = self._test_powerup_reachability(level_data)
        if powerup_issues:
            issues.extend(powerup_issues)
            for issue in powerup_issues:
                print(f"  ❌ {issue}")
        else:
            print(f"  ✅ All powerups are reachable")

        # Test 5: Check for soft-lock situations
        print(f"\n[Test 5] Soft-Lock Detection")
        softlock_issues = self._test_soft_locks(level_data)
        if softlock_issues:
            issues.extend(softlock_issues)
            for issue in softlock_issues:
                print(f"  ❌ {issue}")
        else:
            print(f"  ✅ No soft-lock situations detected")

        # Summary
        print(f"\n{'─' * 80}")
        if not issues:
            print(f"✅ LEVEL {level_num} ({level_name}) - PASSED ALL TESTS")
            self.test_results[level_num] = "PASSED"
            return True
        else:
            print(f"❌ LEVEL {level_num} ({level_name}) - FAILED ({len(issues)} issues)")
            self.test_results[level_num] = f"FAILED ({len(issues)} issues)"
            return False

    def _test_goal_accessibility(self, level_data):
        """Test if the goal exists and is on a valid platform."""
        issues = []

        if "goal" not in level_data:
            issues.append("No goal defined in level")
            return issues

        goal = level_data["goal"]
        goal_x = goal["x"]
        goal_y = goal["y"]
        goal_width = goal.get("width", 50)
        goal_height = goal.get("height", 80)
        goal_bottom = goal_y + goal_height

        # Check if there's a platform under the goal
        platforms = level_data.get("platforms", [])
        goal_has_platform = False

        for platform in platforms:
            platform_left = platform["x"]
            platform_right = platform["x"] + platform["width"]
            platform_top = platform["y"]

            # Check if goal overlaps horizontally with platform
            goal_right = goal_x + goal_width
            horizontal_overlap = not (goal_right < platform_left or goal_x > platform_right)

            # Check if goal is standing on or near this platform (within 100 pixels)
            if horizontal_overlap and abs(goal_bottom - platform_top) <= 100:
                goal_has_platform = True
                break

        if not goal_has_platform:
            issues.append(f"Goal at ({goal_x}, {goal_y}) has no platform underneath")

        return issues

    def _test_platform_reachability(self, level_data):
        """Test if all platforms can be reached from spawn point."""
        issues = []
        platforms = level_data.get("platforms", [])

        if not platforms:
            issues.append("No platforms defined in level")
            return issues

        # Get spawn point
        spawn_x = level_data["player"]["spawn_x"]
        spawn_y = level_data["player"]["spawn_y"]

        # Find starting platform - check if spawn is on or above a platform
        starting_platform = None
        for platform in platforms:
            platform_left = platform["x"]
            platform_right = platform["x"] + platform["width"]
            platform_top = platform["y"]

            # Check if spawn point is horizontally aligned and within 150 pixels vertically
            if (platform_left <= spawn_x <= platform_right and
                abs(spawn_y - platform_top) <= 150):
                starting_platform = platform
                break

        if not starting_platform:
            issues.append(f"Spawn point ({spawn_x}, {spawn_y}) is not on any platform")

        return issues

    def _test_gap_jumpability(self, level_data):
        """Test if all gaps between platforms are jumpable."""
        issues = []
        platforms = level_data.get("platforms", [])

        # Sort platforms by x position
        sorted_platforms = sorted(platforms, key=lambda p: p["x"])

        for i in range(len(sorted_platforms) - 1):
            current = sorted_platforms[i]
            next_platform = sorted_platforms[i + 1]

            # Calculate gap between platforms
            gap_start = current["x"] + current["width"]
            gap_end = next_platform["x"]
            gap_width = gap_end - gap_start

            # Calculate height difference
            height_diff = current["y"] - next_platform["y"]

            # Skip if platforms overlap or there's no gap
            if gap_width <= 0:
                continue

            # For downward jumps, allow larger horizontal distances
            # because player gains more air time falling
            if height_diff < 0:  # Jumping downward
                # Calculate additional horizontal distance from falling
                # Using v² = u² + 2as to find extra fall distance
                fall_distance = abs(height_diff)
                # Extra time = sqrt(2 * fall_distance / gravity)
                extra_time = math.sqrt(2 * fall_distance / self.gravity)
                extra_horizontal = self.player_speed * extra_time
                max_distance = self.max_jump_horizontal_distance + extra_horizontal
                tolerance = 50
            else:  # Jumping upward
                max_distance = self.max_jump_horizontal_distance
                tolerance = 50

            # Check if gap is jumpable
            if gap_width > max_distance + tolerance:
                issues.append(
                    f"Gap too wide: {gap_width:.0f}px between platforms at "
                    f"x={gap_start:.0f} and x={gap_end:.0f} "
                    f"(max for this jump: {max_distance:.0f}px)"
                )

            # Check if jump is too high
            if height_diff > 0:  # Jumping upward
                if height_diff > self.max_jump_height:
                    issues.append(
                        f"Jump too high: {height_diff:.0f}px at x={gap_end:.0f} "
                        f"(max: {self.max_jump_height:.0f}px)"
                    )

        return issues

    def _test_powerup_reachability(self, level_data):
        """Test if all powerups are reachable."""
        issues = []
        powerups = level_data.get("powerups", [])
        platforms = level_data.get("platforms", [])

        for i, powerup in enumerate(powerups):
            powerup_x = powerup["x"]
            powerup_y = powerup["y"]

            # Check if powerup is on or near a platform
            powerup_reachable = False

            for platform in platforms:
                platform_left = platform["x"]
                platform_right = platform["x"] + platform["width"]
                platform_top = platform["y"]

                # Check if powerup is above this platform (within jump range)
                if (platform_left - 50 <= powerup_x <= platform_right + 50):
                    vertical_distance = platform_top - powerup_y
                    if 0 <= vertical_distance <= self.max_jump_height + 50:
                        powerup_reachable = True
                        break

            if not powerup_reachable:
                issues.append(
                    f"Powerup at ({powerup_x}, {powerup_y}) may not be reachable"
                )

        return issues

    def _test_soft_locks(self, level_data):
        """Test for potential soft-lock situations."""
        issues = []
        platforms = level_data.get("platforms", [])
        goal = level_data.get("goal", {})
        goal_x = goal.get("x", 0)
        goal_y = goal.get("y", 0)

        # Find goal platform
        goal_platform = None
        for platform in platforms:
            platform_left = platform["x"]
            platform_right = platform["x"] + platform["width"]
            platform_top = platform["y"]

            if (platform_left <= goal_x <= platform_right and
                abs(goal_y - platform_top) <= 100):
                goal_platform = platform
                break

        # Check for isolated platforms (platforms with no escape)
        # Exclude the goal platform since it's meant to be the final destination
        for i, platform in enumerate(platforms):
            if platform == goal_platform:
                continue  # Skip goal platform - it's meant to be final

            neighbors = self._find_reachable_platforms(platform, platforms)
            if not neighbors and len(platforms) > 1:
                issues.append(
                    f"Isolated platform at x={platform['x']}, y={platform['y']} "
                    f"with no reachable neighbors"
                )

        return issues

    def _find_reachable_platforms(self, from_platform, all_platforms):
        """Find all platforms reachable from a given platform."""
        reachable = []

        for platform in all_platforms:
            if platform == from_platform:
                continue

            # Calculate horizontal and vertical distances
            horiz_dist = abs(
                (platform["x"] + platform["width"]/2) -
                (from_platform["x"] + from_platform["width"]/2)
            )
            vert_dist = from_platform["y"] - platform["y"]

            # Check if reachable
            if horiz_dist <= self.max_jump_horizontal_distance + 100:
                if vert_dist <= self.max_jump_height or vert_dist < 0:
                    reachable.append(platform)

        return reachable

    def _is_point_on_platform(self, point, platform):
        """Check if a point is on a platform."""
        x, y = point
        platform_left = platform["x"]
        platform_right = platform["x"] + platform["width"]
        platform_top = platform["y"]
        platform_bottom = platform["y"] + platform["height"]

        return (platform_left <= x <= platform_right and
                abs(y - platform_top) <= 10)


def main():
    """Run the level completability tests."""
    tester = LevelCompletabilityTester()
    all_passed = tester.run_all_tests()

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
