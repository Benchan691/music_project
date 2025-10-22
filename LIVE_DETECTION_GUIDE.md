# Live Audio Detection Guide

## 🎤 Real-Time Instrument and Note Recognition

The live detection feature allows you to continuously record and get instant predictions of what instrument and note you're playing!

## Features

### ✨ Continuous Recording
- Click once to start, click again to stop
- No need to upload files - just play!
- Automatic audio chunking for analysis

### 📊 Real-Time Display
- **Large visual display** of current instrument and note
- **Confidence bars** showing prediction certainty
- **Live audio visualization** with wave bars
- **Detection history** showing last 10 results

### 📈 Statistics Tracking
- Total number of detections
- Average confidence score
- Detection rate (per minute)
- All updated in real-time!

## How to Use

### Step 1: Start the Server
```bash
python app.py
```

### Step 2: Open Live Detection
Navigate to: **http://localhost:5000/live**

Or click the "Try Live Detection Mode" button from the main page.

### Step 3: Start Recording
1. **Click the big microphone button** (🎤)
2. **Allow microphone access** when prompted
3. **Start playing** your instrument
4. **Watch results appear** in real-time!

### Step 4: Stop Recording
Click the button again (now showing ⏹️) to stop

## Interface Overview

### Main Display (Top)
```
┌─────────────────────────────────┐
│         🎹                       │  ← Instrument (emoji + name)
│      95% confident               │  ← Confidence score
│      ▓▓▓▓▓▓▓▓▓▓░░░░░            │  ← Visual bar
└─────────────────────────────────┘

┌─────────────────────────────────┐
│         A4                       │  ← Note name
│      88% confident               │  ← Confidence score
│      ▓▓▓▓▓▓▓▓░░░░░░░            │  ← Visual bar
└─────────────────────────────────┘
```

### Statistics (Middle)
```
┌───────┬───────────┬────────────┐
│   15  │    92%    │    7.5     │
│ Detect│  Avg Conf │ Rate/min   │
└───────┴───────────┴────────────┘
```

### Audio Visualization
```
▂▃▅▆▃▂▁▂▃▅▇▅▃▂▁▂▃▅▆▃  ← Live wave bars
```

### Detection History (Bottom)
```
Recent Detections:
┌────────────────────────────────┐
│ piano - A4          14:23:45   │
│ violin - C5         14:23:42   │
│ piano - G4          14:23:39   │
└────────────────────────────────┘
```

## Settings

### Detection Interval
Adjust how often audio is analyzed:
- **1000ms (1 sec)**: Very fast, more detections
- **2000ms (2 sec)**: Default, balanced
- **3000ms (3 sec)**: Slower, more accurate
- **5000ms (5 sec)**: Slowest, most stable

**Tip**: Shorter intervals = faster updates but more processing

## Technical Details

### How It Works

1. **Continuous Recording**
   - Browser captures audio from microphone
   - Audio is split into chunks (based on interval)

2. **Chunk Processing**
   - Each chunk sent to server
   - Preprocessed to mel spectrogram
   - Fed through AI model

3. **Result Display**
   - Predictions returned via API
   - UI updates instantly
   - History tracked locally

4. **Loop**
   - Process repeats until stopped
   - New chunk recorded immediately after previous

### Performance

- **Latency**: ~0.5-2 seconds per prediction
  - Depends on: audio length, server speed, model complexity
  
- **Accuracy**: Same as batch mode
  - Real-time doesn't sacrifice quality
  
- **Resource Usage**: Moderate
  - CPU: Light (browser handles recording)
  - Network: Light (small audio chunks)
  - Server: Medium (model inference)

## Tips for Best Results

### Recording Quality
✅ **Good:**
- Use in quiet environment
- Speak/play clearly
- Maintain consistent volume
- Stay near microphone (6-12 inches)

❌ **Avoid:**
- Background noise/music
- Multiple instruments at once
- Too quiet or too loud
- Rapid changes mid-chunk

### Optimal Settings
- **For practice**: 2-3 second intervals
- **For performance**: 1-2 second intervals
- **For accuracy**: 3-5 second intervals

### Understanding Results

**High Confidence (>80%)**
- Model is very sure
- Clear, sustained note
- Familiar instrument

**Medium Confidence (50-80%)**
- Model is somewhat sure
- May be between notes
- Multiple possibilities

