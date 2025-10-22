"""
Data generator for efficient loading and augmentation during training
"""

import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from typing import Tuple, List
import config
from audio_processor import AudioProcessor


class AudioDataGenerator(keras.utils.Sequence):
    """
    Custom data generator for loading and preprocessing audio files
    """
    
    def __init__(self, data_dir: str, batch_size: int = config.BATCH_SIZE,
                 shuffle: bool = True, augment: bool = False):
        """
        Initialize data generator
        
        Args:
            data_dir: Directory containing instrument subdirectories
            batch_size: Batch size
            shuffle: Whether to shuffle data
            augment: Whether to apply data augmentation
        """
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.augment = augment
        self.processor = AudioProcessor()
        
        # Load file paths and labels
        self.file_paths, self.instrument_labels, self.note_labels = self._load_data()
        self.indexes = np.arange(len(self.file_paths))
        
        if self.shuffle:
            np.random.shuffle(self.indexes)
    
    def _load_data(self) -> Tuple[List[str], List[int], List[int]]:
        """
        Load file paths and create labels
        
        Returns:
            file_paths, instrument_labels, note_labels
        """
        file_paths = []
        instrument_labels = []
        note_labels = []
        
        # Iterate through instrument directories
        for instrument_idx, instrument in enumerate(config.INSTRUMENTS):
            instrument_dir = os.path.join(self.data_dir, instrument)
            
            if not os.path.exists(instrument_dir):
                print(f"Warning: Directory not found: {instrument_dir}")
                continue
            
            # Iterate through audio files in instrument directory
            for filename in os.listdir(instrument_dir):
                if not any(filename.lower().endswith(ext) for ext in ['.wav', '.mp3', '.ogg', '.flac']):
                    continue
                
                # Extract note from filename (e.g., "C3_001.wav" -> "C3")
                note_name = filename.split('_')[0]
                
                if note_name not in config.NOTES:
                    print(f"Warning: Unknown note {note_name} in file {filename}")
                    continue
                
                note_idx = config.NOTES.index(note_name)
                
                file_path = os.path.join(instrument_dir, filename)
                file_paths.append(file_path)
                instrument_labels.append(instrument_idx)
                note_labels.append(note_idx)
        
        return file_paths, instrument_labels, note_labels
    
    def __len__(self) -> int:
        """Number of batches per epoch"""
        return int(np.ceil(len(self.file_paths) / self.batch_size))
    
    def __getitem__(self, index: int) -> Tuple[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Generate one batch of data
        
        Args:
            index: Batch index
            
        Returns:
            X (batch of spectrograms), (y_instrument, y_note)
        """
        # Get batch indexes
        batch_indexes = self.indexes[index * self.batch_size:(index + 1) * self.batch_size]
        
        # Generate data
        X, y_instrument, y_note = self._generate_batch(batch_indexes)
        
        return X, {'instrument_output': y_instrument, 'note_output': y_note}
    
    def _generate_batch(self, batch_indexes: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Generate batch of data"""
        X = []
        y_instrument = []
        y_note = []
        
        for idx in batch_indexes:
            try:
                file_path = self.file_paths[idx]
                
                # Load and process audio
                audio = self.processor.load_audio(file_path)
                
                # Apply augmentation if enabled
                if self.augment:
                    audio = self.processor.apply_augmentations(audio, pitch_shift=False)
                
                # Extract features
                mel_spec = self.processor.extract_mel_spectrogram(audio)
                mel_spec_norm = self.processor.normalize_spectrogram(mel_spec)
                mel_spec_norm = np.expand_dims(mel_spec_norm, axis=-1)
                
                X.append(mel_spec_norm)
                y_instrument.append(self.instrument_labels[idx])
                y_note.append(self.note_labels[idx])
                
            except Exception as e:
                print(f"Error processing file {self.file_paths[idx]}: {str(e)}")
                continue
        
        # Convert to numpy arrays
        X = np.array(X)
        
        # One-hot encode labels
        y_instrument = keras.utils.to_categorical(y_instrument, num_classes=config.NUM_INSTRUMENTS)
        y_note = keras.utils.to_categorical(y_note, num_classes=config.NUM_NOTES)
        
        return X, y_instrument, y_note
    
    def on_epoch_end(self):
        """Update indexes after each epoch"""
        if self.shuffle:
            np.random.shuffle(self.indexes)


def create_data_generators(train_dir: str = config.TRAIN_DIR,
                          val_dir: str = config.VAL_DIR,
                          batch_size: int = config.BATCH_SIZE) -> Tuple[AudioDataGenerator, AudioDataGenerator]:
    """
    Create training and validation data generators
    
    Args:
        train_dir: Training data directory
        val_dir: Validation data directory
        batch_size: Batch size
        
    Returns:
        train_generator, val_generator
    """
    train_generator = AudioDataGenerator(
        train_dir,
        batch_size=batch_size,
        shuffle=True,
        augment=True
    )
    
    val_generator = AudioDataGenerator(
        val_dir,
        batch_size=batch_size,
        shuffle=False,
        augment=False
    )
    
    return train_generator, val_generator


if __name__ == "__main__":
    print("Testing data generator...")
    
    # This will work once you have data organized in the proper structure
    # For now, just test the class can be instantiated
    print("AudioDataGenerator class defined successfully!")
    print(f"Expected data structure:")
    print(f"  {config.TRAIN_DIR}/")
    print(f"    piano/")
    print(f"      C3_001.wav")
    print(f"      C3_002.wav")
    print(f"      ...")
    print(f"    violin/")
    print(f"    shepherds_flute/")


