"""
Configuration file for the audio instrument and note classifier
"""

# Audio processing parameters
SAMPLE_RATE = 22050
DURATION = 2.0  # seconds
N_MELS = 128
HOP_LENGTH = 512
N_FFT = 2048
TRIM_SILENCE = True  # Automatically trim silence from beginning/end
SILENCE_THRESHOLD_DB = 20  # Threshold in dB for silence detection (higher = more aggressive)

# Model parameters
INSTRUMENTS = ['piano', 'violin', 'shepherds_flute']
NUM_INSTRUMENTS = len(INSTRUMENTS)

# Notes from C3 to B5 (3 octaves, chromatic scale)
NOTES = [
    'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3',
    'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4',
    'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5'
]
NUM_NOTES = len(NOTES)

# Note name to MIDI number mapping
NOTE_TO_MIDI = {note: 48 + i for i, note in enumerate(NOTES)}  # C3 is MIDI 48

# Training parameters
BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.15
TEST_SPLIT = 0.15

# Data augmentation parameters
AUGMENT_TIME_STRETCH_RANGE = (0.9, 1.1)  # ±10%
AUGMENT_PITCH_SHIFT_RANGE = (-2, 2)  # ±2 semitones
AUGMENT_NOISE_SNR_RANGE = (20, 40)  # dB

# File paths
DATA_DIR = 'data'
TRAIN_DIR = f'{DATA_DIR}/train'
VAL_DIR = f'{DATA_DIR}/validation'
TEST_DIR = f'{DATA_DIR}/test'
MODEL_DIR = 'models'
MODEL_PATH = f'{MODEL_DIR}/audio_classifier_model.h5'
HISTORY_PATH = f'{MODEL_DIR}/training_history.json'

# Web app settings
UPLOAD_FOLDER = 'uploads'
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac'}


