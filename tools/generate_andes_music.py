"""
Generate Andes mountain theme music for level 2
Traditional Andean music with pan flute (zampoña) and charango sounds
"""
import numpy as np
from scipy.io import wavfile
import os

# Audio parameters
SAMPLE_RATE = 44100
DURATION = 120  # 2 minutes loop
BPM = 95  # Moderate tempo for mountain atmosphere
BEAT_DURATION = 60.0 / BPM

def generate_tone(frequency, duration, sample_rate=44100, envelope='adsr'):
    """Generate a tone with ADSR envelope"""
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Generate base tone
    tone = np.sin(2 * np.pi * frequency * t)

    # Apply ADSR envelope
    if envelope == 'adsr':
        attack = int(0.05 * len(t))
        decay = int(0.1 * len(t))
        sustain_level = 0.7
        release = int(0.2 * len(t))

        envelope = np.ones_like(t)
        # Attack
        envelope[:attack] = np.linspace(0, 1, attack)
        # Decay
        envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
        # Sustain
        envelope[attack+decay:-release] = sustain_level
        # Release
        envelope[-release:] = np.linspace(sustain_level, 0, release)

        tone *= envelope

    return tone

def generate_panflute_note(frequency, duration, sample_rate=44100):
    """Simulate pan flute (zampoña) sound"""
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Fundamental + harmonics (pan flute has distinctive harmonic structure)
    tone = (
        0.6 * np.sin(2 * np.pi * frequency * t) +
        0.2 * np.sin(2 * np.pi * frequency * 2 * t) +
        0.15 * np.sin(2 * np.pi * frequency * 3 * t) +
        0.05 * np.sin(2 * np.pi * frequency * 5 * t)
    )

    # Breathy attack
    breath_noise = np.random.normal(0, 0.03, len(t))
    breath_envelope = np.exp(-10 * t)
    tone += breath_noise * breath_envelope

    # ADSR envelope
    attack = int(0.08 * len(t))
    decay = int(0.15 * len(t))
    sustain_level = 0.6
    release = int(0.25 * len(t))

    envelope = np.ones_like(t)
    envelope[:attack] = np.linspace(0, 1, attack)
    envelope[attack:attack+decay] = np.linspace(1, sustain_level, decay)
    envelope[attack+decay:-release] = sustain_level
    envelope[-release:] = np.linspace(sustain_level, 0, release)

    tone *= envelope

    return tone

