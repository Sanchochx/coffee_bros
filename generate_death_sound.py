"""
Script to generate a death sound effect for Sancho Bros
Creates a descending tone that sounds sad/failure-like
"""

import numpy as np
import wave

def generate_death_sound():
    """Generate a descending 'sad' tone for death sound effect"""
    sample_rate = 44100
    duration = 0.5  # 0.5 seconds

    # Create time array
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Create descending tone from 800Hz to 200Hz (sad descending sound)
    frequency_start = 800
    frequency_end = 200
    frequency_sweep = np.linspace(frequency_start, frequency_end, len(t))

    # Generate sine wave with frequency sweep
    audio = np.sin(2 * np.pi * frequency_sweep * t)

    # Apply fade out envelope for natural sound
    envelope = np.linspace(1.0, 0.0, len(t))
    audio = audio * envelope

    # Convert to 16-bit PCM format
    audio = (audio * 32767 * 0.3).astype(np.int16)  # 30% volume

    # Write to WAV file (US-067: cross-platform compatible path)
    import os
    output_path = os.path.join('assets', 'sounds', 'death.wav')
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())

    print(f'Death sound generated successfully at {output_path}')
    print(f'Duration: {duration}s, Frequency: {frequency_start}Hz -> {frequency_end}Hz')

if __name__ == '__main__':
    generate_death_sound()
