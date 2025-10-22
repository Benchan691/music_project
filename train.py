"""
Training script for the audio instrument and note classifier
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import tensorflow as tf
from sklearn.model_selection import train_test_split

import config
from model import create_cnn_model, compile_model, get_callbacks
from data_generator import create_data_generators, AudioDataGenerator


def train_model(train_dir=config.TRAIN_DIR, val_dir=config.VAL_DIR,
                model_path=config.MODEL_PATH, epochs=config.EPOCHS,
                batch_size=config.BATCH_SIZE, use_transfer_learning=False):
    """
    Train the audio classification model
    
    Args:
        train_dir: Directory containing training data
        val_dir: Directory containing validation data
        model_path: Path to save trained model
        epochs: Number of training epochs
        batch_size: Batch size
        use_transfer_learning: Whether to use transfer learning model
    """
    print("=" * 70)
    print("AUDIO INSTRUMENT AND NOTE CLASSIFIER - TRAINING")
    print("=" * 70)
    
    # Create model directory if it doesn't exist
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    
    # Create data generators
    print("\nLoading data generators...")
    train_generator, val_generator = create_data_generators(
        train_dir=train_dir,
        val_dir=val_dir,
        batch_size=batch_size
    )
    
    print(f"Training samples: {len(train_generator.file_paths)}")
    print(f"Validation samples: {len(val_generator.file_paths)}")
    
    # Get input shape from first batch
    print("\nLoading sample batch to determine input shape...")
    sample_X, _ = train_generator[0]
    input_shape = sample_X.shape[1:]
    print(f"Input shape: {input_shape}")
    
    # Create model
    print("\nCreating model...")
    if use_transfer_learning:
        from model import create_transfer_learning_model
        model = create_transfer_learning_model(input_shape)
        print("Using transfer learning architecture")
    else:
        model = create_cnn_model(input_shape)
        print("Using custom CNN architecture")
    
    # Compile model
    model = compile_model(model, learning_rate=config.LEARNING_RATE)
    
    print("\nModel Summary:")
    model.summary()
    
    # Get callbacks
    callbacks = get_callbacks(model_path=model_path, patience=10)
    
    # Train model
    print("\n" + "=" * 70)
    print("STARTING TRAINING")
    print("=" * 70)
    
    start_time = datetime.now()
    
    history = model.fit(
        train_generator,
        validation_data=val_generator,
        epochs=epochs,
        callbacks=callbacks,
        verbose=1
    )
    
    end_time = datetime.now()
    training_duration = end_time - start_time
    
    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)
    print(f"Training duration: {training_duration}")
    print(f"Model saved to: {model_path}")
    
    # Save training history
    history_dict = {key: [float(val) for val in values] 
                   for key, values in history.history.items()}
    history_path = config.HISTORY_PATH
    
    with open(history_path, 'w') as f:
        json.dump(history_dict, f, indent=2)
    print(f"Training history saved to: {history_path}")
    
    # Plot training history
    plot_training_history(history, save_path=f"{config.MODEL_DIR}/training_history.png")
    
    return model, history


def plot_training_history(history, save_path=None):
    """
    Plot training history
    
    Args:
        history: Training history object
        save_path: Path to save plot
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Instrument accuracy
    axes[0, 0].plot(history.history['instrument_output_accuracy'], label='Train')
    axes[0, 0].plot(history.history['val_instrument_output_accuracy'], label='Validation')
    axes[0, 0].set_title('Instrument Classification Accuracy')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True)
    
    # Note accuracy
    axes[0, 1].plot(history.history['note_output_accuracy'], label='Train')
    axes[0, 1].plot(history.history['val_note_output_accuracy'], label='Validation')
    axes[0, 1].set_title('Note Classification Accuracy')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Accuracy')
    axes[0, 1].legend()
    axes[0, 1].grid(True)
    
    # Instrument loss
    axes[1, 0].plot(history.history['instrument_output_loss'], label='Train')
    axes[1, 0].plot(history.history['val_instrument_output_loss'], label='Validation')
    axes[1, 0].set_title('Instrument Classification Loss')
    axes[1, 0].set_xlabel('Epoch')
    axes[1, 0].set_ylabel('Loss')
    axes[1, 0].legend()
    axes[1, 0].grid(True)
    
    # Note loss
    axes[1, 1].plot(history.history['note_output_loss'], label='Train')
    axes[1, 1].plot(history.history['val_note_output_loss'], label='Validation')
    axes[1, 1].set_title('Note Classification Loss')
    axes[1, 1].set_xlabel('Epoch')
    axes[1, 1].set_ylabel('Loss')
    axes[1, 1].legend()
    axes[1, 1].grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Training plots saved to: {save_path}")
    
    plt.close()


if __name__ == "__main__":
    # Check if training data exists
    if not os.path.exists(config.TRAIN_DIR):
        print(f"Error: Training directory not found: {config.TRAIN_DIR}")
        print("\nPlease organize your data in the following structure:")
        print(f"  {config.TRAIN_DIR}/")
        print(f"    piano/")
        print(f"      C3_001.wav")
        print(f"      C3_002.wav")
        print(f"      ...")
        print(f"    violin/")
        print(f"    shepherds_flute/")
        print("\nYou can use the data preparation scripts to download and organize data.")
    else:
        # Train model
        model, history = train_model(
            train_dir=config.TRAIN_DIR,
            val_dir=config.VAL_DIR,
            model_path=config.MODEL_PATH,
            epochs=config.EPOCHS,
            batch_size=config.BATCH_SIZE
        )


