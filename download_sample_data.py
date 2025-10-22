"""
Helper script to download sample audio files for testing
This downloads a small set of audio samples to test the system
"""

import os
import urllib.request
import json

# Sample audio URLs (public domain or creative commons)
# These are just examples - you'll need to find actual sources
SAMPLE_URLS = {
    'piano': [
        # Add URLs to piano samples here
        # Example format:
        # ('C4', 'https://example.com/piano_c4.wav'),
    ],
    'violin': [
        # Add URLs to violin samples here
    ],
    'flute': [
        # Add URLs to flute samples here
    ]
}


def download_freesound_samples():
    """
    Guide for downloading from Freesound.org
    
    Freesound requires API key registration.
    Visit: https://freesound.org/apiv2/apply
    """
    print("=" * 70)
    print("DOWNLOADING SAMPLE DATA FROM FREESOUND")
    print("=" * 70)
    print("\nFreesound.org is a collaborative database of audio samples.")
    print("To use it, you need to:")
    print("1. Create account at: https://freesound.org/")
    print("2. Apply for API key at: https://freesound.org/apiv2/apply")
    print("3. Install freesound-python: pip install freesound-python")
    print("\nExample search queries:")
    print("  - 'piano note C4'")
    print("  - 'violin single note'")
    print("  - 'tin whistle note'")
    print("  - 'recorder note'")
    print("\n" + "=" * 70 + "\n")


def download_philharmonia_samples():
    """
    Guide for downloading Philharmonia Orchestra samples
    """
    print("=" * 70)
    print("PHILHARMONIA ORCHESTRA SAMPLES")
    print("=" * 70)
    print("\nThe Philharmonia Orchestra provides free instrument samples.")
    print("\nWebsite: https://philharmonia.co.uk/resources/sound-samples/")
    print("\nAvailable instruments:")
    print("  - Violin (multiple articulations)")
    print("  - Many other orchestral instruments")
    print("\nDownload instructions:")
    print("1. Visit the website")
    print("2. Select instrument (e.g., Violin)")
    print("3. Download individual notes or full package")
    print("4. Extract to data/philharmonia/violin/")
    print("5. Rename files to match format: NOTE_001.wav (e.g., C4_001.wav)")
    print("\n" + "=" * 70 + "\n")


def create_test_samples():
    """
    Create synthetic test samples using numpy
    This is for testing the pipeline without real data
    """
    print("=" * 70)
    print("CREATING SYNTHETIC TEST SAMPLES")
    print("=" * 70)
    print("\nGenerating synthetic audio for testing purposes...")
    
    try:
        import numpy as np
        import soundfile as sf
        import librosa
        
        # Create test directory
        test_dir = 'data/test_samples'
        os.makedirs(test_dir, exist_ok=True)
        
        for instrument in ['piano', 'violin', 'shepherds_flute']:
            instrument_dir = os.path.join(test_dir, instrument)
            os.makedirs(instrument_dir, exist_ok=True)
            
            # Generate a few synthetic notes
            notes = ['C4', 'D4', 'E4', 'F4', 'G4']
            
            for note in notes:
                # Convert note to frequency
                midi_note = librosa.note_to_midi(note)
                frequency = librosa.midi_to_hz(midi_note)
                
                # Generate 2 seconds of audio
                duration = 2.0
                sample_rate = 22050
                t = np.linspace(0, duration, int(sample_rate * duration))
                
                # Simple sine wave (not realistic but works for testing)
                audio = 0.5 * np.sin(2 * np.pi * frequency * t)
                
                # Add some harmonics for more realistic sound
                audio += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)
                audio += 0.2 * np.sin(2 * np.pi * frequency * 3 * t)
                
                # Apply envelope (attack, decay, sustain, release)
                envelope = np.ones_like(audio)
                attack_samples = int(0.1 * sample_rate)
                release_samples = int(0.2 * sample_rate)
                
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                envelope[-release_samples:] = np.linspace(1, 0, release_samples)
                
                audio = audio * envelope
                
                # Save
                filename = f"{note}_001.wav"
                filepath = os.path.join(instrument_dir, filename)
                sf.write(filepath, audio, sample_rate)
                
                print(f"  Created: {filepath}")
        
        print(f"\n✓ Synthetic test samples created in {test_dir}/")
        print("\nNote: These are simple synthetic sounds for testing only.")
        print("For real training, you need actual instrument recordings.")
        print("\n" + "=" * 70 + "\n")
        
        return True
        
    except ImportError as e:
        print(f"\n✗ Error: Missing package - {e}")
        print("Install with: pip install numpy soundfile librosa")
        return False


def main():
    """Main function"""
    print("\n" + "=" * 70)
    print("AUDIO CLASSIFIER - SAMPLE DATA DOWNLOAD GUIDE")
    print("=" * 70 + "\n")
    
    print("This script provides guidance for obtaining training data.\n")
    
    # Option 1: Create synthetic test data
    print("OPTION 1: Create Synthetic Test Data (Quick Test)")
    print("-" * 70)
    response = input("Generate synthetic test samples? (y/n): ").lower()
    if response == 'y':
        create_test_samples()
    
    # Option 2: Freesound
    print("\nOPTION 2: Freesound.org (Large Database)")
    print("-" * 70)
    download_freesound_samples()
    
    # Option 3: Philharmonia
    print("\nOPTION 3: Philharmonia Orchestra (High Quality)")
    print("-" * 70)
    download_philharmonia_samples()
    
    # Summary
    print("\nRECOMMENDED WORKFLOW:")
    print("=" * 70)
    print("1. Start with synthetic samples to test pipeline")
    print("2. Download NSynth dataset for piano and violin")
    print("3. Download or record shepherd's flute samples")
    print("4. Supplement with Freesound or Philharmonia if needed")
    print("5. Split data: python prepare_data.py split data/all_samples")
    print("6. Train model: python train.py")
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()


