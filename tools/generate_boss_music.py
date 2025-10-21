"""
Generate EXTREMELY MENACING AND AGGRESSIVE boss battle music for Coffee Bros final level
COMPLETELY DIFFERENT from other levels - industrial, distorted, chaotic
"""

import numpy as np
import wave
import os

SAMPLE_RATE = 44100
DURATION = 30  # 30 second loop


def generate_distorted_wave(frequency, duration, distortion_level=5, sample_rate=SAMPLE_RATE):
    """Generate heavily distorted aggressive wave"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Create base wave
    wave = np.sin(2 * np.pi * frequency * t)
    # Apply EXTREME distortion (clipping and overdrive)
    wave = np.tanh(wave * distortion_level)
    # Add dissonant harmonics
    wave += np.sin(2 * np.pi * frequency * 1.7 * t) * 0.4  # Dissonant interval
    wave += np.sin(2 * np.pi * frequency * 2.3 * t) * 0.3  # More dissonance
    return wave


def generate_noise_burst(duration, intensity=0.3, sample_rate=SAMPLE_RATE):
    """Generate aggressive noise burst for industrial effect"""
    samples = int(sample_rate * duration)
    noise = np.random.uniform(-intensity, intensity, samples)
    # Apply harsh filtering
    return noise


def generate_boss_battle_music():
    """
    Generate EXTREMELY AGGRESSIVE AND MENACING boss battle music
    Industrial metal style with distortion, dissonance, and chaos
    COMPLETELY DIFFERENT from other levels
    """

    # Use DISSONANT frequencies (not a scale - pure aggression)
    aggressive_freqs = {
        'ULTRA_LOW': 40,     # Sub-bass rumble
        'LOW1': 65,          # Deep threatening bass
        'LOW2': 73,          #
        'HEAVY1': 110,       # Heavy distorted
        'HEAVY2': 117,       # Dissonant with HEAVY1
        'MID1': 185,         # Grinding mid
        'MID2': 196,         # Clashing
        'HIGH1': 311,        # Harsh high
        'HIGH2': 370,        # More harsh
        'SIREN': 450,        # Alarm-like
    }

    # INDUSTRIAL AGGRESSIVE RHYTHM - mechanical, relentless
    industrial_pattern = [
        ('LOW1', 0.06, 8),   # (freq, duration, distortion)
        ('LOW1', 0.06, 8),
        ('HEAVY2', 0.12, 10),
        ('LOW1', 0.06, 8),
        ('LOW2', 0.06, 8),
        ('HEAVY1', 0.12, 10),
        ('LOW1', 0.06, 8),
        ('LOW1', 0.06, 8),
        ('HEAVY2', 0.12, 10),
    ]

    # DISSONANT AGGRESSIVE LEAD - chaotic and threatening
    chaos_pattern = [
        ('MID2', 0.08, 6),
        ('HIGH1', 0.08, 6),
        ('MID1', 0.12, 7),
        ('HIGH2', 0.08, 6),
        ('SIREN', 0.06, 5),
        ('MID2', 0.12, 7),
        ('HIGH1', 0.08, 6),
        ('MID1', 0.08, 6),
    ]

    # Build INDUSTRIAL DISTORTED BASS RHYTHM
    industrial_bass = np.array([])
    for _ in range(int(DURATION / 0.6)):  # Loop pattern
        for note, duration, distortion in industrial_pattern:
            freq = aggressive_freqs[note]
            wave = generate_distorted_wave(freq, duration, distortion)
            # Add sub-bass rumble for impact
            sub_rumble = generate_distorted_wave(freq * 0.5, duration, distortion * 0.7) * 0.6
            combined = wave + sub_rumble
            industrial_bass = np.concatenate([industrial_bass, combined * 0.8])

    # Build CHAOTIC AGGRESSIVE LEAD
    chaos_lead = np.array([])
    for _ in range(int(DURATION / 0.6)):  # Loop pattern
        for note, duration, distortion in chaos_pattern:
            freq = aggressive_freqs[note]
            wave = generate_distorted_wave(freq, duration, distortion)
            # Add shrieking harmonic
            screech = generate_distorted_wave(freq * 2.7, duration, distortion * 0.5) * 0.4
            combined = wave + screech
            # Harsh envelope
            envelope = np.linspace(1.0, 0.5, len(combined))
            chaos_lead = np.concatenate([chaos_lead, combined * envelope * 0.5])

    # Create BRUTAL PERCUSSION - industrial drum machine
    brutal_drums = np.array([])
    kick_interval = 0.05  # VERY fast, relentless
    for i in range(int(DURATION / kick_interval)):
        # Alternating heavy kicks with noise bursts
        if i % 8 == 0:  # Heavy accent
            kick = generate_distorted_wave(45, kick_interval, 12) * 0.7
        elif i % 4 == 0:  # Medium accent
            kick = generate_distorted_wave(50, kick_interval, 10) * 0.5
        else:  # Regular beat
            kick = generate_distorted_wave(55, kick_interval, 8) * 0.4

        # Add metallic noise hits randomly
        if i % 3 == 0:
            noise = generate_noise_burst(kick_interval, 0.2)
            kick = kick + noise

        brutal_drums = np.concatenate([brutal_drums, kick])

    # Add SIREN/ALARM effect for extra menace
    siren = np.array([])
    siren_duration = 0.3
    for i in range(int(DURATION / siren_duration)):
        # Sweep from high to low (warning/alarm sound)
        t = np.linspace(0, siren_duration, int(SAMPLE_RATE * siren_duration))
        freq_sweep = np.linspace(600, 400, len(t))
        phase = np.cumsum(2 * np.pi * freq_sweep / SAMPLE_RATE)
        siren_tone = np.sin(phase) * 0.2
        # Add distortion
        siren_tone = np.tanh(siren_tone * 4)
        siren = np.concatenate([siren, siren_tone])

    # Add RANDOM CHAOS BURSTS for unpredictability
    chaos_bursts = np.array([])
    burst_interval = 0.2
    for i in range(int(DURATION / burst_interval)):
        if np.random.random() < 0.3:  # 30% chance of chaos burst
            burst = generate_noise_burst(burst_interval, 0.25)
            # Add harsh frequency spike
            freq = np.random.choice([200, 300, 500, 700])
            spike = generate_distorted_wave(freq, burst_interval, 15) * 0.3
            burst = burst + spike
        else:
            burst = np.zeros(int(burst_interval * SAMPLE_RATE))
        chaos_bursts = np.concatenate([chaos_bursts, burst])

    # Make all arrays same length
    max_length = max(len(industrial_bass), len(chaos_lead), len(brutal_drums), len(siren), len(chaos_bursts))
    industrial_bass = np.pad(industrial_bass, (0, max_length - len(industrial_bass)))
    chaos_lead = np.pad(chaos_lead, (0, max_length - len(chaos_lead)))
    brutal_drums = np.pad(brutal_drums, (0, max_length - len(brutal_drums)))
    siren = np.pad(siren, (0, max_length - len(siren)))
    chaos_bursts = np.pad(chaos_bursts, (0, max_length - len(chaos_bursts)))

    # Mix ALL AGGRESSIVE LAYERS together for MAXIMUM INTENSITY
    boss_music = (industrial_bass * 1.0 +     # Heavy bass foundation
                  chaos_lead * 0.7 +          # Aggressive dissonant lead
                  brutal_drums * 0.9 +        # Relentless percussion
                  siren * 0.6 +               # Menacing alarm
                  chaos_bursts * 0.5)         # Random chaos

    # Normalize with HARD limiting for maximum loudness
    boss_music = boss_music / np.max(np.abs(boss_music))
    boss_music = np.tanh(boss_music * 1.5)  # Soft clipping for extra aggression
    boss_music = boss_music * 0.85  # Very loud

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
    """Generate EXTREMELY AGGRESSIVE boss battle music"""
    output_dir = "assets/music"  # Changed to correct location
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("GENERATING MENACING BOSS BATTLE MUSIC")
    print("=" * 60)
    print("Style: Industrial Metal / Aggressive / Distorted")
    print("Features: Heavy distortion, dissonance, chaos, sirens")
    print("=" * 60)

    boss_music = generate_boss_battle_music()
    output_file = os.path.join(output_dir, "boss_battle.wav")
    save_wav(output_file, boss_music)

    print(f"\n[OK] Boss battle music saved to: {output_file}")
    print(f"[OK] Duration: {DURATION} seconds (loops infinitely)")
    print(f"[OK] Style: COMPLETELY DIFFERENT from other levels")
    print("=" * 60)
    print("THE CORRUPTION BOSS BATTLE SOUNDTRACK IS READY!")
    print("PREPARE FOR MAXIMUM AGGRESSION!")
    print("=" * 60)


if __name__ == "__main__":
    main()
