# 🎵 Start Collecting Training Data!

Your beautiful data collection interface is ready!

## Quick Start (3 Steps)

### 1. Install Dependencies (if not done yet)
```bash
pip install -r requirements.txt
```

### 2. Start the Data Collection Server
```bash
python data_collection_app.py
```

### 3. Open in Browser
Navigate to: **http://localhost:5001**

## What You'll See

A beautiful web interface with:

### 📊 **Top Statistics Bar**
- Real-time count of all your samples
- Individual counts for each instrument
- Updates automatically as you collect

### 📁 **Audio Input Panel (Left)**
Two ways to add audio:
- **📤 Upload File Tab**: Drag-drop or click to upload existing audio files
- **🎤 Record Live Tab**: Click the microphone button to record directly

### 🏷️ **Labels Panel (Right)**
- **Instrument Dropdown**: Piano, Violin, or Shepherd's Flute
- **Note Grid**: Visual grid with all 36 notes (C3-B5)
- **Progress Bar**: Shows your progress for current selection
- **Submit Button**: Save your labeled sample

### 📊 **What's Needed (Bottom)**
- Lists top 20 combinations that need more samples
- Shows current count vs target (100 per combination)
- Helps you prioritize what to record next

## Recording Workflow

### For Upload:
1. Select "Upload File" tab
2. Drag-drop your audio file
3. Choose instrument
4. Click the note
5. Click "Submit Sample"
6. 🎉 See success message!

### For Live Recording:
1. Select "Record Live" tab
2. Click big microphone button
3. Play your note (2-5 seconds)
4. Click stop button
5. Choose instrument and note
6. Click "Submit Sample"
7. 🎉 See success message!

## Features You'll Love

✨ **Smart File Naming**
- Automatic naming: `NOTE_COUNT_TIMESTAMP.wav`
- Example: `A4_023_20251021_143022.wav`
- No conflicts, easy to find

📊 **Real-time Progress**
- See how many samples you've collected
- Track progress per instrument-note combination
- Know exactly what you still need

🎯 **Priority List**
- "What's Needed" section shows what to record next
- Sorted by most needed
- Reach your target of 100 samples per combination

💾 **One-Click Organization**
- Click "Move All to Dataset" when done
- Automatically splits into train/val/test (70/15/15)
- Ready for training immediately

## Recording Tips

### Quality Matters!
- **Quiet space**: Minimal background noise
- **Good mic position**: 6-12 inches away
- **Clear notes**: Sustain for 2-5 seconds
- **Consistent volume**: Medium playing level

### Add Variety!
For each note, record with:
- Different dynamics (soft, medium, loud)
- Different articulations
- Slightly different mic positions
- Different playing techniques

### Stay Organized
- One instrument at a time
- Complete one octave before moving on
- Take breaks to maintain quality
- Use "What's Needed" list as guide

## Recommended Targets

### Minimum (For Testing)
- **50 samples** per combination
- **Total: 5,400 samples**
- Training time: ~1 week

### Recommended (Good Quality)
- **100 samples** per combination
- **Total: 10,800 samples**
- Training time: ~2-3 weeks
- **This is what the interface tracks!**

### Optimal (Best Quality)
- **150-200 samples** per combination
- **Total: 16,200-21,600 samples**
- Training time: ~3-4 weeks

## When You're Done Collecting

1. **Click "Move All to Dataset"**
   - Splits files into train/val/test
   - Moves to proper directories
   - Resets counter

2. **Generate Metadata**
   ```bash
   python prepare_data.py metadata
   ```

3. **Start Training**
   ```bash
   python train.py
   ```

4. **Wait 2-8 hours** (depending on data size)

5. **Deploy Your Model!**
   ```bash
   python app.py
   ```

## Sample Recording Schedule

### Week 1: Piano
- **Days 1-2**: C3-B3 (12 notes × 100 samples)
- **Days 3-4**: C4-B4 (12 notes × 100 samples)
- **Days 5-6**: C5-B5 (12 notes × 100 samples)
- **Day 7**: Fill gaps, add variety

### Week 2: Violin
- Same schedule as piano

### Week 3: Shepherd's Flute
- Same schedule as piano

### Week 4: Polish & Train
- Review "What's Needed"
- Fill remaining gaps
- Add more variety to under-represented notes
- Move to dataset and start training!

## Storage Space

You'll need:
- **During collection**: ~2-5 GB (temporary)
- **Final dataset**: ~2-5 GB (organized)
- **Total**: ~10 GB free space recommended

## Troubleshooting

### Can't hear recording
- Check system audio settings
- Check browser permissions
- Try different browser (Chrome works best)

### Submit button disabled
- Must select ALL THREE: audio + instrument + note
- Audio must be uploaded or recorded first

### Stats not updating
- Auto-refreshes every 30 seconds
- Or refresh browser page manually

### File upload fails
- Check file size (max 10MB)
- Check format (WAV, MP3, OGG, FLAC)
- Check internet connection

## Need Help?

📖 **Full Documentation**: See `DATA_COLLECTION_GUIDE.md`

💡 **Quick Tips**:
- Start with piano (easiest to record)
- Record in batches (all C notes, all D notes, etc.)
- Take breaks to maintain quality
- Quality > Quantity!

---

## Ready? Let's Go! 🚀

```bash
python data_collection_app.py
```

Then open: **http://localhost:5001**

Happy collecting! Your AI model will thank you! 🎵


