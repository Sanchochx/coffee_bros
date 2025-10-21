"""
Generate placeholder music tracks for Coffee Bros game (US-047).
Creates simple synthesized music using wave files.
"""

import numpy as np
import wave
import os


def generate_tone(frequency, duration, sample_rate=44100, volume=0.3):
    """
    Generate a simple sine wave tone.

    Args:
        frequency (float): Frequency in Hz
        duration (float): Duration in seconds
        sample_rate (int): Sample rate (default 44100 Hz)
        volume (float): Volume level (0.0 to 1.0)

    Returns:
        numpy.ndarray: Audio samples
    """
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = volume * np.sin(2 * np.pi * frequency * t)
    return wave_data


def generate_chord(frequencies, duration, sample_rate=44100, volume=0.2):
    """
    Generate a chord by combining multiple frequencies.

    Args:
        frequencies (list): List of frequencies in Hz
        duration (float): Duration in seconds
        sample_rate (int): Sample rate (default 44100 Hz)
        volume (float): Volume level per tone (0.0 to 1.0)

    Returns:
        numpy.ndarray: Combined audio samples
    """
    chord = np.zeros(int(sample_rate * duration))
    for freq in frequencies:
        chord += generate_tone(freq, duration, sample_rate, volume)
    # Normalize to prevent clipping
    chord = chord / len(frequencies)
    return chord


def save_wav(filename, audio_data, sample_rate=44100):
    """
    Save audio data to a WAV file.

    Args:
        filename (str): Output filename
        audio_data (numpy.ndarray): Audio samples
        sample_rate (int): Sample rate (default 44100 Hz)
    """
    # Convert to 16-bit PCM
    audio_data = np.int16(audio_data * 32767)

    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters: 1 channel (mono), 2 bytes per sample, sample rate
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

    print(f"Generated: {filename}")


def convert_wav_to_ogg(wav_filename, ogg_filename):
    """
    Convert WAV file to OGG format using ffmpeg if available.
    Falls back to keeping WAV file if ffmpeg is not available.

    Args:
        wav_filename (str): Input WAV filename
        ogg_filename (str): Output OGG filename (not used if ffmpeg unavailable)
    """
    import subprocess

    try:
        # Try to convert using ffmpeg
        subprocess.run(
            ['ffmpeg', '-i', wav_filename, '-c:a', 'libvorbis', '-q:a', '4', ogg_filename, '-y'],
            check=True,
            capture_output=True
        )
        print(f"Converted to OGG: {ogg_filename}")
        # Remove WAV file after successful conversion
        os.remove(wav_filename)
    except (subprocess.CalledProcessError, FileNotFoundError):
        # ffmpeg not available - keep WAV file instead
        print(f"Warning: ffmpeg not available. Keeping WAV format.")
        print(f"Note: Update AudioManager to use .wav extension instead of .ogg")


def generate_menu_music(output_file, duration=30):
    """
    Generate upbeat menu music with Colombian/Latin vibes (US-047).
    Simple repetitive melody that loops well.

    Args:
        output_file (str): Output filename
        duration (float): Duration in seconds
    """
    sample_rate = 44100

    # Colombian/Latin-inspired chord progression (I - IV - V - I in C major)
    # C major, F major, G major, C major
    chords = [
        [261.63, 329.63, 392.00],  # C major (C-E-G)
        [349.23, 440.00, 523.25],  # F major (F-A-C)
        [392.00, 493.88, 587.33],  # G major (G-B-D)
        [261.63, 329.63, 392.00],  # C major (C-E-G)
    ]

    # Generate repeating chord pattern
    chord_duration = 1.5  # Each chord lasts 1.5 seconds
    pattern_duration = chord_duration * len(chords)  # 6 seconds per pattern
    num_patterns = int(duration / pattern_duration) + 1

    music = np.array([])

    for _ in range(num_patterns):
        for chord_freqs in chords:
            chord = generate_chord(chord_freqs, chord_duration, sample_rate, volume=0.15)
            music = np.concatenate([music, chord])

    # Trim to exact duration
    music = music[:int(sample_rate * duration)]

    # Add fade out at the end for smooth looping
    fade_duration = int(sample_rate * 0.5)  # 0.5 second fade
    fade_curve = np.linspace(1.0, 0.0, fade_duration)
    music[-fade_duration:] *= fade_curve

    # Save as WAV first
    wav_file = output_file.replace('.ogg', '.wav')
    save_wav(wav_file, music, sample_rate)

    # Convert to OGG
    convert_wav_to_ogg(wav_file, output_file)


