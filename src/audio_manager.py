"""
Audio Manager Module
Handles loading and playing sound effects for Sancho Bros game.
"""

import pygame
import os


class AudioManager:
    """
    Singleton audio manager for sound effects playback.
    Handles loading sound files and playing them during game events.
    """

    _instance = None  # Singleton instance

    def __new__(cls):
        """Ensure only one instance of AudioManager exists (singleton pattern)"""
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the audio manager and load all sound effects"""
        # Only initialize once (singleton pattern)
        if self._initialized:
            return

        self._initialized = True

        # Initialize pygame mixer for audio (US-040)
        # 44100 Hz frequency, 16-bit samples, 2 channels (stereo), 512 buffer size
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            print("Audio system initialized successfully")
        except pygame.error as e:
            print(f"Warning: Failed to initialize audio system: {e}")
            print("Game will run without sound.")
            self._initialized = True
            self.sounds = {}
            return

        # Set number of mixer channels for simultaneous sounds (US-040: multiple sounds)
        # 8 channels allow multiple sound effects to play at once
        pygame.mixer.set_num_channels(8)

        # Dictionary to store loaded sound effects
        # Key: sound name (string), Value: pygame.mixer.Sound object
        self.sounds = {}

        # Base directory for sound files
        self.sounds_dir = os.path.join("assets", "sounds")

        # Default volume level (0.0 to 1.0)
        self._volume = 0.7  # 70% volume by default

        # Sound effect file names (to be loaded - US-040)
        # These correspond to sound effects needed in later user stories
        self.sound_files = {
            "jump": "jump.wav",           # US-041: Jump sound effect
            "stomp": "stomp.wav",         # US-042: Stomp sound effect
            "laser": "laser.wav",         # US-043: Laser shoot sound effect
            "powerup": "powerup.wav",     # US-044: Powerup collection sound
            "death": "death.wav",         # US-045: Death sound effect
            "level_complete": "complete.wav",  # US-046: Level complete sound
        }

        # Load all sound effects (US-040)
        self._load_sounds()

    def _load_sounds(self):
        """
        Load all sound effects from the sounds directory.
        Handles missing files gracefully without crashing (US-040).
        """
        # Create sounds directory if it doesn't exist
        if not os.path.exists(self.sounds_dir):
            print(f"Warning: Sounds directory not found at '{self.sounds_dir}'. Creating it...")
            try:
                os.makedirs(self.sounds_dir)
            except OSError as e:
                print(f"Error creating sounds directory: {e}")

        # Load each sound file
        for sound_name, filename in self.sound_files.items():
            sound_path = os.path.join(self.sounds_dir, filename)

            try:
                # Load the sound file (US-040: load from files)
                sound = pygame.mixer.Sound(sound_path)
                # Set initial volume
                sound.set_volume(self._volume)
                # Store in dictionary
                self.sounds[sound_name] = sound
                print(f"Loaded sound: {sound_name} from {sound_path}")
            except FileNotFoundError:
                # Handle missing file gracefully (US-040: don't crash)
                print(f"Warning: Sound file not found: {sound_path}. Sound '{sound_name}' will be silent.")
                self.sounds[sound_name] = None  # Store None for missing sounds
            except pygame.error as e:
                # Handle pygame audio errors (e.g., invalid format)
                print(f"Warning: Error loading sound {sound_path}: {e}. Sound '{sound_name}' will be silent.")
                self.sounds[sound_name] = None

    def play_sound(self, sound_name):
        """
        Play a sound effect by name.

        Args:
            sound_name (str): Name of the sound to play (from sound_files dict)

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        print(f"play_sound('{sound_name}') called")

        # Check if sound exists in loaded sounds
        if sound_name not in self.sounds:
            print(f"Warning: Sound '{sound_name}' not registered.")
            return False

        sound = self.sounds[sound_name]

        # Check if sound was loaded successfully (not None)
        if sound is None:
            print(f"Warning: Sound '{sound_name}' is None (failed to load)")
            return False

        try:
            # Play the sound (US-040: triggered by events)
            # play() returns a Channel object, which we don't need to store
            channel = sound.play()
            print(f"Successfully played sound '{sound_name}' on channel: {channel}")
            return True
        except pygame.error as e:
            print(f"Warning: Error playing sound '{sound_name}': {e}")
            return False

    def set_volume(self, volume):
        """
        Set the master volume for all sound effects (US-040: adjustable volume).

        Args:
            volume (float): Volume level from 0.0 (silent) to 1.0 (maximum)
        """
        # Clamp volume to valid range [0.0, 1.0]
        volume = max(0.0, min(1.0, volume))
        self._volume = volume

        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            if sound is not None:  # Skip None (missing) sounds
                sound.set_volume(volume)

    def get_volume(self):
        """
        Get the current master volume level.

        Returns:
            float: Current volume level (0.0 to 1.0)
        """
        return self._volume

    def stop_all_sounds(self):
        """
        Stop all currently playing sound effects.
        Useful for pausing or transitioning between game states.
        """
        pygame.mixer.stop()

    # Convenience methods for specific sound effects (US-041+)
    def play_jump(self):
        """
        Play the jump sound effect (US-041).
        Short, snappy sound when player jumps.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        print("play_jump() called")
        return self.play_sound("jump")

    def play_stomp(self):
        """
        Play the stomp sound effect (US-042).
        Satisfying squish/pop sound when player stomps on an enemy.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        print("play_stomp() called")
        return self.play_sound("stomp")

    def play_laser(self):
        """
        Play the laser shoot sound effect (US-043).
        Sci-fi energy beam sound when player shoots a laser.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        print("play_laser() called")
        return self.play_sound("laser")
