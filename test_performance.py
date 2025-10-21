"""
Performance testing script for Coffee Bros (US-063).
Tests frame rate, load times, and memory usage to ensure game meets performance targets.
"""

import pygame
import sys
import time
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WINDOW_TITLE
from src.level import Level
from src.audio_manager import AudioManager
from src.performance_monitor import PerformanceMonitor


def test_level_loading_times():
    """Test that all levels load within acceptable time (< 2 seconds)."""
    print("=" * 60)
    print("LEVEL LOADING TIME TEST")
    print("=" * 60)
    print("Target: All levels should load in < 2.0 seconds")
    print()

    # Initialize pygame (required for loading levels)
    pygame.init()
    audio_manager = AudioManager()
    audio_manager.set_music_volume(0)  # Mute for testing
    audio_manager.set_sfx_volume(0)

    max_level = 5
    all_passed = True

    for level_num in range(1, max_level + 1):
        try:
            start_time = time.time()
            level = Level.load_from_file(level_num, audio_manager)
            load_time = time.time() - start_time

            # Check if load time meets target
            passed = load_time < 2.0
            status = "PASS" if passed else "FAIL"
            all_passed = all_passed and passed

            print(f"Level {level_num}: {load_time:.3f}s [{status}]")

        except FileNotFoundError:
            print(f"Level {level_num}: Not found [SKIP]")
        except Exception as e:
            print(f"Level {level_num}: Error - {e} [FAIL]")
            all_passed = False

    print()
    print("Overall Loading Test:", "PASSED" if all_passed else "FAILED")
    print()

    pygame.quit()
    return all_passed


def test_frame_rate():
    """Test that game maintains 60 FPS during gameplay."""
    print("=" * 60)
    print("FRAME RATE TEST")
    print("=" * 60)
    print("Target: Maintain 60 FPS (minimum 55 FPS) for 10 seconds")
    print()

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"{WINDOW_TITLE} - Performance Test")
    clock = pygame.time.Clock()

    # Initialize performance monitor
    perf_monitor = PerformanceMonitor(target_fps=FPS)

    # Initialize audio manager (muted for testing)
    audio_manager = AudioManager()
    audio_manager.set_music_volume(0)
    audio_manager.set_sfx_volume(0)

    # Load a test level (Level 1)
    try:
        level = Level.load_from_file(1, audio_manager)
    except Exception as e:
        print(f"Failed to load test level: {e}")
        pygame.quit()
        return False

    # Run game loop for 10 seconds and collect FPS data
    test_duration = 10.0  # seconds
    start_time = time.time()
    frame_count = 0
    fps_samples = []

    print("Running game loop for 10 seconds...")
    print()

    while time.time() - start_time < test_duration:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        # Update entities (simulate gameplay)
        keys = pygame.key.get_pressed()
        level.player.update(keys, level.platforms, level.metadata.get("width", WINDOW_WIDTH))

        for enemy in level.enemies:
            enemy.update(level.platforms)

        for powerup in level.powerups:
            powerup.update()

        # Update performance monitor
        perf_monitor.update()
        fps_samples.append(perf_monitor.current_fps)

        # Simple rendering (black screen - we're just testing update performance)
        screen.fill((0, 0, 0))

        # Draw performance overlay
        perf_monitor.draw_debug_overlay(screen, 10, 10)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

        frame_count += 1

    # Calculate statistics
    avg_fps = sum(fps_samples) / len(fps_samples) if fps_samples else 0
    min_fps = min(fps_samples) if fps_samples else 0
    max_fps = max(fps_samples) if fps_samples else 0

    # Check if FPS meets target
    passed = min_fps >= 55 and avg_fps >= 58

    print(f"Frames rendered: {frame_count}")
    print(f"Average FPS: {avg_fps:.1f}")
    print(f"Minimum FPS: {min_fps:.1f}")
    print(f"Maximum FPS: {max_fps:.1f}")
    print()
    print("Frame Rate Test:", "PASSED" if passed else "FAILED")
    print()

    pygame.quit()
    return passed


def test_memory_stability():
    """Test that memory usage is stable (no major leaks)."""
    print("=" * 60)
    print("MEMORY STABILITY TEST")
    print("=" * 60)
    print("Target: Memory growth < 50 MB over 60 seconds of gameplay")
    print()

    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"{WINDOW_TITLE} - Memory Test")
    clock = pygame.time.Clock()

    # Initialize performance monitor
    perf_monitor = PerformanceMonitor(target_fps=FPS)

    # Initialize audio manager (muted for testing)
    audio_manager = AudioManager()
    audio_manager.set_music_volume(0)
    audio_manager.set_sfx_volume(0)

    # Load a test level
    try:
        level = Level.load_from_file(1, audio_manager)
    except Exception as e:
        print(f"Failed to load test level: {e}")
        pygame.quit()
        return False

    # Run for 60 seconds and track memory
    test_duration = 60.0  # seconds
    start_time = time.time()
    initial_memory = None
    final_memory = None

    print("Running memory test for 60 seconds...")
    print("(This may take a while...)")
    print()

    while time.time() - start_time < test_duration:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        # Update entities (simulate gameplay with lots of activity)
        keys = pygame.key.get_pressed()
        level.player.update(keys, level.platforms, level.metadata.get("width", WINDOW_WIDTH))

        for enemy in level.enemies:
            enemy.update(level.platforms)

        for powerup in level.powerups:
            powerup.update()

        # Update performance monitor
        perf_monitor.update()

        # Store initial and final memory readings
        stats = perf_monitor.get_stats()
        if initial_memory is None:
            initial_memory = stats["memory_mb"]

        final_memory = stats["memory_mb"]

        # Simple rendering
        screen.fill((0, 0, 0))

        # Draw performance overlay
        perf_monitor.draw_debug_overlay(screen, 10, 10)

        # Show progress
        elapsed = time.time() - start_time
        progress_text = f"Test Progress: {elapsed:.1f}/{test_duration}s"
        font = pygame.font.Font(None, 24)
        text = font.render(progress_text, True, (255, 255, 255))
        screen.blit(text, (10, 100))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Calculate memory growth
    memory_growth = final_memory - initial_memory

    # Check if memory growth is acceptable
    passed = memory_growth < 50  # Less than 50 MB growth

    print(f"Initial memory: {initial_memory:.1f} MB")
    print(f"Final memory: {final_memory:.1f} MB")
    print(f"Memory growth: {memory_growth:.1f} MB")
    print()
    print("Memory Stability Test:", "PASSED" if passed else "FAILED")
    print()

    pygame.quit()
    return passed


def main():
    """Run all performance tests."""
    print()
    print("=" * 60)
    print("    SANCHO BROS - PERFORMANCE TESTS")
    print("=" * 60)
    print()

    results = {
        "Level Loading": test_level_loading_times(),
        "Frame Rate": test_frame_rate(),
        "Memory Stability": test_memory_stability()
    }

    # Print summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results.items():
        status = "[PASSED]" if passed else "[FAILED]"
        print(f"{test_name}: {status}")
        all_passed = all_passed and passed

    print()
    print("Overall Result:", "[ALL TESTS PASSED]" if all_passed else "[SOME TESTS FAILED]")
    print("=" * 60)
    print()

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
