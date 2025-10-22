"""
Flask web application for collecting training data
Allows uploading audio files or recording live with labeling
"""

import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import shutil

import config

app = Flask(__name__)
CORS(app)

# Configuration
COLLECTION_FOLDER = 'data/collection_temp'
app.config['COLLECTION_FOLDER'] = COLLECTION_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_UPLOAD_SIZE

# Create folders
os.makedirs(COLLECTION_FOLDER, exist_ok=True)

# Stats file
STATS_FILE = 'data/collection_stats.json'


def load_stats():
    """Load collection statistics"""
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {
        'total_samples': 0,
        'by_instrument': {inst: 0 for inst in config.INSTRUMENTS},
        'by_note': {note: 0 for note in config.NOTES},
        'by_combination': {}
    }


def save_stats(stats):
    """Save collection statistics"""
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=2)


def update_stats(instrument, note):
    """Update statistics after adding a sample"""
    stats = load_stats()
    stats['total_samples'] += 1
    stats['by_instrument'][instrument] += 1
    stats['by_note'][note] += 1
    
    combo_key = f"{instrument}_{note}"
    if combo_key not in stats['by_combination']:
        stats['by_combination'][combo_key] = 0
    stats['by_combination'][combo_key] += 1
    
    save_stats(stats)
    return stats


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render data collection page"""
    return render_template('data_collection.html')


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get current collection statistics"""
    stats = load_stats()
    return jsonify(stats)


@app.route('/api/submit', methods=['POST'])
def submit_sample():
    """
    Handle audio sample submission with labels
    
    Expected form data:
    - file: audio file (required)
    - instrument: instrument name (required)
    - note: note name (required)
    - source: 'upload' or 'recording' (optional)
    """
    try:
        # Validate required fields
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        if 'instrument' not in request.form or 'note' not in request.form:
            return jsonify({'error': 'Missing instrument or note label'}), 400
        
        file = request.files['file']
        instrument = request.form['instrument']
        note = request.form['note']
        source = request.form.get('source', 'upload')
        
        # Validate
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if instrument not in config.INSTRUMENTS:
            return jsonify({'error': f'Invalid instrument: {instrument}'}), 400
        
        if note not in config.NOTES:
            return jsonify({'error': f'Invalid note: {note}'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Create instrument directory
        instrument_dir = os.path.join(app.config['COLLECTION_FOLDER'], instrument)
        os.makedirs(instrument_dir, exist_ok=True)
        
        # Count existing files for this combination
        existing_files = [f for f in os.listdir(instrument_dir) 
                         if f.startswith(f"{note}_")]
        count = len(existing_files) + 1
        
        # Generate filename
        ext = file.filename.rsplit('.', 1)[1].lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{note}_{count:03d}_{timestamp}.{ext}"
        filepath = os.path.join(instrument_dir, filename)
        
        # Save file
        file.save(filepath)
        
        # Update statistics
        stats = update_stats(instrument, note)
        
        # Return success with updated stats
        return jsonify({
            'success': True,
            'message': f'Successfully saved: {filename}',
            'filename': filename,
            'instrument': instrument,
            'note': note,
            'count_for_combination': stats['by_combination'].get(f"{instrument}_{note}", 0),
            'total_samples': stats['total_samples'],
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/move-to-dataset', methods=['POST'])
def move_to_dataset():
    """
    Move collected samples to train/val/test splits
    """
    try:
        from sklearn.model_selection import train_test_split
        
        # Get all files from collection folder
        all_files = []
        for instrument in config.INSTRUMENTS:
            instrument_dir = os.path.join(app.config['COLLECTION_FOLDER'], instrument)
            if os.path.exists(instrument_dir):
                for filename in os.listdir(instrument_dir):
                    if allowed_file(filename):
                        all_files.append({
                            'instrument': instrument,
                            'filename': filename,
                            'path': os.path.join(instrument_dir, filename)
                        })
        
        if not all_files:
            return jsonify({'error': 'No files to move'}), 400
        
        # Split by instrument to maintain balance
        moved_count = {'train': 0, 'val': 0, 'test': 0}
        
        for instrument in config.INSTRUMENTS:
            inst_files = [f for f in all_files if f['instrument'] == instrument]
            
            if len(inst_files) < 3:
                # Too few files, put all in training
                for file_info in inst_files:
                    dest_dir = os.path.join(config.TRAIN_DIR, instrument)
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, file_info['filename'])
                    shutil.move(file_info['path'], dest_path)
                    moved_count['train'] += 1
            else:
                # Split 70/15/15
                train_files, temp_files = train_test_split(inst_files, train_size=0.70, random_state=42)
                val_files, test_files = train_test_split(temp_files, train_size=0.5, random_state=42)
                
                # Move files
                for files, split_name, split_dir in [
                    (train_files, 'train', config.TRAIN_DIR),
                    (val_files, 'val', config.VAL_DIR),
                    (test_files, 'test', config.TEST_DIR)
                ]:
                    dest_dir = os.path.join(split_dir, instrument)
                    os.makedirs(dest_dir, exist_ok=True)
                    
                    for file_info in files:
                        dest_path = os.path.join(dest_dir, file_info['filename'])
                        shutil.move(file_info['path'], dest_path)
                        moved_count[split_name] += 1
        
        # Clear stats
        save_stats({
            'total_samples': 0,
            'by_instrument': {inst: 0 for inst in config.INSTRUMENTS},
            'by_note': {note: 0 for note in config.NOTES},
            'by_combination': {}
        })
        
        return jsonify({
            'success': True,
            'message': f"Moved {sum(moved_count.values())} files to dataset",
            'moved_count': moved_count
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/needed-samples', methods=['GET'])
def needed_samples():
    """Get information about how many more samples are needed"""
    stats = load_stats()
    
    target_per_combination = 100  # Recommended target
    
    needs = []
    for instrument in config.INSTRUMENTS:
        for note in config.NOTES:
            combo_key = f"{instrument}_{note}"
            current = stats['by_combination'].get(combo_key, 0)
            if current < target_per_combination:
                needs.append({
                    'instrument': instrument,
                    'note': note,
                    'current': current,
                    'target': target_per_combination,
                    'needed': target_per_combination - current
                })
    
    # Sort by most needed
    needs.sort(key=lambda x: x['needed'], reverse=True)
    
    return jsonify({
        'total_collected': stats['total_samples'],
        'target_total': len(config.INSTRUMENTS) * len(config.NOTES) * target_per_combination,
        'needs': needs[:20]  # Top 20 most needed
    })


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("AUDIO CLASSIFIER - DATA COLLECTION INTERFACE")
    print("=" * 70)
    print(f"\nServer starting on http://localhost:5001")
    print("Upload or record audio samples and label them for training!\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)


