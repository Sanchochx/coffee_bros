"""
Coffee Bros - Settings Manager
Handles loading and saving game settings to persistent storage.
"""

import json
import os


class SettingsManager:
    """Manages game settings persistence using JSON file storage"""

    def __init__(self, settings_file="settings.json"):
        """Initialize the settings manager

        Args:
            settings_file (str): Path to settings file relative to game root
        """
        # Get the project root directory (parent of src/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.settings_file = os.path.join(project_root, settings_file)

        # Default settings
        self.default_settings = {
            "music_volume": 0.7,  # 70% default volume
            "sfx_volume": 0.7     # 70% default volume
        }

        # Current settings (loaded or default)
        self.settings = self.load_settings()

    def load_settings(self):
        """Load settings from file, or return defaults if file doesn't exist

        Returns:
            dict: Settings dictionary with volume values
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    settings = self.default_settings.copy()
                    settings.update(loaded_settings)
                    return settings
            else:
                # File doesn't exist, return defaults
                return self.default_settings.copy()
        except (json.JSONDecodeError, IOError) as e:
            # If there's an error reading the file, return defaults
            print(f"Warning: Could not load settings from {self.settings_file}: {e}")
            return self.default_settings.copy()

    def save_settings(self):
        """Save current settings to file

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except IOError as e:
            print(f"Error: Could not save settings to {self.settings_file}: {e}")
            return False

    def get_music_volume(self):
        """Get the current music volume setting

        Returns:
            float: Music volume (0.0 to 1.0)
        """
        return self.settings.get("music_volume", self.default_settings["music_volume"])

    def set_music_volume(self, volume):
        """Set and save the music volume

        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        # Clamp volume to valid range
        volume = max(0.0, min(1.0, volume))
        self.settings["music_volume"] = volume
        self.save_settings()

    def get_sfx_volume(self):
        """Get the current SFX volume setting

        Returns:
            float: SFX volume (0.0 to 1.0)
        """
        return self.settings.get("sfx_volume", self.default_settings["sfx_volume"])

    def set_sfx_volume(self, volume):
        """Set and save the SFX volume

        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        # Clamp volume to valid range
        volume = max(0.0, min(1.0, volume))
        self.settings["sfx_volume"] = volume
        self.save_settings()

    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.settings = self.default_settings.copy()
        self.save_settings()