def generate_gameplay_music(output_file, duration=45):
    """
    Generate energetic gameplay music (US-047).
    More dynamic than menu music with a driving rhythm.

    Args:
        output_file (str): Output filename
        duration (float): Duration in seconds
    """
    sample_rate = 44100

    # Upbeat melody pattern with higher tempo
    # Using A minor pentatonic scale for energetic feel
    melody_notes = [
        440.00,  # A
        523.25,  # C
        587.33,  # D
        659.25,  # E
        783.99,  # G
        880.00,  # A (octave)
        659.25,  # E
        587.33,  # D
    ]

    note_duration = 0.4  # Each note lasts 0.4 seconds (faster tempo)
    pattern_duration = note_duration * len(melody_notes)
    num_patterns = int(duration / pattern_duration) + 1

    music = np.array([])

    for _ in range(num_patterns):
        for note_freq in melody_notes:
            # Add some bass note (octave down)
            bass_freq = note_freq / 2
            note = generate_tone(note_freq, note_duration, sample_rate, volume=0.2)
            bass = generate_tone(bass_freq, note_duration, sample_rate, volume=0.15)
            combined = note + bass
            music = np.concatenate([music, combined])

    # Trim to exact duration
    music = music[:int(sample_rate * duration)]

    # Add fade out at the end for smooth looping
    fade_duration = int(sample_rate * 0.5)
    fade_curve = np.linspace(1.0, 0.0, fade_duration)
    music[-fade_duration:] *= fade_curve

    # Save as WAV first
    wav_file = output_file.replace('.ogg', '.wav')
    save_wav(wav_file, music, sample_rate)

    # Convert to OGG
    convert_wav_to_ogg(wav_file, output_file)


def generate_victory_music(output_file, duration=20):
    """
    Generate triumphant victory music (US-047).
    Celebratory fanfare-style music.

    Args:
        output_file (str): Output filename
        duration (float): Duration in seconds
    """
    sample_rate = 44100

    # Triumphant ascending melody (fanfare-style)
    # C major scale ascending with emphasis
    fanfare_notes = [
        261.63,  # C
        293.66,  # D
        329.63,  # E
        349.23,  # F
        392.00,  # G
        440.00,  # A
        493.88,  # B
        523.25,  # C (octave)
        523.25,  # C (hold)
        523.25,  # C (hold)
    ]

    note_duration = 0.6  # Slower, more triumphant
    pattern_duration = note_duration * len(fanfare_notes)
    num_patterns = int(duration / pattern_duration) + 1

    music = np.array([])

    for _ in range(num_patterns):
        for i, note_freq in enumerate(fanfare_notes):
            # Make final notes louder for emphasis
            volume = 0.25 if i >= len(fanfare_notes) - 3 else 0.2
            note = generate_tone(note_freq, note_duration, sample_rate, volume=volume)
            music = np.concatenate([music, note])

    # Trim to exact duration
    music = music[:int(sample_rate * duration)]

    # Add fade out at the end
    fade_duration = int(sample_rate * 1.0)  # 1 second fade
    fade_curve = np.linspace(1.0, 0.0, fade_duration)
    music[-fade_duration:] *= fade_curve

    # Save as WAV first
    wav_file = output_file.replace('.ogg', '.wav')
    save_wav(wav_file, music, sample_rate)

    # Convert to OGG
    convert_wav_to_ogg(wav_file, output_file)


def main():
    """Generate all music files for the game (US-047)"""
    # Create music directory if it doesn't exist
    music_dir = os.path.join("assets", "music")
    if not os.path.exists(music_dir):
        os.makedirs(music_dir)
        print(f"Created directory: {music_dir}")

    print("Generating music files for Coffee Bros (US-047)...")
    print("=" * 60)

    # Generate menu music (30 seconds, will loop)
    print("\n1. Generating menu music...")
    menu_music_path = os.path.join(music_dir, "menu_music.ogg")
    generate_menu_music(menu_music_path, duration=30)

    # Generate gameplay music (45 seconds, will loop)
    print("\n2. Generating gameplay music...")
    gameplay_music_path = os.path.join(music_dir, "gameplay_music.ogg")
    generate_gameplay_music(gameplay_music_path, duration=45)

    # Generate victory music (20 seconds, will loop)
    print("\n3. Generating victory music...")
    victory_music_path = os.path.join(music_dir, "victory_music.ogg")
    generate_victory_music(victory_music_path, duration=20)

    print("\n" + "=" * 60)
    print("All music files generated successfully!")
    print(f"Music files saved to: {music_dir}")
    print("\nNote: These are simple placeholder music tracks.")
    print("For production, replace with professionally composed music.")


if __name__ == "__main__":
    main()
