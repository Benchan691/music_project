"""
Standalone prediction script for inference on audio files
"""

import os
import sys
import numpy as np
import tensorflow as tf

import config
from audio_processor import AudioProcessor


def load_model_and_processor():
    """Load trained model and audio processor"""
    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {config.MODEL_PATH}. Please train the model first.")
    
    print("Loading model...")
    model = tf.keras.models.load_model(config.MODEL_PATH)
    processor = AudioProcessor()
    print("Model loaded successfully!\n")
    
    return model, processor


def predict_audio(audio_path, model, processor, top_k=3):
    """
    Predict instrument and note for an audio file
    
    Args:
        audio_path: Path to audio file
        model: Trained Keras model
        processor: AudioProcessor instance
        top_k: Number of top predictions to return
        
    Returns:
        Dictionary with predictions
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    print(f"Processing: {audio_path}")
    
    # Preprocess audio
    features = processor.process_audio_file(audio_path)
    features = np.expand_dims(features, axis=0)  # Add batch dimension
    
    # Make prediction
    instrument_pred, note_pred = model.predict(features, verbose=0)
    
    # Get top predictions
    instrument_top_k = np.argsort(instrument_pred[0])[::-1][:top_k]
    note_top_k = np.argsort(note_pred[0])[::-1][:top_k]
    
    # Format results
    results = {
        'file': os.path.basename(audio_path),
        'instrument': {
            'prediction': config.INSTRUMENTS[instrument_top_k[0]],
            'confidence': float(instrument_pred[0][instrument_top_k[0]]),
            'top_predictions': [
                {
                    'instrument': config.INSTRUMENTS[idx],
                    'confidence': float(instrument_pred[0][idx])
                }
                for idx in instrument_top_k
            ]
        },
        'note': {
            'prediction': config.NOTES[note_top_k[0]],
            'confidence': float(note_pred[0][note_top_k[0]]),
            'midi_note': config.NOTE_TO_MIDI[config.NOTES[note_top_k[0]]],
            'top_predictions': [
                {
                    'note': config.NOTES[idx],
                    'confidence': float(note_pred[0][idx]),
                    'midi': config.NOTE_TO_MIDI[config.NOTES[idx]]
                }
                for idx in note_top_k
            ]
        }
    }
    
    return results


def print_results(results):
    """Pretty print prediction results"""
    print("\n" + "=" * 70)
    print("PREDICTION RESULTS")
    print("=" * 70)
    
    print(f"\nFile: {results['file']}")
    
    print("\n--- INSTRUMENT ---")
    print(f"Prediction: {results['instrument']['prediction'].upper()}")
    print(f"Confidence: {results['instrument']['confidence']:.2%}")
    
    if len(results['instrument']['top_predictions']) > 1:
        print("\nTop predictions:")
        for i, pred in enumerate(results['instrument']['top_predictions'], 1):
            print(f"  {i}. {pred['instrument'].upper()}: {pred['confidence']:.2%}")
    
    print("\n--- NOTE ---")
    print(f"Prediction: {results['note']['prediction']}")
    print(f"MIDI Note: {results['note']['midi_note']}")
    print(f"Confidence: {results['note']['confidence']:.2%}")
    
    if len(results['note']['top_predictions']) > 1:
        print("\nTop predictions:")
        for i, pred in enumerate(results['note']['top_predictions'], 1):
            print(f"  {i}. {pred['note']} (MIDI {pred['midi']}): {pred['confidence']:.2%}")
    
    print("\n" + "=" * 70 + "\n")


def predict_batch(audio_files, model, processor):
    """Predict for multiple audio files"""
    results = []
    
    for audio_file in audio_files:
        try:
            result = predict_audio(audio_file, model, processor)
            results.append(result)
            print_results(result)
        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}\n")
    
    return results


def interactive_mode(model, processor):
    """Interactive prediction mode"""
    print("\n" + "=" * 70)
    print("INTERACTIVE PREDICTION MODE")
    print("=" * 70)
    print("\nEnter audio file path to classify (or 'quit' to exit)")
    
    while True:
        audio_path = input("\nAudio file: ").strip()
        
        if audio_path.lower() in ['quit', 'exit', 'q']:
            print("Exiting...")
            break
        
        if not audio_path:
            continue
        
        try:
            result = predict_audio(audio_path, model, processor)
            print_results(result)
        except Exception as e:
            print(f"Error: {str(e)}")


def main():
    """Main prediction interface"""
    print("\n" + "=" * 70)
    print("AUDIO INSTRUMENT AND NOTE CLASSIFIER - PREDICTION")
    print("=" * 70 + "\n")
    
    # Load model
    try:
        model, processor = load_model_and_processor()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    
    # Check command line arguments
    if len(sys.argv) > 1:
        # Batch mode: predict for all provided files
        audio_files = sys.argv[1:]
        predict_batch(audio_files, model, processor)
    else:
        # Interactive mode
        interactive_mode(model, processor)


if __name__ == "__main__":
    main()


