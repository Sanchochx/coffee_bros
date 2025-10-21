"""
Generate intense boss battle music for Coffee Bros final level
Dark, dramatic, fast-paced battle theme
"""

import numpy as np
import wave
import os

SAMPLE_RATE = 44100
DURATION = 30  # 30 second loop


def generate_note(frequency, duration, sample_rate=SAMPLE_RATE):
    """Generate a single note"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = np.sin(2 * np.pi * frequency * t)
    return wave_data


def generate_boss_battle_music():
    """
    Generate intense boss battle music
    Dark, dramatic melody with fast percussion-like rhythm
    """
    # Boss battle is in a minor key for dark atmosphere
    # Using D minor scale: D E F G A Bb C
    d_minor_scale = {
        'D3': 146.83,
        'E3': 164.81,
        'F3': 174.61,
        'G3': 196.00,
        'A3': 220.00,
        'Bb3': 233.08,
        'C4': 261.63,
        'D4': 293.66,
        'E4': 329.63,
        'F4': 349.23,
        'G4': 392.00,
        'A4': 440.00,
    }

    # Boss battle melody - intense and dramatic
    melody_notes = [
        ('D3', 0.15), ('D3', 0.15), ('D4', 0.3),
        ('C4', 0.15), ('Bb3', 0.15), ('A3', 0.3),
        ('D3', 0.15), ('D3', 0.15), ('F4', 0.3),
        ('E4', 0.15), ('D4', 0.15), ('C4', 0.3),

        ('A3', 0.15), ('A3', 0.15), ('A4', 0.3),
        ('G4', 0.15), ('F4', 0.15), ('E4', 0.3),
        ('D4', 0.15), ('C4', 0.15), ('Bb3', 0.3),
        ('A3', 0.6),
    ]

    # Bass line - driving force for boss battle
    bass_notes = [
        ('D3', 0.6), ('F3', 0.6),
        ('A3', 0.6), ('G3', 0.6),
        ('D3', 0.6), ('F3', 0.6),
        ('Bb3', 0.6), ('A3', 0.6),
    ]

    # Build melody
    melody = np.array([])
    for _ in range(5):  # Repeat melody 5 times for 30 seconds
        for note, duration in melody_notes:
            if note in d_minor_scale:
                freq = d_minor_scale[note]
                tone = generate_note(freq, duration)
                # Add ADSR envelope for intensity
                envelope = np.linspace(1.0, 0.7, len(tone))
                melody = np.concatenate([melody, tone * envelope * 0.4])

    # Build bass
    bass = np.array([])
    for _ in range(10):  # Repeat bass pattern
        for note, duration in bass_notes:
            if note in d_minor_scale:
                freq = d_minor_scale[note]
                tone = generate_note(freq, duration)
                # Make bass more aggressive with harmonics
                harmonic = generate_note(freq * 2, duration)
                combined = tone * 0.6 + harmonic * 0.2
                bass = np.concatenate([bass, combined * 0.5])

    # Create driving percussion/rhythm (fast heartbeat effect for tension)
    rhythm = np.array([])
    beat_duration = 0.1
    for _ in range(int(DURATION / beat_duration)):
        # Kick drum effect (low frequency pulse)
        kick = generate_note(60, beat_duration) * 0.3
        rhythm = np.concatenate([rhythm, kick])

    # Make all arrays same length
    max_length = max(len(melody), len(bass), len(rhythm))
    melody = np.pad(melody, (0, max_length - len(melody)))
    bass = np.pad(bass, (0, max_length - len(bass)))
    rhythm = np.pad(rhythm, (0, max_length - len(rhythm)))

    # Mix all layers together for epic boss battle sound
    boss_music = melody + bass + rhythm

    # Normalize
    boss_music = boss_music / np.max(np.abs(boss_music))
    boss_music = boss_music * 0.7  # Leave headroom

    # Convert to 16-bit integers
    audio_data = np.int16(boss_music * 32767)

    return audio_data


def save_wav(filename, audio_data, sample_rate=SAMPLE_RATE):
    """Save audio data to WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())


def main():
    """Generate boss battle music"""
    output_dir = "assets/sounds/music"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Boss Battle Music...")
    print("Creating intense, dramatic battle theme...")

    boss_music = generate_boss_battle_music()
    output_file = os.path.join(output_dir, "boss_battle.wav")
    save_wav(output_file, boss_music)

    print(f"Boss battle music saved to: {output_file}")
    print(f"Duration: {DURATION} seconds (loops)")
    print("The soundtrack for epic corruption battle is ready!")


if __name__ == "__main__":
    main()
