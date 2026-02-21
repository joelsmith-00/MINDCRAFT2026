"""
Setup script for Virtual Air Drums
Generates basic drum sounds if you don't have WAV files
"""

import numpy as np
from scipy.io import wavfile
import os

def generate_drum_sound(frequency, duration, sample_rate=22050):
    """Generate a simple drum sound using synthesis"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    
    # Create envelope (attack-decay)
    envelope = np.exp(-t * 10)
    
    # Generate tone with harmonics
    signal = np.sin(2 * np.pi * frequency * t)
    signal += 0.5 * np.sin(2 * np.pi * frequency * 2 * t)
    signal += 0.3 * np.sin(2 * np.pi * frequency * 3 * t)
    
    # Add noise for realistic drum sound
    noise = np.random.normal(0, 0.1, len(t))
    
    # Combine and apply envelope
    drum_sound = (signal + noise) * envelope
    
    # Normalize
    drum_sound = drum_sound / np.max(np.abs(drum_sound))
    
    # Convert to 16-bit PCM
    drum_sound = (drum_sound * 32767).astype(np.int16)
    
    return drum_sound

def create_sounds_folder():
    """Create sounds folder and generate drum samples"""
    
    # Create sounds directory
    if not os.path.exists('sounds'):
        os.makedirs('sounds')
        print("✅ Created 'sounds' folder")
    
    # Generate hi-hat sound (high frequency, short)
    print("🎵 Generating hi-hat sound...")
    hihat = generate_drum_sound(frequency=8000, duration=0.1)
    wavfile.write('sounds/hihat.wav', 22050, hihat)
    
    # Generate snare sound (mid frequency, medium)
    print("🎵 Generating snare sound...")
    snare = generate_drum_sound(frequency=200, duration=0.15)
    wavfile.write('sounds/snare.wav', 22050, snare)
    
    # Generate bass drum sound (low frequency, longer)
    print("🎵 Generating bass drum sound...")
    bass = generate_drum_sound(frequency=60, duration=0.3)
    wavfile.write('sounds/bass.wav', 22050, bass)
    
    print("\n✅ All drum sounds generated successfully!")
    print("📁 Sound files created in 'sounds/' folder")

if __name__ == "__main__":
    print("🥁 Virtual Air Drums - Setup Script")
    print("=" * 50)
    print("\nThis script will generate basic drum sounds.")
    print("For better quality, download professional samples.\n")
    
    try:
        create_sounds_folder()
        print("\n✅ Setup complete! You can now run: python air_drums.py")
    except ImportError:
        print("\n⚠️  scipy not found. Installing basic sound generation...")
        print("Run: pip install scipy")
        print("\nOr manually add WAV files to the 'sounds' folder:")
        print("  - sounds/hihat.wav")
        print("  - sounds/snare.wav")
        print("  - sounds/bass.wav")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nManually create a 'sounds' folder and add WAV files:")
        print("  - sounds/hihat.wav")
        print("  - sounds/snare.wav")
        print("  - sounds/bass.wav")
