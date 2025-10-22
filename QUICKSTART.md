# Quick Start Guide

Get your audio classifier up and running in 5 steps!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- TensorFlow 2.15
- librosa (audio processing)
- Flask (web app)
- Other required packages

## Step 2: Test Your Setup

```bash
python test_setup.py
```

This verifies all packages are installed correctly and the code can run.

## Step 3: Prepare Training Data

### Option A: Use NSynth Dataset (Recommended)

1. Download NSynth dataset:
   - Visit: https://magenta.tensorflow.org/datasets/nsynth
   - Download `nsynth-train.jsonwav.tar.gz` (~30GB)
   - Extract to a temporary directory

2. Filter and organize:
   ```bash
   python prepare_data.py filter /path/to/nsynth-train
   python prepare_data.py split data/nsynth_filtered
   python prepare_data.py metadata
   ```

### Option B: Use Your Own Recordings

1. Create the recording guide:
   ```bash
   python prepare_data.py setup
   ```

2. Follow instructions in `data/recording_guide.txt`

3. Organize files as:
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

4. Split data:
   ```bash
   python prepare_data.py split data/all_samples
   python prepare_data.py metadata
   ```

## Step 4: Train the Model

```bash
python train.py
```

This will:
- Load training data from `data/train/`
- Train for 100 epochs (adjust in `config.py`)
- Save best model to `models/audio_classifier_model.h5`
- Generate training plots

Expected time: 2-8 hours depending on data size and hardware

## Step 5: Use Your Model

### Option A: Web Application

```bash
python app.py
```

Then open: http://localhost:5000

Upload an audio file and get instant predictions!

### Option B: Command Line

```bash
python predict.py path/to/audio.wav
```

Or interactive mode:
```bash
python predict.py
```

## Optional: Evaluate Model

```bash
python evaluate.py
```

This generates:
- Accuracy metrics
- Confusion matrices
- Error analysis
- Results saved to `evaluation/`

## Troubleshooting

### "Model not found" error
- You need to train the model first: `python train.py`

### "No training data" error
- Complete Step 3 to prepare training data
- Verify files exist in `data/train/piano/`, `data/train/violin/`, etc.

### Out of memory
- Reduce `BATCH_SIZE` in `config.py` (default: 32)
- Try: 16, 8, or 4

### Low accuracy
- Collect more training data (aim for 100+ samples per note-instrument)
- Train for more epochs
- Verify data quality and labeling

### Port 5000 already in use
- Kill existing process: `lsof -ti:5000 | xargs kill -9`
- Or change port in `app.py`

## Project Structure

```
Music_project/
├── config.py              # Configuration
├── audio_processor.py     # Audio preprocessing
├── model.py              # Model architecture
├── train.py              # Training script
├── predict.py            # Prediction script
├── app.py                # Web application
├── evaluate.py           # Evaluation script
├── prepare_data.py       # Data preparation
├── test_setup.py         # Setup verification
├── requirements.txt      # Dependencies
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
├── data/                 # Training data
├── models/               # Saved models
├── templates/            # Web UI
├── uploads/              # Temp uploads
└── evaluation/           # Results
```

## Data Requirements Summary

**Minimum viable dataset:**
- 5,400-10,800 total samples
- 50-100 samples per note-instrument combination
- ~10-20 GB storage

**Recommended dataset:**
- 10,800-21,600 total samples
- 100-200 samples per note-instrument combination
- ~15-30 GB storage

**Sample specifications:**
- Duration: 2-5 seconds
- Format: WAV (16-bit) or high-quality MP3
- Sample rate: 22050 Hz or higher
- Quality: Clean, minimal background noise

## Next Steps

After training your model:

1. **Improve accuracy**: Collect more diverse training data
2. **Deploy**: Containerize with Docker for production
3. **Extend**: Add more instruments or note ranges
4. **Optimize**: Export to ONNX or TensorFlow Lite for mobile

## Need Help?

- Check the full README.md for detailed documentation
- Review training logs in `logs/` directory
- Examine `evaluation/` for model performance insights

Happy classifying! 🎵


