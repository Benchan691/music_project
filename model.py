"""
Model architecture for instrument and note classification
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import config


def create_cnn_model(input_shape, num_instruments=config.NUM_INSTRUMENTS, 
                     num_notes=config.NUM_NOTES):
    """
    Create a dual-output CNN model for instrument and note classification
    
    Args:
        input_shape: Shape of input mel spectrogram (n_mels, time_steps, 1)
        num_instruments: Number of instrument classes
        num_notes: Number of note classes
        
    Returns:
        Keras model with two outputs: instrument and note predictions
    """
    # Input layer
    inputs = layers.Input(shape=input_shape, name='mel_spectrogram_input')
    
    # Convolutional backbone
    x = layers.Conv2D(32, (3, 3), activation='relu', padding='same', name='conv1')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name='pool1')(x)
    x = layers.Dropout(0.25)(x)
    
    x = layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv2')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name='pool2')(x)
    x = layers.Dropout(0.25)(x)
    
    x = layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='conv3')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name='pool3')(x)
    x = layers.Dropout(0.25)(x)
    
    x = layers.Conv2D(256, (3, 3), activation='relu', padding='same', name='conv4')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D((2, 2), name='pool4')(x)
    x = layers.Dropout(0.25)(x)
    
    # Flatten for dense layers
    x = layers.Flatten(name='flatten')(x)
    
    # Shared dense layer
    x = layers.Dense(512, activation='relu', name='dense_shared')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    
    # Instrument classification head
    instrument_branch = layers.Dense(256, activation='relu', name='instrument_dense')(x)
    instrument_branch = layers.Dropout(0.3)(instrument_branch)
    instrument_output = layers.Dense(num_instruments, activation='softmax', 
                                    name='instrument_output')(instrument_branch)
    
    # Note classification head
    note_branch = layers.Dense(256, activation='relu', name='note_dense')(x)
    note_branch = layers.Dropout(0.3)(note_branch)
    note_output = layers.Dense(num_notes, activation='softmax', 
                              name='note_output')(note_branch)
    
    # Create model
    model = models.Model(
        inputs=inputs,
        outputs=[instrument_output, note_output],
        name='audio_instrument_note_classifier'
    )
    
    return model


def create_transfer_learning_model(input_shape, num_instruments=config.NUM_INSTRUMENTS,
                                   num_notes=config.NUM_NOTES):
    """
    Create a model using transfer learning with MobileNetV2 as backbone
    (Alternative approach for potentially better performance)
    
    Args:
        input_shape: Shape of input mel spectrogram (n_mels, time_steps, 1)
        num_instruments: Number of instrument classes
        num_notes: Number of note classes
        
    Returns:
        Keras model with two outputs
    """
    inputs = layers.Input(shape=input_shape, name='mel_spectrogram_input')
    
    # Convert single channel to 3 channels for MobileNetV2
    x = layers.Conv2D(3, (1, 1), padding='same')(inputs)
    
    # Use MobileNetV2 as feature extractor
    base_model = keras.applications.MobileNetV2(
        input_shape=(*input_shape[:2], 3),
        include_top=False,
        weights=None  # Train from scratch or use 'imagenet' if you want pretrained
    )
    base_model.trainable = True  # Allow fine-tuning
    
    x = base_model(x, training=True)
    
    # Global pooling
    x = layers.GlobalAveragePooling2D()(x)
    
    # Shared dense layer
    x = layers.Dense(512, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    
    # Instrument classification head
    instrument_branch = layers.Dense(256, activation='relu')(x)
    instrument_branch = layers.Dropout(0.3)(instrument_branch)
    instrument_output = layers.Dense(num_instruments, activation='softmax',
                                    name='instrument_output')(instrument_branch)
    
    # Note classification head
    note_branch = layers.Dense(256, activation='relu')(x)
    note_branch = layers.Dropout(0.3)(note_branch)
    note_output = layers.Dense(num_notes, activation='softmax',
                              name='note_output')(note_branch)
    
    model = models.Model(
        inputs=inputs,
        outputs=[instrument_output, note_output],
        name='audio_transfer_learning_classifier'
    )
    
    return model


def compile_model(model, learning_rate=config.LEARNING_RATE, 
                 instrument_weight=1.0, note_weight=1.0):
    """
    Compile the model with optimizer, loss functions, and metrics
    
    Args:
        model: Keras model
        learning_rate: Learning rate for optimizer
        instrument_weight: Weight for instrument loss
        note_weight: Weight for note loss
        
    Returns:
        Compiled model
    """
    optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
    
    # Define losses and metrics for each output
    model.compile(
        optimizer=optimizer,
        loss={
            'instrument_output': 'categorical_crossentropy',
            'note_output': 'categorical_crossentropy'
        },
        loss_weights={
            'instrument_output': instrument_weight,
            'note_output': note_weight
        },
        metrics={
            'instrument_output': ['accuracy', keras.metrics.TopKCategoricalAccuracy(k=2, name='top_2_accuracy')],
            'note_output': ['accuracy', keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
        }
    )
    
    return model


def get_callbacks(model_path=config.MODEL_PATH, patience=10):
    """
    Create training callbacks for model checkpointing and early stopping
    
    Args:
        model_path: Path to save best model
        patience: Number of epochs to wait before early stopping
        
    Returns:
        List of callbacks
    """
    callbacks = [
        # Save best model
        keras.callbacks.ModelCheckpoint(
            model_path,
            monitor='val_loss',
            save_best_only=True,
            mode='min',
            verbose=1
        ),
        
        # Early stopping
        keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=patience,
            mode='min',
            restore_best_weights=True,
            verbose=1
        ),
        
        # Learning rate reduction
        keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            mode='min',
            verbose=1
        ),
        
        # TensorBoard logging
        keras.callbacks.TensorBoard(
            log_dir='./logs',
            histogram_freq=1,
            write_graph=True
        )
    ]
    
    return callbacks


if __name__ == "__main__":
    # Test model creation
    print("Testing model creation...")
    
    # Dummy input shape (will be determined by actual mel spectrogram size)
    input_shape = (128, 87, 1)  # (n_mels, time_steps, channels)
    
    # Create model
    model = create_cnn_model(input_shape)
    
    # Compile model
    model = compile_model(model)
    
    # Print model summary
    print("\nModel Summary:")
    model.summary()
    
    print(f"\nTotal parameters: {model.count_params():,}")
    print(f"Number of instrument classes: {config.NUM_INSTRUMENTS}")
    print(f"Number of note classes: {config.NUM_NOTES}")
    
    # Test with dummy input
    import numpy as np
    dummy_input = np.random.rand(1, *input_shape)
    instrument_pred, note_pred = model.predict(dummy_input, verbose=0)
    
    print(f"\nTest prediction shapes:")
    print(f"Instrument prediction: {instrument_pred.shape}")
    print(f"Note prediction: {note_pred.shape}")
    print("\nModel created successfully!")


