# Data Collection Interface Guide

## Overview

This interface makes it easy to collect and organize training data for your audio classifier. You can either upload existing audio files or record live directly in your browser!

## Features

✨ **Two Input Methods**
- 📤 Upload audio files (WAV, MP3, OGG, FLAC)
- 🎤 Record live audio directly in browser

🏷️ **Easy Labeling**
- Select instrument from dropdown
- Click notes from visual grid (C3-B5)
- Automatic filename generation

📊 **Real-time Statistics**
- Total samples collected
- Per-instrument counts
- Progress tracking for each combination
- See what you need to record next

📦 **Auto-Organization**
- Files saved with proper naming: `NOTE_COUNT_TIMESTAMP.ext`
- Automatic train/val/test splitting (70/15/15)
- One-click move to dataset

## Quick Start

### 1. Start the Data Collection Server

```bash
python data_collection_app.py
```

The server will start on **http://localhost:5001**

### 2. Open in Browser

Navigate to: http://localhost:5001

You'll see a beautiful interface with:
- Real-time statistics at the top
- Audio input panel (upload or record)
- Labels panel (instrument and note selection)
- What's needed list at the bottom

## How to Use

### Option A: Upload Audio Files

1. **Select "Upload File" tab**
2. **Click or drag-drop** your audio file
3. **Select instrument** from dropdown (Piano, Violin, or Shepherd's Flute)
4. **Click a note** from the grid (C3 through B5)
5. **Click "Submit Sample"**
6. **See confirmation** with updated stats

### Option B: Record Live

1. **Select "Record Live" tab**
2. **Click the microphone button** to start recording
3. **Play your instrument** (2-5 seconds recommended)
4. **Click stop button** (square icon)
5. **Select instrument** from dropdown
6. **Click a note** from the grid
7. **Click "Submit Sample"**
8. **See confirmation** with updated stats

## Understanding the Interface

### Top Statistics Bar
- **Total Samples**: All samples collected
- **Piano Samples**: Piano-only count
- **Violin Samples**: Violin-only count
- **Shepherd's Flute**: Flute-only count

### Progress Bar
Shows your progress toward the target (100 samples) for the currently selected instrument-note combination.

### What You Need to Record
Lists the top 20 combinations that need the most samples. Use this to prioritize your recording sessions!

## Moving to Dataset

Once you've collected samples, click **"Move All to Dataset"** to:
- Split samples into train/val/test (70/15/15)
- Move files to proper directories
- Reset collection counter

After moving, you can continue collecting more samples.

## Tips for Best Results

### Recording Quality
- **Quiet environment**: Minimize background noise
- **Good distance**: 6-12 inches from microphone
- **Clear sound**: Play clearly and sustain notes
- **Consistent volume**: Moderate playing level

### Sample Duration
- **Ideal**: 2-5 seconds per sample
- **Minimum**: 1 second
- **Maximum**: 10 seconds (but 2-5 is better)

### Variety (Important!)
Record multiple versions of each note with:
- Different volumes (soft, medium, loud)
- Different articulations
- Different starting times
- Different microphone positions (slightly)

### Organization
- **One session**: Focus on one instrument at a time
- **Complete octaves**: Record all 12 notes in an octave before moving on
- **Track progress**: Use the "What's Needed" list to guide you

## File Naming Convention

Files are automatically named as:
```
NOTE_COUNT_TIMESTAMP.extension
```

Examples:
- `C4_001_20251021_143022.wav`
- `A3_045_20251021_144530.mp3`

This ensures:
- Easy identification of note
- No filename conflicts
- Chronological ordering
- Proper organization

## Keyboard Shortcuts

Currently none, but you can add them! Feel free to modify the code.

## Recommended Recording Schedule

### Day 1-2: Piano
- Record all 36 notes
- 50-100 samples per note
- Vary dynamics and touch

### Day 3-4: Violin
- Record all 36 notes
- 50-100 samples per note
- Vary bow pressure and vibrato

### Day 5-7: Shepherd's Flute
- Record all 36 notes (or available range)
- 50-100 samples per note
- Vary breath pressure and articulation

### Day 8+: Fill Gaps
- Use "What's Needed" list
- Focus on under-represented combinations
- Add more variety to existing samples

## Target Numbers

### Minimum Viable
- **50 samples** per instrument-note combination
- **Total**: 5,400 samples minimum

### Recommended
- **100 samples** per instrument-note combination
- **Total**: 10,800 samples

### Optimal
- **150-200 samples** per combination
- **Total**: 16,200-21,600 samples

## Storage Requirements

- **Per sample**: ~200KB - 500KB (2-5 seconds)
- **Total for 10,800 samples**: ~2-5 GB
- **Collection folder**: Temporary (cleaned after moving to dataset)
- **Final dataset**: ~2-5 GB (plus augmented versions during training)

## API Endpoints

The data collection server provides these endpoints:

### GET `/api/stats`
Returns current collection statistics

### POST `/api/submit`
Submit a labeled audio sample
- Form data: file, instrument, note, source

### POST `/api/move-to-dataset`
Move all collected samples to train/val/test splits

### GET `/api/needed-samples`
Get list of combinations that need more samples

## Troubleshooting

### Microphone Not Working
- **Check permissions**: Allow microphone access in browser
- **Check device**: Ensure microphone is connected
- **Try different browser**: Chrome/Edge work best

### Upload Fails
- **Check file size**: Max 10MB
- **Check format**: WAV, MP3, OGG, or FLAC only
- **Check file name**: No special characters

### Submit Button Disabled
- **Check all fields**: Must select instrument, note, AND provide audio
- **Audio file**: Must be uploaded or recorded first

### Stats Not Updating
- **Refresh page**: Stats auto-refresh every 30 seconds
- **Check console**: Look for JavaScript errors (F12)

### Can't Record Long Samples
- Browser limitation: Record in chunks if needed
- Or upload pre-recorded files instead

## Advanced Usage

### Batch Upload Script

If you have many existing files, create a batch upload script:

```python
import os
import requests

def upload_batch(directory, instrument, note):
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'rb') as f:
                files = {'file': f}
                data = {
                    'instrument': instrument,
                    'note': note,
                    'source': 'upload'
                }
                response = requests.post(
                    'http://localhost:5001/api/submit',
                    files=files,
                    data=data
                )
                print(f"Uploaded {filename}: {response.json()}")

# Usage
upload_batch('my_piano_c4_samples/', 'piano', 'C4')
```

### Custom Note Range

Edit `data_collection_app.py` to modify the note range if your instruments can't play all notes.

### Multiple People Recording

Each person can run their own instance:
- Person 1: Port 5001
- Person 2: Port 5002
- Person 3: Port 5003

Just change the port in `data_collection_app.py`

## After Collection

Once you've collected enough samples:

1. **Click "Move All to Dataset"**
2. **Verify files** in `data/train/`, `data/validation/`, `data/test/`
3. **Create metadata**: `python prepare_data.py metadata`
4. **Start training**: `python train.py`

## Security Notes

⚠️ **This is a local development tool**
- Only use on localhost
- Don't expose to internet without authentication
- Files are saved to disk without encryption

## Customization

Feel free to modify:
- **Colors/Style**: Edit CSS in `templates/data_collection.html`
- **Target numbers**: Change 100 to your desired target
- **Note range**: Modify notes array in JavaScript
- **File formats**: Add more in `config.ALLOWED_EXTENSIONS`

## Support

If you encounter issues:
1. Check browser console (F12) for errors
2. Check terminal for server errors
3. Verify microphone permissions
4. Try different browser (Chrome recommended)

---

Happy collecting! 🎵 Remember: **Quality over quantity!** Better to have 50 excellent samples than 200 poor ones.


