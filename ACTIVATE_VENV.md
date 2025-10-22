# Virtual Environment Activation Guide

## ✅ Setup Complete!

Your Python virtual environment has been created and all dependencies are installed.

## 🚀 How to Use the Virtual Environment

**IMPORTANT:** Every time you open a new terminal window, you need to activate the virtual environment before running any Python scripts.

### Activate the Virtual Environment

```bash
cd /Users/chankokpan/Documents/Music_project
source venv/bin/activate
```

You'll see `(venv)` appear in your terminal prompt, indicating the virtual environment is active.

### Run Your Scripts

Once activated, you can run any project script:

```bash
# Test setup
python test_setup.py

# Prepare data
python prepare_data.py setup

# Train model
python train.py

# Run web app
python app.py
```

### Deactivate (When Done)

To exit the virtual environment:

```bash
deactivate
```

## 📦 Installed Packages

- ✅ TensorFlow 2.20.0 (with Apple Silicon support)
- ✅ Pandas 2.3.3
- ✅ Librosa 0.11.0
- ✅ Flask 3.1.2
- ✅ scikit-learn 1.7.2
- ✅ And all other dependencies

## 🎯 Next Steps

1. **Download NSynth Dataset:**
   - Visit: https://magenta.tensorflow.org/datasets/nsynth
   - Download and extract the dataset

2. **Filter NSynth Data:**
   ```bash
   source venv/bin/activate
   python prepare_data.py filter /path/to/nsynth-train
   ```

3. **Split Data:**
   ```bash
   python prepare_data.py split data/nsynth_filtered
   python prepare_data.py metadata
   ```

4. **Train Your Model:**
   ```bash
   python train.py
   ```

5. **Run the Web App:**
   ```bash
   python app.py
   ```

## 💡 Pro Tip

Add this to your `.zshrc` or `.bashrc` to create a shortcut:

```bash
alias music-ai="cd /Users/chankokpan/Documents/Music_project && source venv/bin/activate"
```

Then you can just type `music-ai` in any terminal to activate!

## ⚠️ Important Notes

- The `venv/` directory contains all your packages (don't delete it!)
- The virtual environment is local to this project
- You can safely add `venv/` to `.gitignore` (it's project-specific)
- If you need to install more packages, activate venv first, then use `pip install`

## 🆘 Troubleshooting

**If packages are missing:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**If virtual environment is corrupted:**
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Happy coding! 🎵


