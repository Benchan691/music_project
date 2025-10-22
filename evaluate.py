"""
Model evaluation script with confusion matrices and metrics
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf

import config
from data_generator import AudioDataGenerator


def evaluate_model(model_path=config.MODEL_PATH, test_dir=config.TEST_DIR):
    """
    Evaluate the trained model on test data
    
    Args:
        model_path: Path to trained model
        test_dir: Directory containing test data
    """
    print("=" * 70)
    print("MODEL EVALUATION")
    print("=" * 70)
    
    # Load model
    print("\nLoading model...")
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully!")
    
    # Create test data generator
    print("\nLoading test data...")
    test_generator = AudioDataGenerator(
        test_dir,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        augment=False
    )
    
    print(f"Test samples: {len(test_generator.file_paths)}")
    
    # Make predictions
    print("\nMaking predictions...")
    all_instrument_preds = []
    all_note_preds = []
    all_instrument_true = []
    all_note_true = []
    
    for i in range(len(test_generator)):
        X, y = test_generator[i]
        
        # Predict
        instrument_pred, note_pred = model.predict(X, verbose=0)
        
        # Store predictions and true labels
        all_instrument_preds.extend(np.argmax(instrument_pred, axis=1))
        all_note_preds.extend(np.argmax(note_pred, axis=1))
        all_instrument_true.extend(np.argmax(y['instrument_output'], axis=1))
        all_note_true.extend(np.argmax(y['note_output'], axis=1))
    
    all_instrument_preds = np.array(all_instrument_preds)
    all_note_preds = np.array(all_note_preds)
    all_instrument_true = np.array(all_instrument_true)
    all_note_true = np.array(all_note_true)
    
    # Calculate metrics
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    
    # Instrument classification metrics
    print("\n--- INSTRUMENT CLASSIFICATION ---")
    instrument_accuracy = accuracy_score(all_instrument_true, all_instrument_preds)
    print(f"Accuracy: {instrument_accuracy:.4f} ({instrument_accuracy*100:.2f}%)")
    
    print("\nClassification Report:")
    print(classification_report(all_instrument_true, all_instrument_preds,
                               target_names=config.INSTRUMENTS))
    
    # Note classification metrics
    print("\n--- NOTE CLASSIFICATION ---")
    note_accuracy = accuracy_score(all_note_true, all_note_preds)
    print(f"Accuracy: {note_accuracy:.4f} ({note_accuracy*100:.2f}%)")
    
    # Top-3 accuracy for notes
    correct_top3 = 0
    for i in range(len(test_generator)):
        X, y = test_generator[i]
        _, note_pred = model.predict(X, verbose=0)
        
        true_labels = np.argmax(y['note_output'], axis=1)
        top3_preds = np.argsort(note_pred, axis=1)[:, -3:]
        
        for j, true_label in enumerate(true_labels):
            if true_label in top3_preds[j]:
                correct_top3 += 1
    
    top3_accuracy = correct_top3 / len(all_note_true)
    print(f"Top-3 Accuracy: {top3_accuracy:.4f} ({top3_accuracy*100:.2f}%)")
    
    # Combined accuracy (both correct)
    combined_correct = np.sum((all_instrument_preds == all_instrument_true) & 
                             (all_note_preds == all_note_true))
    combined_accuracy = combined_correct / len(all_instrument_true)
    print(f"\n--- COMBINED TASK ---")
    print(f"Both Correct: {combined_accuracy:.4f} ({combined_accuracy*100:.2f}%)")
    
    # Create visualizations
    print("\nGenerating visualizations...")
    os.makedirs('evaluation', exist_ok=True)
    
    # Instrument confusion matrix
    plot_confusion_matrix(
        all_instrument_true, all_instrument_preds,
        config.INSTRUMENTS,
        title='Instrument Classification Confusion Matrix',
        save_path='evaluation/instrument_confusion_matrix.png'
    )
    
    # Note confusion matrix
    plot_confusion_matrix(
        all_note_true, all_note_preds,
        config.NOTES,
        title='Note Classification Confusion Matrix',
        save_path='evaluation/note_confusion_matrix.png',
        figsize=(20, 18)
    )
    
    # Per-instrument note accuracy
    plot_per_instrument_accuracy(
        all_instrument_true, all_note_true, all_note_preds,
        save_path='evaluation/per_instrument_accuracy.png'
    )
    
    print("\nEvaluation complete! Results saved to 'evaluation/' directory.")
    
    return {
        'instrument_accuracy': instrument_accuracy,
        'note_accuracy': note_accuracy,
        'note_top3_accuracy': top3_accuracy,
        'combined_accuracy': combined_accuracy
    }


def plot_confusion_matrix(y_true, y_pred, labels, title, save_path, figsize=(10, 8)):
    """Plot and save confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    
    # Normalize
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    plt.figure(figsize=figsize)
    sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues',
                xticklabels=labels, yticklabels=labels, cbar_kws={'label': 'Accuracy'})
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  Saved: {save_path}")


