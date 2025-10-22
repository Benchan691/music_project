"""
Flask web application for audio instrument and note classification
"""

import os
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import tensorflow as tf

import config
from audio_processor import AudioProcessor

app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_UPLOAD_SIZE

# Create upload folder if it doesn't exist
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

# Global variables for model and processor
model = None
processor = None


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def load_model():
    """Load the trained model"""
    global model, processor
    
    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {config.MODEL_PATH}. Please train the model first.")
    
    print("Loading model...")
    model = tf.keras.models.load_model(config.MODEL_PATH)
    processor = AudioProcessor()
    print("Model loaded successfully!")


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/live')
def live():
    """Render live detection page"""
    return render_template('live_detection.html')


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Endpoint for audio classification
    
    Expected: audio file in 'file' field of multipart/form-data
    Returns: JSON with instrument, note, and confidence scores
    """
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'Invalid file type. Allowed types: {", ".join(config.ALLOWED_EXTENSIONS)}'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess audio
        features = processor.process_audio_file(filepath)
        features = np.expand_dims(features, axis=0)  # Add batch dimension
        
        # Make prediction
        instrument_pred, note_pred = model.predict(features, verbose=0)
        
        # Get top predictions
        instrument_idx = np.argmax(instrument_pred[0])
        note_idx = np.argmax(note_pred[0])
        
        instrument_confidence = float(instrument_pred[0][instrument_idx])
        note_confidence = float(note_pred[0][note_idx])
        
        instrument_name = config.INSTRUMENTS[instrument_idx]
        note_name = config.NOTES[note_idx]
        
        # Get top 3 predictions for each
        top_instruments = []
        for idx in np.argsort(instrument_pred[0])[::-1][:3]:
            top_instruments.append({
                'instrument': config.INSTRUMENTS[idx],
                'confidence': float(instrument_pred[0][idx])
            })
        
        top_notes = []
        for idx in np.argsort(note_pred[0])[::-1][:5]:
            top_notes.append({
                'note': config.NOTES[idx],
                'confidence': float(note_pred[0][idx])
            })
        
        # Clean up uploaded file
        os.remove(filepath)
        
        # Return results
        result = {
            'success': True,
            'instrument': instrument_name,
            'instrument_confidence': instrument_confidence,
            'note': note_name,
            'note_confidence': note_confidence,
            'top_instruments': top_instruments,
            'top_notes': top_notes
        }
        
        return jsonify(result)
    
    except Exception as e:
        # Clean up file if it exists
        if os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({'error': str(e)}), 500


@app.route('/api/info', methods=['GET'])
def info():
    """Get information about the model"""
    return jsonify({
        'instruments': config.INSTRUMENTS,
        'notes': config.NOTES,
        'num_instruments': config.NUM_INSTRUMENTS,
        'num_notes': config.NUM_NOTES,
        'model_loaded': model is not None
    })


@app.route('/api/predict-stream', methods=['POST'])
def predict_stream():
    """
    Endpoint for streaming predictions (continuous recording)
    Optimized for faster response
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save temporarily
        filename = secure_filename(f"stream_{datetime.now().timestamp()}.wav")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Preprocess audio
        features = processor.process_audio_file(filepath)
        features = np.expand_dims(features, axis=0)
        
        # Make prediction
        instrument_pred, note_pred = model.predict(features, verbose=0)
        
        # Get top predictions
        instrument_idx = np.argmax(instrument_pred[0])
        note_idx = np.argmax(note_pred[0])
        
        instrument_confidence = float(instrument_pred[0][instrument_idx])
        note_confidence = float(note_pred[0][note_idx])
        
        instrument_name = config.INSTRUMENTS[instrument_idx]
        note_name = config.NOTES[note_idx]
        
        # Clean up
        os.remove(filepath)
        
        # Return simplified result for speed
        result = {
            'success': True,
            'instrument': instrument_name,
            'instrument_confidence': instrument_confidence,
            'note': note_name,
            'note_confidence': note_confidence,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(result)
    
    except Exception as e:
        # Clean up file if it exists
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })


if __name__ == '__main__':
    # Load model on startup
    try:
        load_model()
    except FileNotFoundError as e:
        print(f"Warning: {e}")
        print("Server will start but predictions will not work until model is trained.")
    
    # Run app
    print("\n" + "=" * 70)
    print("AUDIO INSTRUMENT AND NOTE CLASSIFIER - WEB APP")
    print("=" * 70)
    print(f"\nServer starting on http://localhost:5001")
    print("Upload an audio file to get instrument and note predictions!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)


