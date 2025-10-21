"""
Coffee Bros - Save Manager
Handles loading and saving game progress to persistent storage.
"""

import json
import os


class SaveManager:
    """Manages game save data persistence using JSON file storage (US-068)"""

    def __init__(self, save_file="savegame.json"):
        """Initialize the save manager

        Args:
            save_file (str): Path to save file relative to game root
        """
        # Get the project root directory (parent of src/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.save_file = os.path.join(project_root, save_file)

        # Default save data
        self.default_save_data = {
            "highest_level_completed": 0,  # 0 means no levels completed yet
            "high_score": 0,               # Best score achieved
            "music_volume": 0.7,           # Settings - music volume
            "sfx_volume": 0.7              # Settings - sound effects volume
        }

        # Current save data (loaded or default)
        self.save_data = self.load_save()

    def load_save(self):
        """Load save data from file, or return defaults if file doesn't exist

        Returns:
            dict: Save data dictionary with progress and settings
        """
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    loaded_data = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    save_data = self.default_save_data.copy()
                    save_data.update(loaded_data)
                    print(f"Save file loaded: Level {save_data['highest_level_completed']}, High Score: {save_data['high_score']}")
                    return save_data
            else:
                # File doesn't exist, return defaults (new game)
                print("No save file found - starting new game")
                return self.default_save_data.copy()
        except (json.JSONDecodeError, IOError) as e:
            # If there's an error reading the file, return defaults
            print(f"Warning: Could not load save file from {self.save_file}: {e}")
            print("Starting with default save data")
            return self.default_save_data.copy()

    def save_game(self):
        """Save current game progress to file

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            with open(self.save_file, 'w') as f:
                # Write as human-readable JSON with indentation (US-068 requirement)
                json.dump(self.save_data, f, indent=4)
            print(f"Game saved: Level {self.save_data['highest_level_completed']}, High Score: {self.save_data['high_score']}")
            return True
        except IOError as e:
            print(f"Error: Could not save game to {self.save_file}: {e}")
            return False

    def get_highest_level_completed(self):
        """Get the highest level the player has completed

        Returns:
            int: Highest level number completed (0 if no levels completed)
        """
        return self.save_data.get("highest_level_completed", 0)

    def set_highest_level_completed(self, level_number):
        """Update and save the highest level completed

        Args:
            level_number (int): Level number that was just completed
        """
        current_highest = self.get_highest_level_completed()
        # Only update if this is higher than the current record
        if level_number > current_highest:
            self.save_data["highest_level_completed"] = level_number
            print(f"New highest level completed: {level_number}")
            self.save_game()

    def get_high_score(self):
        """Get the player's high score

        Returns:
            int: Highest score achieved
        """
        return self.save_data.get("high_score", 0)

    def update_high_score(self, score):
        """Update high score if current score is higher

        Args:
            score (int): Current score to compare
        """
        current_high = self.get_high_score()
        # Only update if this score is higher than the current record
        if score > current_high:
            self.save_data["high_score"] = score
            print(f"New high score: {score}")
            self.save_game()

    def get_music_volume(self):
        """Get the saved music volume setting

        Returns:
            float: Music volume (0.0 to 1.0)
        """
        return self.save_data.get("music_volume", self.default_save_data["music_volume"])

    def set_music_volume(self, volume):
        """Set and save the music volume

        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        # Clamp volume to valid range
        volume = max(0.0, min(1.0, volume))
        self.save_data["music_volume"] = volume
        self.save_game()

    def get_sfx_volume(self):
        """Get the saved SFX volume setting

        Returns:
            float: SFX volume (0.0 to 1.0)
        """
        return self.save_data.get("sfx_volume", self.default_save_data["sfx_volume"])

    def set_sfx_volume(self, volume):
        """Set and save the SFX volume

        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        # Clamp volume to valid range
        volume = max(0.0, min(1.0, volume))
        self.save_data["sfx_volume"] = volume
        self.save_game()

    def reset_save_data(self):
        """Reset all save data to defaults (essentially a new game)"""
        self.save_data = self.default_save_data.copy()
        self.save_game()
        print("Save data reset to defaults")
