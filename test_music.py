"""
Test script to verify music playback works
"""
import pygame
from src.audio_manager import AudioManager

# Initialize pygame
pygame.init()

# Create a small window (required for pygame events)
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Music Test")

# Initialize audio manager
print("Initializing AudioManager...")
audio_manager = AudioManager()

# Test menu music
print("\nTesting menu music playback...")
result = audio_manager.play_menu_music()
print(f"play_menu_music() returned: {result}")
print(f"Is music playing? {audio_manager.is_music_playing()}")
print(f"Current music: {audio_manager.current_music}")
print(f"Music volume: {audio_manager.get_music_volume()}")

# Wait for a few seconds while playing
clock = pygame.time.Clock()
for i in range(180):  # 3 seconds at 60 FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    # Draw something so we know it's running
    screen.fill((50, 50, 50))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Music Test - Frame {i}/180", True, (255, 255, 255))
    screen.blit(text, (50, 100))

    status_text = font.render(f"Music: {'Playing' if audio_manager.is_music_playing() else 'Stopped'}", True, (0, 255, 0) if audio_manager.is_music_playing() else (255, 0, 0))
    screen.blit(status_text, (50, 150))

    pygame.display.flip()
    clock.tick(60)

print("\nStopping music...")
audio_manager.stop_music()

print("\nTest complete!")
pygame.quit()
