"""
Test script to verify installation and setup
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing package imports...\n")
    
    packages = [
        ('tensorflow', 'TensorFlow'),
        ('librosa', 'librosa'),
        ('numpy', 'NumPy'),
        ('matplotlib', 'Matplotlib'),
        ('flask', 'Flask'),
        ('sklearn', 'scikit-learn'),
        ('pandas', 'pandas'),
        ('seaborn', 'seaborn'),
    ]
    
    all_passed = True
    
    for package, name in packages:
        try:
            __import__(package)
            print(f"✓ {name} - OK")
        except ImportError as e:
            print(f"✗ {name} - MISSING")
            all_passed = False
    
    return all_passed


def test_config():
    """Test if config file loads correctly"""
    print("\n\nTesting configuration...\n")
    
    try:
        import config
        print(f"✓ Config loaded")
        print(f"  - Instruments: {config.INSTRUMENTS}")
        print(f"  - Number of notes: {config.NUM_NOTES}")
        print(f"  - Sample rate: {config.SAMPLE_RATE} Hz")
        print(f"  - Batch size: {config.BATCH_SIZE}")
        return True
    except Exception as e:
        print(f"✗ Config error: {e}")
        return False


def test_audio_processor():
    """Test if AudioProcessor can be initialized"""
    print("\n\nTesting audio processor...\n")
    
    try:
        from audio_processor import AudioProcessor
        processor = AudioProcessor()
        print(f"✓ AudioProcessor initialized")
        print(f"  - Sample rate: {processor.sample_rate} Hz")
        print(f"  - Duration: {processor.duration} seconds")
        print(f"  - Mel bands: {processor.n_mels}")
        return True
    except Exception as e:
        print(f"✗ AudioProcessor error: {e}")
        return False


def test_model():
    """Test if model can be created"""
    print("\n\nTesting model creation...\n")
    
    try:
        from model import create_cnn_model, compile_model
        
        # Create dummy model
        input_shape = (128, 87, 1)
        model = create_cnn_model(input_shape)
        model = compile_model(model)
        
        print(f"✓ Model created successfully")
        print(f"  - Total parameters: {model.count_params():,}")
        print(f"  - Input shape: {input_shape}")
        print(f"  - Output 1 (instruments): {model.outputs[0].shape}")
        print(f"  - Output 2 (notes): {model.outputs[1].shape}")
        return True
    except Exception as e:
        print(f"✗ Model error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 70)
    print("AUDIO CLASSIFIER - SETUP TEST")
    print("=" * 70)
    
    results = []
    
    results.append(("Package imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Audio processor", test_audio_processor()))
    results.append(("Model creation", test_model()))
    
    print("\n\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n✓ All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Prepare your training data using prepare_data.py")
        print("2. Train the model using train.py")
        print("3. Start the web app using app.py")
    else:
        print("\n✗ Some tests failed. Please install missing packages:")
        print("  pip install -r requirements.txt")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())


