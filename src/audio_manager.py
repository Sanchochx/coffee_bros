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

        # Music system (US-047)
        self.music_dir = os.path.join("assets", "music")
        self.music_volume = 0.4  # Music volume (lower than SFX to not overpower them)
        self.is_music_muted = False  # Music mute state
        self.current_music = None  # Track currently playing music

        # Music file names (US-047)
        # Using WAV format since ffmpeg/OGG conversion not available
        self.music_files = {
            "menu": "menu_music.wav",      # Background music for menu screens
            "gameplay": "gameplay_music.wav",  # Background music for gameplay levels
            "victory": "victory_music.wav",    # Background music for victory screen
        }

        # Initialize music system (US-047)
        self._init_music()

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
            sound.play()
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

    def set_sfx_volume(self, volume):
        """
        Set the sound effects volume level (US-060: settings menu volume control).
        Alias for set_volume() for clarity in settings menu.

        Args:
            volume (float): Volume level from 0.0 (silent) to 1.0 (maximum)
        """
        self.set_volume(volume)

    def get_sfx_volume(self):
        """
        Get the sound effects volume level (US-060: settings menu volume control).
        Alias for get_volume() for clarity in settings menu.

        Returns:
            float: Current sound effects volume level (0.0 to 1.0)
        """
        return self.get_volume()

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
        return self.play_sound("jump")

    def play_stomp(self):
        """
        Play the stomp sound effect (US-042).
        Satisfying squish/pop sound when player stomps on an enemy.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        return self.play_sound("stomp")

    def play_laser(self):
        """
        Play the laser shoot sound effect (US-043).
        Sci-fi energy beam sound when player shoots a laser.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        return self.play_sound("laser")

    def play_powerup(self):
        """
        Play the powerup collection sound effect (US-044).
        Positive, rewarding sound when player collects a Golden Arepa.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        return self.play_sound("powerup")

    def play_death(self):
        """
        Play the death sound effect (US-045).
        Descending/sad tone when player loses a life from damage or falling.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        return self.play_sound("death")

    def play_level_complete(self):
        """
        Play the level complete sound effect (US-046).
        Triumphant fanfare when player reaches the level goal.

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        return self.play_sound("level_complete")

    # Background Music Methods (US-047)
    def _init_music(self):
        """
        Initialize the music system (US-047).
        Creates music directory if it doesn't exist.
        """
        # Create music directory if it doesn't exist
        if not os.path.exists(self.music_dir):
            print(f"Warning: Music directory not found at '{self.music_dir}'. Creating it...")
            try:
                os.makedirs(self.music_dir)
            except OSError as e:
                print(f"Error creating music directory: {e}")

    def play_music(self, music_name, loops=-1, fade_ms=0):
        """
        Play background music by name (US-047).

        Args:
            music_name (str): Name of the music to play (from music_files dict)
            loops (int): Number of times to loop (-1 = infinite loop, 0 = play once)
            fade_ms (int): Fade in time in milliseconds (default: 0 = no fade)

        Returns:
            bool: True if music started successfully, False otherwise
        """
        # Check if music exists in music files
        if music_name not in self.music_files:
            print(f"Warning: Music '{music_name}' not registered.")
            return False

        # If music is muted, don't play
        if self.is_music_muted:
            print(f"Music is muted, not playing '{music_name}'")
            self.current_music = music_name  # Still track it for when unmuting
            return False

        # Get music file path
        music_file = self.music_files[music_name]
        music_path = os.path.join(self.music_dir, music_file)

        # Check if file exists
        if not os.path.exists(music_path):
            print(f"Warning: Music file not found: {music_path}")
            return False

        try:
            # Stop any currently playing music
            pygame.mixer.music.stop()

            # Load the music file (US-047: WAV format - OGG requires ffmpeg conversion)
            pygame.mixer.music.load(music_path)

            # Set music volume (US-047: lower than SFX)
            pygame.mixer.music.set_volume(self.music_volume)

            # Play the music with looping (US-047: loops seamlessly)
            if fade_ms > 0:
                pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)
            else:
                pygame.mixer.music.play(loops=loops)

            # Track currently playing music
            self.current_music = music_name

            print(f"Playing music: {music_name} from {music_path}")
            return True

        except pygame.error as e:
            print(f"Warning: Error loading/playing music '{music_name}': {e}")
            return False

    def stop_music(self, fade_ms=0):
        """
        Stop the currently playing background music (US-047).

        Args:
            fade_ms (int): Fade out time in milliseconds (default: 0 = immediate stop)
        """
        try:
            if fade_ms > 0:
                pygame.mixer.music.fadeout(fade_ms)
            else:
                pygame.mixer.music.stop()
            self.current_music = None
        except pygame.error as e:
            print(f"Warning: Error stopping music: {e}")

    def set_music_volume(self, volume):
        """
        Set the music volume level (US-047: adjustable volume).

        Args:
            volume (float): Volume level from 0.0 (silent) to 1.0 (maximum)
        """
        # Clamp volume to valid range [0.0, 1.0]
        volume = max(0.0, min(1.0, volume))
        self.music_volume = volume

        # Update pygame music volume
        try:
            pygame.mixer.music.set_volume(volume)
        except pygame.error as e:
            print(f"Warning: Error setting music volume: {e}")

    def get_music_volume(self):
        """
        Get the current music volume level (US-047).

        Returns:
            float: Current music volume level (0.0 to 1.0)
        """
        return self.music_volume

    def mute_music(self):
        """
        Mute the background music (US-047: can be muted in settings).
        Music continues to "play" but at 0 volume.
        """
        self.is_music_muted = True
        try:
            pygame.mixer.music.set_volume(0.0)
            print("Music muted")
        except pygame.error as e:
            print(f"Warning: Error muting music: {e}")

    def unmute_music(self):
        """
        Unmute the background music (US-047).
        Restores music to previous volume level.
        """
        self.is_music_muted = False
        try:
            pygame.mixer.music.set_volume(self.music_volume)
            print("Music unmuted")
        except pygame.error as e:
            print(f"Warning: Error unmuting music: {e}")

    def toggle_music_mute(self):
        """
        Toggle music mute on/off (US-047).

        Returns:
            bool: New mute state (True = muted, False = unmuted)
        """
        if self.is_music_muted:
            self.unmute_music()
        else:
            self.mute_music()
        return self.is_music_muted

    def is_music_playing(self):
        """
        Check if music is currently playing (US-047).

        Returns:
            bool: True if music is playing, False otherwise
        """
        try:
            return pygame.mixer.music.get_busy()
        except pygame.error:
            return False

    # Convenience methods for specific music tracks (US-047)
    def play_menu_music(self):
        """
        Play menu background music with infinite looping (US-047).

        Returns:
            bool: True if music started successfully, False otherwise
        """
        return self.play_music("menu", loops=-1, fade_ms=1000)

    def play_gameplay_music(self):
        """
        Play gameplay background music with infinite looping (US-047).

        Returns:
            bool: True if music started successfully, False otherwise
        """
        return self.play_music("gameplay", loops=-1, fade_ms=1000)

    def play_victory_music(self):
        """
        Play victory screen music with infinite looping (US-047).

        Returns:
            bool: True if music started successfully, False otherwise
        """
        return self.play_music("victory", loops=-1, fade_ms=1000)