def plot_per_instrument_accuracy(instrument_true, note_true, note_pred, save_path):
    """Plot note accuracy for each instrument"""
    accuracies = []
    
    for i, instrument in enumerate(config.INSTRUMENTS):
        mask = instrument_true == i
        if np.sum(mask) > 0:
            accuracy = accuracy_score(note_true[mask], note_pred[mask])
            accuracies.append(accuracy)
        else:
            accuracies.append(0)
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(config.INSTRUMENTS, accuracies, color=['#667eea', '#764ba2', '#f093fb'])
    plt.title('Note Classification Accuracy by Instrument')
    plt.ylabel('Accuracy')
    plt.xlabel('Instrument')
    plt.ylim(0, 1)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  Saved: {save_path}")


def analyze_errors(model_path=config.MODEL_PATH, test_dir=config.TEST_DIR, num_errors=10):
    """
    Analyze misclassified samples
    
    Args:
        model_path: Path to trained model
        test_dir: Directory containing test data
        num_errors: Number of errors to display
    """
    print("\nAnalyzing errors...")
    
    model = tf.keras.models.load_model(model_path)
    test_generator = AudioDataGenerator(test_dir, batch_size=1, shuffle=False, augment=False)
    
    errors = []
    
    for i in range(len(test_generator)):
        X, y = test_generator[i]
        instrument_pred, note_pred = model.predict(X, verbose=0)
        
        instrument_true = np.argmax(y['instrument_output'][0])
        note_true = np.argmax(y['note_output'][0])
        instrument_pred_idx = np.argmax(instrument_pred[0])
        note_pred_idx = np.argmax(note_pred[0])
        
        if instrument_pred_idx != instrument_true or note_pred_idx != note_true:
            errors.append({
                'file': test_generator.file_paths[i],
                'true_instrument': config.INSTRUMENTS[instrument_true],
                'pred_instrument': config.INSTRUMENTS[instrument_pred_idx],
                'true_note': config.NOTES[note_true],
                'pred_note': config.NOTES[note_pred_idx],
                'instrument_conf': instrument_pred[0][instrument_pred_idx],
                'note_conf': note_pred[0][note_pred_idx]
            })
    
    print(f"\nTotal errors: {len(errors)} out of {len(test_generator)} ({len(errors)/len(test_generator)*100:.1f}%)")
    print(f"\nShowing first {min(num_errors, len(errors))} errors:")
    
    for i, error in enumerate(errors[:num_errors]):
        print(f"\n{i+1}. {os.path.basename(error['file'])}")
        print(f"   True: {error['true_instrument']} - {error['true_note']}")
        print(f"   Pred: {error['pred_instrument']} ({error['instrument_conf']:.2%}) - "
              f"{error['pred_note']} ({error['note_conf']:.2%})")


if __name__ == "__main__":
    # Check if model exists
    if not os.path.exists(config.MODEL_PATH):
        print(f"Error: Model not found at {config.MODEL_PATH}")
        print("Please train the model first using train.py")
    elif not os.path.exists(config.TEST_DIR):
        print(f"Error: Test directory not found at {config.TEST_DIR}")
        print("Please prepare test data first using prepare_data.py")
    else:
        # Evaluate model
        metrics = evaluate_model()
        
        # Analyze errors
        analyze_errors(num_errors=10)


