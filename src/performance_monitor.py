"""
Performance monitoring system for Coffee Bros.
Tracks FPS, frame time, and memory usage to ensure smooth gameplay.
"""

import pygame
import time
import psutil
import os


class PerformanceMonitor:
    """
    Monitors game performance metrics including FPS, frame time, and memory usage.
    Helps identify performance bottlenecks and ensure 60 FPS target is maintained.
    """

    def __init__(self, target_fps=60, sample_size=60):
        """
        Initialize performance monitor.

        Args:
            target_fps (int): Target frames per second (default: 60)
            sample_size (int): Number of frames to average for metrics (default: 60)
        """
        self.target_fps = target_fps
        self.sample_size = sample_size

        # FPS tracking
        self.frame_times = []  # List of frame times (in milliseconds)
        self.last_frame_time = time.time()

        # Memory tracking
        self.process = psutil.Process(os.getpid())
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        # Performance statistics
        self.current_fps = 0
        self.average_frame_time = 0
        self.current_memory_mb = 0
        self.memory_delta_mb = 0

        # Warning flags
        self.fps_drop_detected = False
        self.memory_leak_detected = False

    def update(self):
        """
        Update performance metrics. Call this once per frame.
        """
        # Calculate frame time
        current_time = time.time()
        frame_time = (current_time - self.last_frame_time) * 1000  # Convert to milliseconds
        self.last_frame_time = current_time

        # Add to frame times list (keep only last sample_size frames)
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.sample_size:
            self.frame_times.pop(0)

        # Calculate average FPS and frame time
        if len(self.frame_times) > 0:
            self.average_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.current_fps = 1000.0 / self.average_frame_time if self.average_frame_time > 0 else 0

        # Update memory usage
        memory_info = self.process.memory_info()
        self.current_memory_mb = memory_info.rss / 1024 / 1024  # Convert bytes to MB
        self.memory_delta_mb = self.current_memory_mb - self.initial_memory

        # Check for performance issues
        self._check_performance_warnings()

    def _check_performance_warnings(self):
        """Check for performance issues and set warning flags."""
        # FPS drop detection (if average FPS is below 55, we have issues)
        self.fps_drop_detected = self.current_fps < (self.target_fps - 5)

        # Memory leak detection (if memory has grown by more than 100 MB)
        self.memory_leak_detected = self.memory_delta_mb > 100

    def get_stats(self):
        """
        Get current performance statistics.

        Returns:
            dict: Dictionary containing performance metrics
        """
        return {
            "fps": round(self.current_fps, 1),
            "frame_time_ms": round(self.average_frame_time, 2),
            "memory_mb": round(self.current_memory_mb, 1),
            "memory_delta_mb": round(self.memory_delta_mb, 1),
            "fps_drop": self.fps_drop_detected,
            "memory_leak": self.memory_leak_detected
        }

    def draw_debug_overlay(self, screen, x=10, y=50):
        """
        Draw performance metrics overlay on screen for debugging.

        Args:
            screen (pygame.Surface): Game screen surface
            x (int): X position for overlay (default: 10)
            y (int): Y position for overlay (default: 50)
        """
        font = pygame.font.Font(None, 24)
        stats = self.get_stats()

        # Determine FPS color (green if good, red if bad)
        fps_color = (0, 255, 0) if stats["fps"] >= 55 else (255, 0, 0)

        # Render FPS
        fps_text = font.render(f"FPS: {stats['fps']}", True, fps_color)
        screen.blit(fps_text, (x, y))

        # Render frame time
        frame_time_text = font.render(f"Frame: {stats['frame_time_ms']}ms", True, (255, 255, 255))
        screen.blit(frame_time_text, (x, y + 25))

        # Render memory usage
        memory_color = (0, 255, 0) if not stats["memory_leak"] else (255, 255, 0)
        memory_text = font.render(f"Memory: {stats['memory_mb']}MB (+{stats['memory_delta_mb']}MB)", True, memory_color)
        screen.blit(memory_text, (x, y + 50))

    def is_performance_good(self):
        """
        Check if performance is meeting targets.

        Returns:
            bool: True if performance is good (no warnings), False otherwise
        """
        return not self.fps_drop_detected and not self.memory_leak_detected

    def reset(self):
        """Reset performance statistics."""
        self.frame_times.clear()
        self.last_frame_time = time.time()
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024
        self.fps_drop_detected = False
        self.memory_leak_detected = False
