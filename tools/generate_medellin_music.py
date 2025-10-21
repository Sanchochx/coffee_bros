"""
Generate Colombian Medellin-style music
Cumbia/Salsa influenced with tropical rhythms
"""

import numpy as np
import wave
import os

SAMPLE_RATE = 44100
DURATION = 45  # 45 second loop


def generate_note(frequency, duration, sample_rate=SAMPLE_RATE):
    """Generate a musical note"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    wave_data = np.sin(2 * np.pi * frequency * t)
    return wave_data


def generate_medellin_music():
    """
    Generate tropical Colombian music in Cumbia/Salsa style
    Upbeat, rhythmic, with Latin percussion feel
    """

    # Colombian/Latin music scale (major with Latin flavor)
    # Using G major for bright, happy feel
    latin_scale = {
        'G3': 196.00,
        'A3': 220.00,
        'B3': 246.94,
        'C4': 261.63,
        'D4': 293.66,
        'E4': 329.63,
        'F#4': 369.99,
        'G4': 392.00,
        'A4': 440.00,
        'B4': 493.88,
        'C5': 523.25,
        'D5': 587.33,
    }

    # CUMBIA-STYLE MELODY - tropical and rhythmic
    cumbia_melody = [
        # Phrase 1 - upbeat opening
        ('G4', 0.3), ('A4', 0.3), ('B4', 0.4),
        ('D5', 0.3), ('B4', 0.3), ('G4', 0.4),
        ('A4', 0.3), ('G4', 0.3), ('E4', 0.4),
        ('D4', 0.6),

        # Phrase 2 - melodic response
        ('G4', 0.3), ('B4', 0.3), ('D5', 0.4),
        ('C5', 0.3), ('B4', 0.3), ('A4', 0.4),
        ('G4', 0.3), ('A4', 0.3), ('B4', 0.4),
        ('G4', 0.6),

        # Phrase 3 - tropical feel
        ('D4', 0.2), ('E4', 0.2), ('G4', 0.3),
        ('B4', 0.3), ('A4', 0.3), ('G4', 0.3),
        ('E4', 0.3), ('D4', 0.5),
    ]

    # BASS LINE - cumbia walking bass (accordion-style)
    cumbia_bass = [
        ('G3', 0.4), ('G3', 0.4), ('D4', 0.4), ('G3', 0.4),
        ('C4', 0.4), ('C4', 0.4), ('G3', 0.4), ('C4', 0.4),
        ('D4', 0.4), ('D4', 0.4), ('A3', 0.4), ('D4', 0.4),
        ('G3', 0.4), ('B3', 0.4), ('D4', 0.4), ('G3', 0.4),
    ]

    # Build TROPICAL MELODY
    melody = np.array([])
    for _ in range(8):  # Repeat for full duration
        for note, duration in cumbia_melody:
            if note in latin_scale:
                freq = latin_scale[note]
                tone = generate_note(freq, duration)
                # Add bright harmonics for tropical sound
                harmonic = generate_note(freq * 2, duration) * 0.3
                combined = tone + harmonic
                # Bouncy envelope
                attack_len = len(combined) // 4
                decay_len = len(combined) - attack_len
                envelope = np.concatenate([
                    np.linspace(0.8, 1.0, attack_len),
                    np.linspace(1.0, 0.7, decay_len)
                ])
                melody = np.concatenate([melody, combined * envelope * 0.5])

    # Build GROOVY BASS LINE
    bass = np.array([])
    for _ in range(14):  # Repeat bass pattern
        for note, duration in cumbia_bass:
            if note in latin_scale:
                freq = latin_scale[note]
                tone = generate_note(freq, duration)
                # Add richness with octave
                octave = generate_note(freq * 2, duration) * 0.2
                combined = tone + octave
                bass = np.concatenate([bass, combined * 0.6])

    # Create LATIN PERCUSSION RHYTHM (clave/guiro feel)
    percussion = np.array([])
    beat_duration = 0.15  # Quick, syncopated
    clave_pattern = [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0]  # Rumba clave

    for i in range(int(DURATION / beat_duration)):
        pattern_index = i % len(clave_pattern)
        if clave_pattern[pattern_index] == 1:
            # High percussion hit
            hit = generate_note(800, beat_duration) * 0.3
            # Add click/snap sound
            noise = np.random.uniform(-0.15, 0.15, len(hit))
            percussion_hit = hit + noise * 0.5
        else:
            # Soft background rhythm
            hit = generate_note(400, beat_duration) * 0.1
            percussion_hit = hit

        # Sharp decay envelope
        env = np.linspace(1.0, 0.0, len(percussion_hit))
        percussion = np.concatenate([percussion, percussion_hit * env])

    # Add GUIRO/SHAKER effect (high frequency scratch)
    shaker = np.array([])
    shake_duration = 0.08
    for i in range(int(DURATION / shake_duration)):
        if i % 2 == 0:  # Every other beat
            shake_noise = np.random.uniform(-0.2, 0.2, int(shake_duration * SAMPLE_RATE))
            shaker = np.concatenate([shaker, shake_noise])
        else:
            silence = np.zeros(int(shake_duration * SAMPLE_RATE))
            shaker = np.concatenate([shaker, silence])

    # Add MARIMBA-STYLE CHORDS (tropical Colombian flavor)
    marimba = np.array([])
    chord_duration = 0.6
    chords = [
        [196, 246, 293],  # G major
        [261, 329, 392],  # C major
        [293, 369, 440],  # D major
        [196, 246, 293],  # G major
    ]

    for _ in range(int(DURATION / (chord_duration * len(chords)))):
        for chord_freqs in chords:
            chord_sound = np.zeros(int(chord_duration * SAMPLE_RATE))
            for freq in chord_freqs:
                tone = generate_note(freq, chord_duration) * 0.25
                chord_sound = chord_sound + tone
            # Bright plucky envelope
            env = np.linspace(1.0, 0.3, len(chord_sound))
            marimba = np.concatenate([marimba, chord_sound * env])

    # Make all arrays same length
    max_length = max(len(melody), len(bass), len(percussion), len(shaker), len(marimba))
    melody = np.pad(melody, (0, max_length - len(melody)))
    bass = np.pad(bass, (0, max_length - len(bass)))
    percussion = np.pad(percussion, (0, max_length - len(percussion)))
    shaker = np.pad(shaker, (0, max_length - len(shaker)))
    marimba = np.pad(marimba, (0, max_length - len(marimba)))

    # Mix CUMBIA/SALSA layers
    medellin_music = (melody * 0.6 +         # Tropical melody
                      bass * 0.7 +            # Groovy bass
                      percussion * 0.5 +      # Latin percussion
                      shaker * 0.3 +          # Shaker/guiro
                      marimba * 0.6)          # Marimba chords

    # Normalize with warm compression
    medellin_music = medellin_music / np.max(np.abs(medellin_music))
    medellin_music = medellin_music * 0.75  # Comfortable volume

    # Convert to 16-bit integers
    audio_data = np.int16(medellin_music * 32767)

    return audio_data


def save_wav(filename, audio_data, sample_rate=SAMPLE_RATE):
    """Save audio data to WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())


def main():
    """Generate Medellin-style music"""
    output_dir = "assets/music"
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("GENERATING MEDELLIN MUSIC")
    print("=" * 60)
    print("Style: Colombian Cumbia/Salsa - Tropical")
    print("Features: Latin percussion, marimba, groovy bass")
    print("=" * 60)

    medellin_music = generate_medellin_music()
    output_file = os.path.join(output_dir, "medellin_theme.wav")
    save_wav(output_file, medellin_music)

    print(f"\n[OK] Medellin music saved to: {output_file}")
    print(f"[OK] Duration: {DURATION} seconds (loops)")
    print(f"[OK] Style: Colombian tropical cumbia")
    print("=" * 60)
    print("MEDELLIN - CITY OF ETERNAL SPRING SOUNDTRACK READY!")
    print("=" * 60)


if __name__ == "__main__":
    main()
