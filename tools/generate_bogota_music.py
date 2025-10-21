"""
Generate sad, melancholic background music for Bogota level.
Grey, depressing atmosphere with minor keys and slow tempo.
"""

import numpy as np
import wave as wave_module
import os

# Audio settings
SAMPLE_RATE = 44100
DURATION = 30  # 30 second loop
AMPLITUDE = 4096  # Reduced amplitude for sadder, quieter feel

def generate_sine_wave(frequency, duration, sample_rate=SAMPLE_RATE):
    """Generate a sine wave at given frequency."""
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * frequency * t)

def apply_envelope(wave, attack=0.1, decay=0.1, sustain=0.6, release=0.2):
    """Apply ADSR envelope to a wave."""
    length = len(wave)
    envelope = np.ones(length)

    # Attack
    attack_samples = int(length * attack)
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

    # Decay
    decay_samples = int(length * decay)
    decay_end = attack_samples + decay_samples
    envelope[attack_samples:decay_end] = np.linspace(1, sustain, decay_samples)

    # Sustain (already set by decay)

    # Release
    release_samples = int(length * release)
    envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)

    return wave * envelope

# Define a sad, melancholic chord progression in D minor
# D minor, A minor, B♭ major, F major (i-v-VI-III)
chord_progression = [
    # D minor (D, F, A)
    [293.66, 349.23, 440.00],
    # A minor (A, C, E)
    [440.00, 523.25, 659.25],
    # B♭ major (Bb, D, F)
    [466.16, 293.66, 349.23],
    # F major (F, A, C)
    [349.23, 440.00, 523.25]
]

# Timing for each chord (in seconds)
chord_duration = DURATION / len(chord_progression)

# Create the full audio
audio = np.array([])

for chord in chord_progression:
    # Create chord by combining multiple sine waves
    chord_audio = np.zeros(int(SAMPLE_RATE * chord_duration))

    for i, freq in enumerate(chord):
        # Generate sine wave for each note
        wave = generate_sine_wave(freq, chord_duration)

        # Apply envelope to make it less harsh
        wave = apply_envelope(wave, attack=0.05, decay=0.15, sustain=0.6, release=0.2)

        # Different volumes for different notes (root louder)
        volume = 0.4 if i == 0 else 0.25
        chord_audio += wave * volume

    audio = np.concatenate([audio, chord_audio])

# Add a sad melody line (slowly descending minor scale)
melody_notes = [
    (293.66, 1.5),  # D
    (261.63, 1.5),  # C
    (233.08, 1.5),  # Bb
    (220.00, 2.0),  # A
    (196.00, 2.0),  # G
    (174.61, 2.5),  # F
    (293.66, 3.5),  # D (back to root, held longer)
]

melody_audio = np.array([])
melody_start = 0

for note, duration in melody_notes:
    # Generate melody note
    note_duration = duration
    melody_wave = generate_sine_wave(note * 2, note_duration)  # One octave higher

    # Apply envelope for smooth note transitions
    melody_wave = apply_envelope(melody_wave, attack=0.1, decay=0.2, sustain=0.5, release=0.2)

    melody_audio = np.concatenate([melody_audio, melody_wave])

# Pad melody to match length
if len(melody_audio) < len(audio):
    melody_audio = np.concatenate([melody_audio, np.zeros(len(audio) - len(melody_audio))])
else:
    melody_audio = melody_audio[:len(audio)]

# Mix melody with chords (melody quieter)
audio = audio * 0.7 + melody_audio * 0.3

# Add rain/ambient sound effect (simple version without low-pass filter)
rain_duration = len(audio) / SAMPLE_RATE
rain = np.random.normal(0, 0.03, len(audio))  # White noise for rain (quieter)
# Simple smoothing by averaging nearby samples
window_size = 100
rain_smooth = np.convolve(rain, np.ones(window_size)/window_size, mode='same')
audio += rain_smooth * 0.1

# Normalize and convert to 16-bit integers
audio = audio / np.max(np.abs(audio))  # Normalize
audio = (audio * AMPLITUDE).astype(np.int16)

# Fade out at the end for smooth looping
fade_samples = int(SAMPLE_RATE * 2)  # 2 second fade
fade_curve = np.linspace(1, 0, fade_samples)
audio[-fade_samples:] = (audio[-fade_samples:] * fade_curve).astype(np.int16)

# Save as WAV file
output_path = os.path.join("assets", "music", "bogota_theme.wav")
with wave_module.open(output_path, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)  # 16-bit
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(audio.tobytes())

print(f"Bogota theme music saved to {output_path}")
print("A sad, melancholic soundtrack in D minor with rain ambience.")
