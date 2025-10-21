"""
Generate Amazon jungle theme music for level 3
Tropical jungle atmosphere with wildlife sounds, percussion, and marimba
"""
import numpy as np
from scipy.io import wavfile
import os

# Audio parameters
SAMPLE_RATE = 44100
DURATION = 120  # 2 minutes loop
BPM = 85  # Relaxed jungle tempo
BEAT_DURATION = 60.0 / BPM

def generate_tone(frequency, duration, sample_rate=44100):
    """Generate a simple sine wave tone"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    return np.sin(2 * np.pi * frequency * t)

def generate_marimba_note(frequency, duration, sample_rate=44100):
    """Simulate marimba/wooden percussion sound"""
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Marimba has strong fundamental and specific harmonic structure
    tone = (
        1.0 * np.sin(2 * np.pi * frequency * t) +
        0.4 * np.sin(2 * np.pi * frequency * 2.76 * t) +  # Characteristic marimba harmonic
        0.2 * np.sin(2 * np.pi * frequency * 5.4 * t) +
        0.1 * np.sin(2 * np.pi * frequency * 8.93 * t)
    )

    # Wooden attack and decay
    attack = int(0.01 * len(t))
    decay_constant = 3.5  # Fast decay typical of wooden percussion

    envelope = np.ones_like(t)
    envelope[:attack] = np.linspace(0, 1, attack)
    envelope[attack:] = np.exp(-decay_constant * t[attack:])

    tone *= envelope

    return tone * 0.5

def generate_wood_block(sample_rate=44100):
    """Generate wood block percussion hit"""
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration))

    # High pitched click with noise
    click = np.sin(2 * np.pi * 800 * t) * np.exp(-40 * t)
    noise = np.random.normal(0, 0.1, len(t)) * np.exp(-50 * t)

    return (click + noise) * 0.3

def generate_shaker(duration, sample_rate=44100):
    """Generate shaker/rain stick sound"""
    samples = int(sample_rate * duration)
    # Filtered noise for shaker
    noise = np.random.normal(0, 0.15, samples)

    # Apply envelope for natural shake
    t = np.linspace(0, duration, samples)
    envelope = np.sin(np.pi * t / duration) ** 2

    return noise * envelope

def generate_bird_call(call_type='chirp', sample_rate=44100):
    """Generate tropical bird call"""
    if call_type == 'chirp':
        duration = 0.3
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Frequency sweep
        f_start = 2000
        f_end = 3500
        freq = f_start + (f_end - f_start) * t / duration

        phase = 2 * np.pi * np.cumsum(freq) / sample_rate
        chirp = np.sin(phase)

        envelope = np.exp(-8 * t)
        return chirp * envelope * 0.15

    elif call_type == 'trill':
        duration = 0.5
        t = np.linspace(0, duration, int(sample_rate * duration))
        # Rapid frequency modulation
        carrier = 2500
        modulation = 200 * np.sin(2 * np.pi * 15 * t)
        trill = np.sin(2 * np.pi * (carrier + modulation) * t)

        envelope = np.exp(-6 * t)
        return trill * envelope * 0.12

    else:  # 'whistle'
        duration = 0.4
        t = np.linspace(0, duration, int(sample_rate * duration))
        whistle = np.sin(2 * np.pi * 1800 * t)
        envelope = np.exp(-7 * t)
        return whistle * envelope * 0.1

def generate_insect_buzz(duration, sample_rate=44100):
    """Generate insect/cicada ambient sound"""
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Multiple frequency components for realistic buzz
    buzz = (
        0.3 * np.sin(2 * np.pi * 4000 * t) +
        0.2 * np.sin(2 * np.pi * 4200 * t) +
        0.15 * np.sin(2 * np.pi * 3800 * t)
    )

    # Amplitude modulation
    am_freq = 30  # Hz
    modulation = 0.5 + 0.5 * np.sin(2 * np.pi * am_freq * t)

    buzz *= modulation

    # Random envelope variations
    envelope = 0.3 + 0.2 * np.sin(2 * np.pi * 0.5 * t)

    return buzz * envelope

# Musical notes (Pentatonic scale for tropical feel)
# Using F minor pentatonic: F Ab Bb C Eb
F3 = 174.61
Ab3 = 207.65
Bb3 = 233.08
C4 = 261.63
Eb4 = 311.13
F4 = 349.23
Ab4 = 415.30
Bb4 = 466.16
C5 = 523.25
Eb5 = 622.25
F5 = 698.46

# Create the music track
total_samples = int(SAMPLE_RATE * DURATION)
music = np.zeros(total_samples)

# Main marimba melody pattern
melody_pattern = [
    (F4, 0.5), (Ab4, 0.5), (C5, 0.5), (Eb5, 0.5),
    (F5, 1.0), (Eb5, 0.5), (C5, 0.5),
    (Ab4, 0.5), (F4, 0.5), (Eb4, 0.5), (F4, 0.5),
    (C4, 2.0),

    (F4, 0.5), (Ab4, 0.5), (Bb4, 0.5), (C5, 0.5),
    (Eb5, 1.0), (C5, 0.5), (Bb4, 0.5),
    (Ab4, 0.5), (F4, 0.5), (Ab4, 0.5), (C5, 0.5),
    (F4, 2.0),
]

# Bass line (simple root notes)
bass_pattern = [
    (F3, 2.0), (Ab3, 2.0), (Bb3, 2.0), (C4, 2.0),
    (F3, 2.0), (Eb4, 2.0), (Ab3, 2.0), (F3, 2.0),
]

# Build the musical track
current_pos = 0
loop_count = 0
max_loops = 4

while current_pos < total_samples and loop_count < max_loops:
    # Add marimba melody
    melody_pos = current_pos
    for note, duration in melody_pattern:
        note_samples = int(SAMPLE_RATE * duration * BEAT_DURATION)
        if melody_pos + note_samples > total_samples:
            break

        note_audio = generate_marimba_note(note, duration * BEAT_DURATION, SAMPLE_RATE)
        end_pos = min(melody_pos + len(note_audio), total_samples)
        music[melody_pos:end_pos] += note_audio[:end_pos - melody_pos] * 0.5
        melody_pos += note_samples

    # Add bass line
    bass_pos = current_pos
    for note, duration in bass_pattern:
        note_samples = int(SAMPLE_RATE * duration * BEAT_DURATION)
        if bass_pos + note_samples > total_samples:
            break

        note_audio = generate_marimba_note(note * 0.5, duration * BEAT_DURATION, SAMPLE_RATE)
        end_pos = min(bass_pos + len(note_audio), total_samples)
        music[bass_pos:end_pos] += note_audio[:end_pos - bass_pos] * 0.35
        bass_pos += note_samples

    # Add percussion (wood blocks on beats)
    if loop_count >= 1:
        perc_pos = current_pos
        pattern_duration = sum(d for _, d in melody_pattern) * BEAT_DURATION
        beats = int(pattern_duration / BEAT_DURATION)

        for beat in range(beats):
            beat_pos = perc_pos + int(beat * BEAT_DURATION * SAMPLE_RATE)
            if beat_pos >= total_samples:
                break

            # Wood block
            wood = generate_wood_block(SAMPLE_RATE)
            end_pos = min(beat_pos + len(wood), total_samples)
            music[beat_pos:end_pos] += wood[:end_pos - beat_pos]

            # Shaker on off-beats
            if beat % 2 == 1:
                shaker = generate_shaker(0.2, SAMPLE_RATE)
                end_pos = min(beat_pos + len(shaker), total_samples)
                music[beat_pos:end_pos] += shaker[:end_pos - beat_pos]

    # Move to next loop
    pattern_duration = sum(d for _, d in melody_pattern) * BEAT_DURATION
    current_pos += int(SAMPLE_RATE * pattern_duration)
    loop_count += 1

# Add ambient jungle sounds throughout
np.random.seed(123)

# Bird calls scattered throughout
num_bird_calls = 25
for _ in range(num_bird_calls):
    call_time = np.random.uniform(0, DURATION - 1)
    call_pos = int(call_time * SAMPLE_RATE)
    call_type = np.random.choice(['chirp', 'trill', 'whistle'])

    bird = generate_bird_call(call_type, SAMPLE_RATE)
    end_pos = min(call_pos + len(bird), total_samples)
    music[call_pos:end_pos] += bird[:end_pos - call_pos]

# Continuous insect ambiance in background
insect_duration = 5.0  # 5-second segments
num_segments = int(DURATION / insect_duration)

for i in range(num_segments):
    segment_start = int(i * insect_duration * SAMPLE_RATE)
    if segment_start >= total_samples:
        break

    insects = generate_insect_buzz(insect_duration, SAMPLE_RATE)
    end_pos = min(segment_start + len(insects), total_samples)
    music[segment_start:end_pos] += insects[:end_pos - segment_start] * 0.15

# Add gentle rustling/wind
rustle = np.random.normal(0, 0.015, len(music))
# Filter to make it more like wind through leaves
rustle_filtered = np.convolve(rustle, np.ones(100)/100, mode='same')
music += rustle_filtered

# Normalize
music = music / np.max(np.abs(music)) * 0.85

# Fade in and out
fade_duration = int(2 * SAMPLE_RATE)
fade_in = np.linspace(0, 1, fade_duration)
fade_out = np.linspace(1, 0, fade_duration)
music[:fade_duration] *= fade_in
music[-fade_duration:] *= fade_out

# Convert to 16-bit PCM
audio_int16 = np.int16(music * 32767)

# Save
output_path = "assets/music/amazon_theme.wav"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
wavfile.write(output_path, SAMPLE_RATE, audio_int16)

print(f"Amazon jungle theme music generated successfully!")
print(f"Duration: {DURATION}s at {BPM} BPM")
print(f"Saved to: {output_path}")
