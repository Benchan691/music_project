"""
Audio preprocessing module for instrument and note classification
"""

import librosa
import numpy as np
import soundfile as sf
from typing import Tuple, Optional
import config


class AudioProcessor:
    """Handles audio loading, preprocessing, and feature extraction"""
    
    def __init__(self, sample_rate=config.SAMPLE_RATE, duration=config.DURATION,
                 n_mels=config.N_MELS, hop_length=config.HOP_LENGTH, n_fft=config.N_FFT,
                 trim_silence=config.TRIM_SILENCE, top_db=config.SILENCE_THRESHOLD_DB):
        self.sample_rate = sample_rate
        self.duration = duration
        self.n_mels = n_mels
        self.hop_length = hop_length
        self.n_fft = n_fft
        self.target_length = int(sample_rate * duration)
        self.trim_silence = trim_silence
        self.top_db = top_db  # Threshold in dB below reference for silence detection
    
    def load_audio(self, file_path: str) -> np.ndarray:
        """
        Load audio file and resample to target sample rate
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Audio signal as numpy array
        """
        try:
            # Load audio file
            audio, sr = librosa.load(file_path, sr=self.sample_rate, mono=True)
            
            # Trim silence from beginning and end
            if self.trim_silence:
                audio, _ = librosa.effects.trim(audio, top_db=self.top_db)
            
            # Pad or trim to target duration
            audio = self._pad_or_trim(audio)
            
            return audio
        except Exception as e:
            raise ValueError(f"Error loading audio file {file_path}: {str(e)}")
    
    def _pad_or_trim(self, audio: np.ndarray) -> np.ndarray:
        """Pad or trim audio to target length"""
        if len(audio) < self.target_length:
            # Pad with zeros
            padding = self.target_length - len(audio)
            audio = np.pad(audio, (0, padding), mode='constant')
        elif len(audio) > self.target_length:
            # Trim to target length
            audio = audio[:self.target_length]
        return audio
    
    def extract_mel_spectrogram(self, audio: np.ndarray) -> np.ndarray:
        """
        Extract mel spectrogram from audio signal
        
        Args:
            audio: Audio signal
            
        Returns:
            Mel spectrogram (n_mels, time_steps)
        """
        # Compute mel spectrogram
        mel_spec = librosa.feature.melspectrogram(
            y=audio,
            sr=self.sample_rate,
            n_mels=self.n_mels,
            hop_length=self.hop_length,
            n_fft=self.n_fft,
            fmax=8000
        )
        
        # Convert to log scale (dB)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        
        return mel_spec_db
    
    def normalize_spectrogram(self, mel_spec: np.ndarray) -> np.ndarray:
        """Normalize mel spectrogram to [0, 1] range"""
        # Normalize to 0-1 range
        mel_spec_norm = (mel_spec - mel_spec.min()) / (mel_spec.max() - mel_spec.min() + 1e-8)
        return mel_spec_norm
    
    def process_audio_file(self, file_path: str) -> np.ndarray:
        """
        Complete preprocessing pipeline: load -> extract features -> normalize
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Preprocessed mel spectrogram ready for model input
        """
        # Load audio
        audio = self.load_audio(file_path)
        
        # Extract mel spectrogram
        mel_spec = self.extract_mel_spectrogram(audio)
        
        # Normalize
        mel_spec_norm = self.normalize_spectrogram(mel_spec)
        
        # Add channel dimension for CNN input
        mel_spec_norm = np.expand_dims(mel_spec_norm, axis=-1)
        
        return mel_spec_norm
    
    # Data augmentation methods
    def augment_time_stretch(self, audio: np.ndarray, rate: Optional[float] = None) -> np.ndarray:
        """
        Apply time stretching augmentation
        
        Args:
            audio: Audio signal
            rate: Stretch rate (1.0 = no change, <1 = slower, >1 = faster)
            
        Returns:
            Time-stretched audio
        """
        if rate is None:
            rate = np.random.uniform(*config.AUGMENT_TIME_STRETCH_RANGE)
        
        stretched = librosa.effects.time_stretch(audio, rate=rate)
        return self._pad_or_trim(stretched)
    
    def augment_pitch_shift(self, audio: np.ndarray, n_steps: Optional[int] = None) -> np.ndarray:
        """
        Apply pitch shifting augmentation
        
        Args:
            audio: Audio signal
            n_steps: Number of semitones to shift (positive or negative)
            
        Returns:
            Pitch-shifted audio
        """
        if n_steps is None:
            n_steps = np.random.randint(*config.AUGMENT_PITCH_SHIFT_RANGE)
        
        shifted = librosa.effects.pitch_shift(
            audio, sr=self.sample_rate, n_steps=n_steps
        )
        return shifted
    
    def augment_add_noise(self, audio: np.ndarray, snr_db: Optional[float] = None) -> np.ndarray:
        """
        Add white noise to audio
        
        Args:
            audio: Audio signal
            snr_db: Signal-to-noise ratio in dB
            
        Returns:
            Audio with added noise
        """
        if snr_db is None:
            snr_db = np.random.uniform(*config.AUGMENT_NOISE_SNR_RANGE)
        
        # Calculate noise power based on signal power and desired SNR
        signal_power = np.mean(audio ** 2)
        noise_power = signal_power / (10 ** (snr_db / 10))
        
        # Generate and add noise
        noise = np.random.normal(0, np.sqrt(noise_power), len(audio))
        noisy_audio = audio + noise
        
        return noisy_audio
    
    def augment_volume(self, audio: np.ndarray, gain_db: Optional[float] = None) -> np.ndarray:
        """
        Apply volume scaling augmentation
        
        Args:
            audio: Audio signal
            gain_db: Gain in dB (±20 dB)
            
        Returns:
            Volume-adjusted audio
        """
        if gain_db is None:
            gain_db = np.random.uniform(-20, 20)
        
        gain_linear = 10 ** (gain_db / 20)
        return audio * gain_linear
    
    def apply_augmentations(self, audio: np.ndarray, 
                          time_stretch: bool = True,
                          pitch_shift: bool = False,  # Careful with pitch shift for note classification
                          add_noise: bool = True,
                          volume_change: bool = True) -> np.ndarray:
        """
        Apply random augmentations to audio
        
        Args:
            audio: Audio signal
            time_stretch: Whether to apply time stretching
            pitch_shift: Whether to apply pitch shifting (use carefully)
            add_noise: Whether to add noise
            volume_change: Whether to change volume
            
        Returns:
            Augmented audio
        """
        augmented = audio.copy()
        
        if time_stretch and np.random.random() < 0.5:
            augmented = self.augment_time_stretch(augmented)
        
        if pitch_shift and np.random.random() < 0.3:
            # Use with caution for note classification
            augmented = self.augment_pitch_shift(augmented)
        
        if add_noise and np.random.random() < 0.5:
            augmented = self.augment_add_noise(augmented)
        
        if volume_change and np.random.random() < 0.5:
            augmented = self.augment_volume(augmented)
        
        return augmented


def extract_features_batch(file_paths: list, processor: AudioProcessor, 
                          augment: bool = False) -> np.ndarray:
    """
    Extract features from multiple audio files
    
    Args:
        file_paths: List of audio file paths
        processor: AudioProcessor instance
        augment: Whether to apply augmentations
        
    Returns:
        Batch of preprocessed spectrograms
    """
    features = []
    
    for file_path in file_paths:
        try:
            audio = processor.load_audio(file_path)
            
            if augment:
                audio = processor.apply_augmentations(audio, pitch_shift=False)
            
            mel_spec = processor.extract_mel_spectrogram(audio)
            mel_spec_norm = processor.normalize_spectrogram(mel_spec)
            mel_spec_norm = np.expand_dims(mel_spec_norm, axis=-1)
            
            features.append(mel_spec_norm)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue
    
    return np.array(features)


if __name__ == "__main__":
    # Test the audio processor
    processor = AudioProcessor()
    print("AudioProcessor initialized successfully!")
    print(f"Sample rate: {processor.sample_rate} Hz")
    print(f"Duration: {processor.duration} seconds")
    print(f"Mel bands: {processor.n_mels}")
    print(f"Expected input shape for model: (batch_size, {processor.n_mels}, time_steps, 1)")