**Low Confidence (<50%)**
- Model is uncertain
- Noisy audio
- Unusual sound
- Consider playing more clearly

## Use Cases

### 🎓 Learning & Practice
- See what notes you're actually playing
- Check intonation in real-time
- Practice sight-reading
- Verify technique

### 🎸 Performance
- Monitor your playing live
- Identify problem areas
- Analyze improvisation
- Study your patterns

### 🎼 Composition
- Capture ideas quickly
- Identify notes in your head
- Experiment with sounds
- Document your process

### 🔬 Research
- Analyze playing patterns
- Study instrument characteristics
- Collect performance data
- Compare different players

## Keyboard Shortcuts

Currently none, but you can add them! The interface is designed to be extended.

## Browser Compatibility

### ✅ Fully Supported
- **Chrome/Edge** (Recommended)
- **Firefox**
- **Safari** (macOS/iOS)

### ⚠️ Limitations
- **Mobile**: May have higher latency
- **Safari**: Some recording quirks
- **IE**: Not supported

## Troubleshooting

### Microphone Not Working
1. **Check permissions**: Allow microphone access
2. **Check device**: Ensure microphone connected
3. **Check browser**: Use Chrome for best results
4. **Reload page**: Sometimes fixes initialization

### No Predictions Appearing
1. **Check model**: Ensure model is trained and loaded
2. **Check console**: Look for JavaScript errors (F12)
3. **Check network**: Ensure server is running
4. **Check audio**: Make sound loud enough

### Slow/Laggy Predictions
1. **Increase interval**: Try 3-5 seconds
2. **Check server**: May be CPU-limited
3. **Close other apps**: Free up resources
4. **Use GPU**: If available for model

### Incorrect Predictions
1. **Play more clearly**: Sustained, clear notes
2. **Reduce noise**: Quieter environment
3. **Check training**: Model needs good data
4. **Adjust position**: Move closer/farther from mic

## Advanced Usage

### Custom Intervals
Modify the interval input to any value between 1000-5000ms. Experiment to find what works best for your use case!

### Integration
The `/api/predict-stream` endpoint can be used by other applications:

```javascript
// Send audio chunk
const formData = new FormData();
formData.append('file', audioBlob, 'recording.wav');

fetch('/api/predict-stream', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => {
    console.log('Instrument:', data.instrument);
    console.log('Note:', data.note);
    console.log('Confidences:', 
        data.instrument_confidence,
        data.note_confidence
    );
});
```

### Extending the Interface
The code is clean and modular. You can easily:
- Add more visualizations
- Save detection logs
- Export statistics
- Add keyboard shortcuts
- Customize styling
- Add filters/effects

## Comparison: Live vs Upload Mode

| Feature | Live Detection | Upload Mode |
|---------|---------------|-------------|
| **Speed** | Real-time | On-demand |
| **Convenience** | Very high | Medium |
| **Accuracy** | Same | Same |
| **Use Case** | Practice, performance | Analysis, testing |
| **File Needed** | No | Yes |
| **History** | Last 10 | Single result |
| **Continuous** | Yes | No |

## API Endpoint

### POST `/api/predict-stream`

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: audio file (WAV format)

**Response:**
```json
{
  "success": true,
  "instrument": "piano",
  "instrument_confidence": 0.95,
  "note": "A4",
  "note_confidence": 0.88,
  "timestamp": "2025-10-21T14:23:45.123"
}
```

**Error Response:**
```json
{
  "error": "Error message here"
}
```

## Performance Metrics

With a trained model:
- **Processing Time**: ~200-500ms per chunk
- **Network Latency**: ~50-100ms
- **Total Latency**: ~0.5-1 second
- **Detections/Minute**: 30-60 (depends on interval)

## Security Notes

⚠️ **Privacy**: Audio is processed on the server
- Temporary files are deleted immediately
- No audio is stored permanently
- Use on trusted networks only

## Future Enhancements

Planned features:
- [ ] Save detection sessions
- [ ] Export statistics to CSV
- [ ] Record and playback sessions
- [ ] Multi-instrument detection
- [ ] MIDI output support
- [ ] Mobile app version

---

## Quick Start Summary

1. **Start server**: `python app.py`
2. **Open browser**: http://localhost:5000/live
3. **Click mic button**: Start recording
4. **Play instrument**: See real-time results!
5. **Click again**: Stop when done

**That's it!** 🎵 Enjoy real-time audio detection!


