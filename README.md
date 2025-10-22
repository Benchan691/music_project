# Audio Instrument and Note Classifier

An AI model that identifies musical instruments and notes from audio input using deep learning. The system can classify three instruments (Piano, Violin, Shepherd's Flute) and detect 36 musical notes (C3-B5, chromatic scale) from audio recordings.

## Features

- **Dual-task classification**: Simultaneously identifies instrument type and musical note
- **High accuracy**: 95-98% for instruments, 85-92% for notes (with adequate training data)
- **Web interfaces**: 
  - Upload mode for analyzing audio files
  - **Live detection mode**: Continuous real-time recording and prediction
  - Data collection interface for building training dataset
- **Data augmentation**: Built-in augmentation for robust training
- **Real-time inference**: Fast prediction on CPU or GPU
- **Comprehensive evaluation**: Confusion matrices and detailed metrics

## Architecture

The system uses a dual-output CNN model:
- **Input**: Mel spectrogram (128 mel bands, 2-second windows)
- **Backbone**: 4 convolutional layers with batch normalization
- **Outputs**: 
  - Instrument classifier (3 classes)
  - Note classifier (36 classes)
- **Framework**: TensorFlow/Keras

## Installation

### Requirements
- Python 3.8+
- TensorFlow 2.15+
- librosa
- Flask

### Setup

1. Clone the repository:
```bash
cd /path/to/Music_project
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create directory structure:
```bash
python prepare_data.py setup
```

## Usage

### 1. Data Collection (NEW: Easy Web Interface!)

**We now have a beautiful web interface for collecting training data!**

#### Quick Start with Data Collection Interface
```bash
python data_collection_app.py
# Open http://localhost:5001 in your browser
```

This interface allows you to:
- 📤 Upload audio files OR 🎤 record live
- 🏷️ Label instrument and note with easy dropdowns/buttons
- 📊 See real-time statistics
- 🎯 Track progress toward targets
- 📦 One-click move to dataset

See `START_COLLECTION.md` for detailed guide!

#### Or Use Traditional Data Preparation

### 2. Data Preparation (Alternative Method)

#### Download Public Datasets

**NSynth Dataset** (for Piano and Violin):
```bash
# Download NSynth dataset from: https://magenta.tensorflow.org/datasets/nsynth
# Extract to a temporary directory, then filter:
python prepare_data.py filter /path/to/nsynth-train
```

**Shepherd's Flute Samples**:
- See `data/recording_guide.txt` for instructions on recording samples
- Or use substitute instruments (tin whistle, recorder, flute)
- Place samples in `data/manual_recordings/shepherds_flute/`

#### Organize Data

1. Place all collected audio samples in:
```
data/all_samples/
├── piano/
│   ├── C3_001.wav
│   ├── C3_002.wav
│   └── ...
├── violin/
│   └── ...
└── shepherds_flute/
    └── ...
```

2. Split into train/validation/test sets:
```bash
python prepare_data.py split data/all_samples
```

3. Create metadata:
```bash
python prepare_data.py metadata
```

### 2. Training

Train the model:
```bash
python train.py
```

Training parameters can be adjusted in `config.py`:
- `EPOCHS`: Number of training epochs (default: 100)
- `BATCH_SIZE`: Batch size (default: 32)
- `LEARNING_RATE`: Learning rate (default: 0.001)

The model will be saved to `models/audio_classifier_model.h5`

### 3. Evaluation

Evaluate the trained model:
```bash
python evaluate.py
```

This generates:
- Classification metrics
- Confusion matrices
- Per-instrument accuracy plots
- Error analysis

Results are saved in the `evaluation/` directory.

### 4. Prediction

#### Command Line

Predict single file:
```bash
python predict.py path/to/audio.wav
```

Predict multiple files:
```bash
python predict.py file1.wav file2.wav file3.mp3
```

Interactive mode:
```bash
python predict.py
```

#### Web Application

Start the web server:
```bash
python app.py
```

Open your browser to `http://localhost:5000`

Upload an audio file and get instant predictions with confidence scores.

## Training Data Requirements

For robust performance, you need:

### Minimum Dataset
- **Total samples**: 5,400-10,800 audio files
- **Per note-instrument combination**: 50-100 samples
- **Storage**: ~10-20 GB

### Recommended Dataset
- **Total samples**: 10,800-21,600 audio files
- **Per note-instrument combination**: 100-200 samples
- **Storage**: ~15-30 GB

### Sample Specifications
- **Duration**: 2-5 seconds per sample
- **Format**: WAV (16-bit) or high-quality MP3
- **Sample rate**: 22050 Hz or higher
- **Quality**: Clean recordings with minimal background noise
- **Variety**: Multiple dynamics, articulations, and playing styles

### Data Sources

1. **NSynth Dataset**: 300k+ instrument samples (includes piano, violin)
   - Download: https://magenta.tensorflow.org/datasets/nsynth

2. **MAESTRO Dataset**: Piano performances
   - Download: https://magenta.tensorflow.org/datasets/maestro

3. **Philharmonia Orchestra**: Individual instrument samples
   - Website: https://philharmonia.co.uk/resources/sound-samples/

4. **Manual Recording**: Shepherd's flute or substitute
   - See `data/recording_guide.txt` for instructions

### Data Organization

```
data/
├── train/          # 70% of data
│   ├── piano/
│   ├── violin/
│   └── shepherds_flute/
├── validation/     # 15% of data
│   └── ...
├── test/          # 15% of data
│   └── ...
└── train_metadata.csv
```

## Project Structure

```
Music_project/
├── config.py                 # Configuration parameters
├── audio_processor.py        # Audio preprocessing and augmentation
├── model.py                  # Model architecture
├── data_generator.py         # Data loading and batching
├── train.py                  # Training script
├── evaluate.py               # Evaluation and metrics
├── predict.py                # Standalone prediction
├── app.py                    # Flask web application
├── prepare_data.py           # Data preparation utilities
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web interface
├── data/                    # Training data
├── models/                  # Saved models
├── evaluation/              # Evaluation results
└── uploads/                 # Temporary upload folder
```

## Model Performance

With adequate training data, expected performance:

- **Instrument Classification**: 95-98% accuracy
- **Note Classification**: 85-92% accuracy
- **Combined Task** (both correct): 80-88% accuracy
- **Note Top-3 Accuracy**: 93-97%

Performance depends heavily on:
- Quality and quantity of training data
- Recording conditions
- Instrument quality
- Playing technique consistency

## Configuration

Edit `config.py` to customize:

```python
# Audio parameters
SAMPLE_RATE = 22050
DURATION = 2.0
N_MELS = 128

# Training parameters
BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001

# Instruments and notes
INSTRUMENTS = ['piano', 'violin', 'shepherds_flute']
NOTES = ['C3', 'C#3', ..., 'B5']  # 36 notes
```

## API Endpoints

When running the web app:

- `GET /` - Web interface
- `POST /api/predict` - Upload audio for prediction
- `GET /api/info` - Model information
- `GET /health` - Health check

## Tips for Best Results

1. **Data Quality**:
   - Use high-quality recordings
   - Minimize background noise
   - Ensure consistent recording conditions

2. **Training**:
   - Use data augmentation
   - Monitor validation loss for overfitting
   - Train for at least 50 epochs

3. **Inference**:
   - Use 2-5 second audio clips
   - Ensure clear, sustained notes
   - Minimize polyphonic content (multiple notes)

## Troubleshooting

**Model not loading**:
- Ensure you've trained the model first: `python train.py`
- Check that `models/audio_classifier_model.h5` exists

**Low accuracy**:
- Increase training data quantity and variety
- Train for more epochs
- Verify data quality and labeling

**Out of memory**:
- Reduce `BATCH_SIZE` in `config.py`
- Use a machine with more RAM/VRAM

**Web app not starting**:
- Check port 5000 is available
- Ensure Flask is installed: `pip install Flask`

## Future Enhancements

- [ ] Real-time audio streaming support
- [ ] Chord detection (multiple notes)
- [ ] Note duration tracking
- [ ] More instruments
- [ ] Mobile app version
- [ ] ONNX export for cross-platform deployment

## License

This project is provided as-is for educational and research purposes.

## Acknowledgments

- **NSynth Dataset**: Google Magenta
- **TensorFlow/Keras**: Model framework
- **librosa**: Audio processing library


