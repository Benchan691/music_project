# Environment Setup Guide

## ✅ Installation Complete!

Your Python environment has been successfully configured with all dependencies.

## Environment Details

- **Environment Name**: `music_project`
- **Python Version**: 3.10.18
- **TensorFlow Version**: 2.15.0 (macOS optimized)
- **GPU Acceleration**: tensorflow-metal enabled

## How to Use

### Activate the Environment

Every time you work on this project, activate the conda environment first:

```bash
conda activate music_project
```

### Run Your Applications

Once activated, you can run any of the project scripts:

```bash
# Train the model
python train.py

# Run web application
python app.py

# Make predictions
python predict.py audio_file.wav

# Evaluate model
python evaluate.py

# Open Jupyter notebook
jupyter notebook
```

### Deactivate When Done

```bash
conda deactivate
```

## Verification

Check that everything is working:

```bash
conda activate music_project
python -c "import tensorflow as tf; print('TensorFlow:', tf.__version__)"
```

Expected output: `TensorFlow: 2.15.0`

## Troubleshooting

### If you see "command not found: conda"
```bash
# Initialize conda for your shell
conda init zsh
# Restart your terminal
```

### If environment activation fails
```bash
# Recreate the environment
conda env remove -n music_project
conda create -n music_project python=3.10 -y
conda activate music_project
pip install -r requirements.txt
```

### To see all conda environments
```bash
conda env list
```

## Dependencies Installed

All packages from `requirements.txt` are installed with compatible versions:
- ✅ TensorFlow 2.15.0 (macOS optimized)
- ✅ NumPy 1.24.3
- ✅ Librosa 0.10.1
- ✅ Scikit-learn 1.3.2
- ✅ Pandas 2.1.4
- ✅ Matplotlib 3.8.2
- ✅ Flask 3.0.0
- ✅ Jupyter 1.0.0
- ✅ And all other dependencies

## Next Steps

1. **Prepare your data**: `python prepare_data.py setup`
2. **Train your model**: `python train.py`
3. **Test predictions**: `python predict.py your_audio.wav`
4. **Launch web app**: `python app.py` (visit http://localhost:5000)

---

**Note**: Always remember to `conda activate music_project` before working on this project!

