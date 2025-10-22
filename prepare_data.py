"""
Data preparation script for downloading and organizing training data
"""

import os
import json
import shutil
import urllib.request
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

import config


def create_directory_structure():
    """Create the directory structure for training data"""
    print("Creating directory structure...")
    
    directories = [
        config.DATA_DIR,
        config.TRAIN_DIR,
        config.VAL_DIR,
        config.TEST_DIR,
    ]
    
    for instrument in config.INSTRUMENTS:
        for base_dir in [config.TRAIN_DIR, config.VAL_DIR, config.TEST_DIR]:
            directories.append(os.path.join(base_dir, instrument))
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  Created: {directory}")
    
    print("Directory structure created successfully!\n")


def download_nsynth_dataset():
    """
    Guide for downloading NSynth dataset
    
    Note: NSynth is large (~30GB). This function provides instructions.
    Actual download should be done manually or with specialized tools.
    """
    print("=" * 70)
    print("NSynth DATASET DOWNLOAD INSTRUCTIONS")
    print("=" * 70)
    print("\nThe NSynth dataset is a large dataset (30+ GB) with 300,000+ musical notes.")
    print("It includes piano, violin, and many other instruments.")
    print("\nTo download NSynth:")
    print("1. Visit: https://magenta.tensorflow.org/datasets/nsynth")
    print("2. Download 'nsynth-train.jsonwav.tar.gz' and/or 'nsynth-valid.jsonwav.tar.gz'")
    print("3. Extract the dataset to a temporary directory")
    print("4. Run the filter_nsynth_data() function in this script to extract relevant samples")
    print("\nAlternatively, you can use the tensorflow_datasets library:")
    print("  pip install tensorflow-datasets")
    print("  import tensorflow_datasets as tfds")
    print("  ds = tfds.load('nsynth', split='train')")
    print("\n" + "=" * 70 + "\n")


def filter_nsynth_data(nsynth_dir, output_dir='data/nsynth_filtered'):
    """
    Filter NSynth dataset to extract only piano and violin samples in our note range
    
    Args:
        nsynth_dir: Path to extracted NSynth dataset
        output_dir: Path to save filtered samples
    """
    print("Filtering NSynth dataset...")
    print(f"Source: {nsynth_dir}")
    print(f"Output: {output_dir}")
    
    # Load NSynth metadata
    metadata_path = os.path.join(nsynth_dir, 'examples.json')
    if not os.path.exists(metadata_path):
        print(f"Error: Metadata file not found at {metadata_path}")
        return
    
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Filter samples
    piano_samples = []
    violin_samples = []
    
    # NSynth instrument families
    # Family 0: Bass, 1: Brass, 2: Flute, 3: Guitar, 4: Keyboard, 5: Mallet, 
    # 6: Organ, 7: Reed, 8: String, 9: Synth Lead, 10: Vocal
    
    target_instruments = {
        'keyboard': 'piano',  # Family 4
        'string': 'violin'     # Family 8
    }
    
    for sample_id, sample_data in metadata.items():
        instrument_family = sample_data.get('instrument_family_str', '')
        pitch = sample_data.get('pitch', 0)  # MIDI note number
        
        # Check if in our target range (C3=48 to B5=83)
        if 48 <= pitch <= 83:
            note_name = config.NOTES[pitch - 48]  # Convert MIDI to our note names
            
            if instrument_family in target_instruments:
                instrument = target_instruments[instrument_family]
                audio_file = os.path.join(nsynth_dir, 'audio', f'{sample_id}.wav')
                
                if os.path.exists(audio_file):
                    if instrument == 'piano':
                        piano_samples.append((audio_file, note_name))
                    elif instrument == 'violin':
                        violin_samples.append((audio_file, note_name))
    
    print(f"\nFound {len(piano_samples)} piano samples")
    print(f"Found {len(violin_samples)} violin samples")
    
    # Copy filtered samples
    for samples, instrument in [(piano_samples, 'piano'), (violin_samples, 'violin')]:
        instrument_dir = os.path.join(output_dir, instrument)
        os.makedirs(instrument_dir, exist_ok=True)
        
        note_counts = {}
        for audio_file, note_name in samples:
            # Count samples per note
            if note_name not in note_counts:
                note_counts[note_name] = 0
            note_counts[note_name] += 1
            
            # Copy file
            filename = f"{note_name}_{note_counts[note_name]:03d}.wav"
            dest_path = os.path.join(instrument_dir, filename)
            shutil.copy2(audio_file, dest_path)
        
        print(f"\nCopied {len(samples)} {instrument} samples to {instrument_dir}")
    
    print("\nFiltering complete!")


