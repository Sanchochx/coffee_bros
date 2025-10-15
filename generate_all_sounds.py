"""
Script to generate all sound effects for Sancho Bros game
Creates actual audible sound effects to replace silent placeholders
"""

import numpy as np
import wave
import os


def save_wav(filename, audio, sample_rate=44100):
    """Helper function to save audio array as WAV file"""
    # Convert to 16-bit PCM format
    audio = (audio * 32767 * 0.5).astype(np.int16)  # 50% volume

    output_path = os.path.join('assets', 'sounds', filename)
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())

    print(f'Generated: {filename}')


def generate_jump_sound():
    """Generate jump sound - rising tone (boing!)"""
    sample_rate = 44100
    duration = 0.15  # Short, snappy

    t = np.linspace(0, duration, int(sample_rate * duration))

    # Rising frequency from 200Hz to 600Hz
    frequency_sweep = np.linspace(200, 600, len(t))
    audio = np.sin(2 * np.pi * frequency_sweep * t)

    # Quick fade out
    envelope = np.concatenate([
        np.ones(int(len(t) * 0.6)),
        np.linspace(1.0, 0.0, int(len(t) * 0.4))
    ])
    audio = audio * envelope

    save_wav('jump.wav', audio, sample_rate)


def generate_stomp_sound():
    """Generate stomp sound - short percussive hit"""
    sample_rate = 44100
    duration = 0.2

    t = np.linspace(0, duration, int(sample_rate * duration))

    # Descending tone (squish sound)
    frequency_sweep = np.linspace(400, 100, len(t))
    audio = np.sin(2 * np.pi * frequency_sweep * t)

    # Sharp attack, quick decay
    envelope = np.exp(-t * 15)
    audio = audio * envelope

    save_wav('stomp.wav', audio, sample_rate)


def generate_laser_sound():
    """Generate laser sound - sci-fi zap"""
    sample_rate = 44100
    duration = 0.25

    t = np.linspace(0, duration, int(sample_rate * duration))

    # High frequency sweep (laser zap)
    frequency_sweep = np.linspace(1200, 400, len(t))
    audio = np.sin(2 * np.pi * frequency_sweep * t)

    # Add some noise for texture
    noise = np.random.uniform(-0.1, 0.1, len(t))
    audio = audio + noise

    # Envelope
    envelope = np.exp(-t * 8)
    audio = audio * envelope

    save_wav('laser.wav', audio, sample_rate)


def generate_powerup_sound():
    """Generate powerup sound - ascending magical chime"""
    sample_rate = 44100
    duration = 0.4

    t = np.linspace(0, duration, int(sample_rate * duration))

    # Ascending arpeggio (C-E-G major chord)
    freqs = [523, 659, 784]  # C5, E5, G5
    audio = np.zeros(len(t))

    third = len(t) // 3
    for i, freq in enumerate(freqs):
        start = i * third
        end = min((i + 1) * third + third // 2, len(t))
        segment = t[start:end] - t[start]
        tone = np.sin(2 * np.pi * freq * segment)

        # Envelope for each note
        env = np.exp(-segment * 5)
        audio[start:end] += tone * env

    save_wav('powerup.wav', audio, sample_rate)


def generate_complete_sound():
    """Generate level complete sound - victory fanfare"""
    sample_rate = 44100
    duration = 0.6

    t = np.linspace(0, duration, int(sample_rate * duration))

    # Victory fanfare (ascending notes)
    freqs = [523, 659, 784, 1047]  # C-E-G-C
    audio = np.zeros(len(t))

    quarter = len(t) // 4
    for i, freq in enumerate(freqs):
        start = i * quarter
        end = min((i + 1) * quarter + quarter // 3, len(t))
        segment = t[start:end] - t[start]
        tone = np.sin(2 * np.pi * freq * segment)

        # Envelope
        env = np.exp(-segment * 3)
        audio[start:end] += tone * env

    save_wav('complete.wav', audio, sample_rate)


def generate_death_sound():
    """Generate death sound - sad descending tone"""
    sample_rate = 44100
    duration = 0.5

    t = np.linspace(0, duration, int(sample_rate * duration))

    # Descending tone (sad/failure)
    frequency_sweep = np.linspace(800, 200, len(t))
    audio = np.sin(2 * np.pi * frequency_sweep * t)

    # Fade out
    envelope = np.linspace(1.0, 0.0, len(t))
    audio = audio * envelope

    save_wav('death.wav', audio, sample_rate)


if __name__ == '__main__':
    print('Generating all sound effects for Sancho Bros...\n')

    # Ensure sounds directory exists
    os.makedirs('assets/sounds', exist_ok=True)

    # Generate all sounds
    generate_jump_sound()
    generate_stomp_sound()
    generate_laser_sound()
    generate_powerup_sound()
    generate_complete_sound()
    generate_death_sound()

    print('\nAll sound effects generated successfully!')
    print('Restart the game to hear the new sounds.')