def generate_charango_strum(frequencies, duration, sample_rate=44100):
    """Simulate charango (small Andean guitar) strum"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    chord = np.zeros_like(t)

    # Strum effect - notes don't start exactly together
    for i, freq in enumerate(frequencies):
        offset = int(i * 0.005 * sample_rate)  # 5ms stagger
        note_t = t[offset:] if offset < len(t) else np.array([])

        if len(note_t) > 0:
            # Plucked string harmonics
            note = (
                0.5 * np.sin(2 * np.pi * freq * note_t) +
                0.25 * np.sin(2 * np.pi * freq * 2 * note_t) +
                0.15 * np.sin(2 * np.pi * freq * 3 * note_t) +
                0.1 * np.sin(2 * np.pi * freq * 4 * note_t)
            )

            # Pluck envelope
            pluck_env = np.exp(-4 * note_t)
            note *= pluck_env

            chord[offset:offset+len(note)] += note

    return chord * 0.3

# Note frequencies (pentatonic scale, common in Andean music)
# Using A minor pentatonic: A C D E G
A3 = 220.0
C4 = 261.63
D4 = 293.66
E4 = 329.63
G4 = 392.00
A4 = 440.0
C5 = 523.25
D5 = 587.33
E5 = 659.25
G5 = 783.99
A5 = 880.0

# Create the music
total_samples = int(SAMPLE_RATE * DURATION)
music = np.zeros(total_samples)

# Main melody pattern (pan flute)
melody_notes = [
    (E5, 0.5), (D5, 0.5), (C5, 0.5), (A4, 0.5),
    (G4, 1.0), (A4, 0.5), (C5, 0.5),
    (D5, 0.5), (E5, 0.5), (D5, 0.5), (C5, 0.5),
    (A4, 2.0),

    (E5, 0.5), (D5, 0.5), (C5, 0.5), (A4, 0.5),
    (G4, 1.0), (A4, 0.5), (C5, 0.5),
    (E5, 1.0), (D5, 1.0),
    (C5, 2.0),
]

# Counter-melody (lower pan flute)
counter_notes = [
    (A4, 1.0), (C4, 1.0), (E4, 1.0), (G4, 1.0),
    (A4, 1.0), (C4, 1.0), (D4, 1.0), (E4, 1.0),
    (A4, 1.0), (C4, 1.0), (E4, 1.0), (G4, 1.0),
    (A4, 1.0), (G4, 0.5), (E4, 0.5), (C4, 1.0),
]

# Charango chords (Am, C, Dm, G pattern)
chord_progression = [
    ([A3, C4, E4], 2.0),  # Am
    ([C4, E4, G4], 2.0),  # C
    ([D4, A4, D5], 2.0),  # Dm
    ([G4, D4, G4], 2.0),  # G
]

# Build the track
current_pos = 0
loop_count = 0
max_loops = 8  # 8 loops of the pattern

while current_pos < total_samples and loop_count < max_loops:
    # Add melody
    melody_pos = current_pos
    for note, duration in melody_notes:
        note_samples = int(SAMPLE_RATE * duration * BEAT_DURATION)
        if melody_pos + note_samples > total_samples:
            break

        note_audio = generate_panflute_note(note, duration * BEAT_DURATION, SAMPLE_RATE)
        music[melody_pos:melody_pos+len(note_audio)] += note_audio * 0.4
        melody_pos += note_samples

    # Add counter-melody (start after 2 loops)
    if loop_count >= 2:
        counter_pos = current_pos
        for note, duration in counter_notes:
            note_samples = int(SAMPLE_RATE * duration * BEAT_DURATION)
            if counter_pos + note_samples > total_samples:
                break

            note_audio = generate_panflute_note(note * 0.5, duration * BEAT_DURATION, SAMPLE_RATE)
            music[counter_pos:counter_pos+len(note_audio)] += note_audio * 0.25
            counter_pos += note_samples

    # Add charango accompaniment
    chord_pos = current_pos
    for chord_freqs, duration in chord_progression:
        chord_samples = int(SAMPLE_RATE * duration * BEAT_DURATION)
        if chord_pos + chord_samples > total_samples:
            break

        chord_audio = generate_charango_strum(chord_freqs, duration * BEAT_DURATION, SAMPLE_RATE)
        music[chord_pos:chord_pos+len(chord_audio)] += chord_audio * 0.3
        chord_pos += chord_samples

    # Move to next loop
    pattern_duration = sum(d for _, d in melody_notes) * BEAT_DURATION
    current_pos += int(SAMPLE_RATE * pattern_duration)
    loop_count += 1

# Add gentle wind ambiance
wind = np.random.normal(0, 0.02, len(music))
wind_filter = np.sin(np.linspace(0, 4 * np.pi, len(music))) * 0.5 + 0.5
music += wind * wind_filter

# Normalize
music = music / np.max(np.abs(music)) * 0.8

# Fade in and out
fade_duration = int(2 * SAMPLE_RATE)
fade_in = np.linspace(0, 1, fade_duration)
fade_out = np.linspace(1, 0, fade_duration)
music[:fade_duration] *= fade_in
music[-fade_duration:] *= fade_out

# Convert to 16-bit PCM
audio_int16 = np.int16(music * 32767)

# Save
output_path = "assets/music/andes_theme.wav"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
wavfile.write(output_path, SAMPLE_RATE, audio_int16)

print(f"Andes theme music generated successfully!")
print(f"Duration: {DURATION}s at {BPM} BPM")
print(f"Saved to: {output_path}")