def create_sample_data_guide():
    """
    Create a guide for manually recording shepherd's flute samples
    """
    guide_path = 'data/recording_guide.txt'
    
    guide_content = """
SHEPHERD'S FLUTE RECORDING GUIDE
================================

This guide will help you record high-quality audio samples for training.

EQUIPMENT NEEDED:
- Shepherd's flute (or substitute: Irish tin whistle, recorder, or similar woodwind)
- Microphone (USB mic or smartphone recorder is fine)
- Quiet recording space
- Audio recording software (Audacity, GarageBand, or phone app)

RECORDING SPECIFICATIONS:
- Sample rate: 44100 Hz (will be downsampled to 22050 Hz)
- Format: WAV (16-bit) or high-quality MP3
- Duration: 2-5 seconds per note
- Quality: Minimal background noise

NOTES TO RECORD (36 total):
C3, C#3, D3, D#3, E3, F3, F#3, G3, G#3, A3, A#3, B3
C4, C#4, D4, D#4, E4, F4, F#4, G4, G#4, A4, A#4, B4
C5, C#5, D5, D#5, E5, F5, F#5, G5, G#5, A5, A#5, B5

RECORDING PROCESS:
1. Tune your instrument
2. Set up in a quiet space
3. Position microphone 6-12 inches from instrument
4. For EACH note, record 100-200 variations:
   - Different volumes (soft, medium, loud)
   - Different articulations (tongued, slurred)
   - Different breath pressures
   - Slightly different starting times
5. Save each recording as: NOTE_XXX.wav
   Example: C3_001.wav, C3_002.wav, ..., C3_100.wav

TIPS:
- Use a tuner app to verify pitch
- Record in batches (all C notes, all D notes, etc.)
- Take breaks to maintain consistent tone quality
- Label files immediately after recording
- Back up your recordings!

ALTERNATIVE OPTION:
If recording is not feasible, you can use samples from:
- Freesound.org (search for "tin whistle" or "recorder")
- Philharmonia Orchestra samples
- Create synthetic samples using audio synthesis

Once recorded, organize files in:
  data/manual_recordings/shepherds_flute/
    C3_001.wav
    C3_002.wav
    ...
"""
    
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    
    print(f"\nRecording guide created: {guide_path}")
    print("Please read this guide for instructions on recording shepherd's flute samples.")


def split_data(source_dir, train_ratio=0.70, val_ratio=0.15, test_ratio=0.15):
    """
    Split data into train/validation/test sets
    
    Args:
        source_dir: Directory containing instrument subdirectories with audio files
        train_ratio: Ratio of data for training
        val_ratio: Ratio of data for validation
        test_ratio: Ratio of data for testing
    """
    print("\nSplitting data into train/validation/test sets...")
    print(f"Ratios: Train={train_ratio}, Val={val_ratio}, Test={test_ratio}")
    
    for instrument in config.INSTRUMENTS:
        instrument_dir = os.path.join(source_dir, instrument)
        
        if not os.path.exists(instrument_dir):
            print(f"Warning: Directory not found: {instrument_dir}")
            continue
        
        # Get all audio files
        audio_files = [f for f in os.listdir(instrument_dir) 
                      if f.lower().endswith(('.wav', '.mp3', '.ogg', '.flac'))]
        
        if len(audio_files) == 0:
            print(f"Warning: No audio files found in {instrument_dir}")
            continue
        
        # Split data
        train_files, temp_files = train_test_split(audio_files, train_size=train_ratio, random_state=42)
        val_files, test_files = train_test_split(temp_files, 
                                                 train_size=val_ratio/(val_ratio + test_ratio), 
                                                 random_state=42)
        
        # Copy files to respective directories
        for files, dest_subdir in [(train_files, config.TRAIN_DIR),
                                   (val_files, config.VAL_DIR),
                                   (test_files, config.TEST_DIR)]:
            dest_dir = os.path.join(dest_subdir, instrument)
            os.makedirs(dest_dir, exist_ok=True)
            
            for filename in files:
                src = os.path.join(instrument_dir, filename)
                dst = os.path.join(dest_dir, filename)
                shutil.copy2(src, dst)
        
        print(f"{instrument}: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test")
    
    print("\nData split complete!")


def create_metadata_csv():
    """Create metadata CSV files for each dataset split"""
    print("\nCreating metadata CSV files...")
    
    for split_name, split_dir in [('train', config.TRAIN_DIR),
                                   ('validation', config.VAL_DIR),
                                   ('test', config.TEST_DIR)]:
        
        metadata = []
        
        for instrument in config.INSTRUMENTS:
            instrument_dir = os.path.join(split_dir, instrument)
            
            if not os.path.exists(instrument_dir):
                continue
            
            for filename in os.listdir(instrument_dir):
                if not any(filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.ogg', '.flac']):
                    continue
                
                # Extract note from filename
                note_name = filename.split('_')[0]
                if note_name not in config.NOTES:
                    continue
                
                filepath = os.path.join(instrument_dir, filename)
                
                metadata.append({
                    'filename': filename,
                    'filepath': filepath,
                    'instrument': instrument,
                    'note': note_name,
                    'midi_note': config.NOTE_TO_MIDI[note_name]
                })
        
        # Save to CSV
        if metadata:
            df = pd.DataFrame(metadata)
            csv_path = os.path.join(config.DATA_DIR, f'{split_name}_metadata.csv')
            df.to_csv(csv_path, index=False)
            print(f"  {split_name}: {len(metadata)} samples -> {csv_path}")
    
    print("Metadata CSV files created!")


def main():
    """Main data preparation workflow"""
    print("\n" + "=" * 70)
    print("AUDIO CLASSIFIER - DATA PREPARATION")
    print("=" * 70 + "\n")
    
    # Step 1: Create directory structure
    create_directory_structure()
    
    # Step 2: Download instructions
    download_nsynth_dataset()
    
    # Step 3: Create recording guide
    create_sample_data_guide()
    
    print("\nNEXT STEPS:")
    print("1. Download NSynth dataset (see instructions above)")
    print("2. Run filter_nsynth_data() to extract piano and violin samples")
    print("3. Record or source shepherd's flute samples (see recording_guide.txt)")
    print("4. Place all samples in data/all_samples/{instrument}/ directories")
    print("5. Run split_data() to create train/val/test splits")
    print("6. Run create_metadata_csv() to create metadata files")
    print("7. Start training with train.py")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'setup':
            create_directory_structure()
        elif command == 'filter' and len(sys.argv) > 2:
            nsynth_dir = sys.argv[2]
            filter_nsynth_data(nsynth_dir)
        elif command == 'split' and len(sys.argv) > 2:
            source_dir = sys.argv[2]
            split_data(source_dir)
        elif command == 'metadata':
            create_metadata_csv()
        else:
            print("Unknown command. Use: setup, filter, split, or metadata")
    else:
        main()


