"""
Generate boss pain/damage sound effect for Coffee Bros
A deep, menacing grunt/growl when boss takes damage
"""

import numpy as np
import wave
import os

SAMPLE_RATE = 44100


def generate_boss_pain_sound():
    """
    Generate a menacing boss pain sound
    Deep, distorted growl/grunt effect
    """
    duration = 0.3  # Short impact sound

    # Create base frequency sweep (descending for pain effect)
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration))

    # Start high and sweep down (like a grunt/growl)
    freq_start = 180  # Deep bass start
    freq_end = 80     # Even deeper end
    freq = np.linspace(freq_start, freq_end, len(t))

    # Generate base tone
    phase = np.cumsum(2 * np.pi * freq / SAMPLE_RATE)
    base_tone = np.sin(phase)

    # Add harsh harmonics for menacing/monstrous effect
    harmonic1 = np.sin(phase * 1.5) * 0.4
    harmonic2 = np.sin(phase * 2.3) * 0.3
    harmonic3 = np.sin(phase * 0.7) * 0.3  # Subharmonic for depth

    # Add noise for growl texture
    noise = np.random.uniform(-0.15, 0.15, len(t))

    # Combine all elements
    combined = base_tone + harmonic1 + harmonic2 + harmonic3 + noise

    # Create attack-decay envelope (sharp attack, quick decay)
    attack_time = 0.02
    decay_time = duration - attack_time

    attack_samples = int(attack_time * SAMPLE_RATE)
    decay_samples = len(t) - attack_samples

    attack_env = np.linspace(0, 1, attack_samples)
    decay_env = np.linspace(1, 0, decay_samples)
    envelope = np.concatenate([attack_env, decay_env])

    # Apply envelope
    sound = combined * envelope

    # Normalize
    sound = sound / np.max(np.abs(sound))
    sound = sound * 0.8  # Leave headroom

    # Convert to 16-bit integers
    audio_data = np.int16(sound * 32767)

    return audio_data


def save_wav(filename, audio_data, sample_rate=SAMPLE_RATE):
    """Save audio data to WAV file"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())


def main():
    """Generate boss pain sound"""
    output_dir = "assets/sounds/sfx"
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Boss Pain Sound Effect...")

    boss_pain = generate_boss_pain_sound()
    output_file = os.path.join(output_dir, "boss_pain.wav")
    save_wav(output_file, boss_pain)

    print(f"Boss pain sound saved to: {output_file}")
    print("Duration: 0.3 seconds")
    print("The boss can now express his pain!")


if __name__ == "__main__":
    main()
