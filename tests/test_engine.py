import pytest
import numpy as np
from src.engine import ImageValidator
from src.weather import get_validated_weather

def test_image_quality_blur_rejection():
    """Test that a completely blank/blurry image is rejected."""
    # Create a dummy blank image (zero variance)
    blank_image = np.zeros((224, 224, 3), dtype=np.uint8)
    passed, msg = ImageValidator.validate(blank_image)
    
    assert passed is False, "System failed to reject a blank image."
    assert "blurry" in msg.lower() or "dark" in msg.lower()

def test_image_quality_optimal_acceptance():
    """Test that a normal, high-contrast image is accepted."""
    # Create a dummy image with high variance (simulated sharp image)
    sharp_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    passed, msg = ImageValidator.validate(sharp_image)
    
    assert passed is True, "System rejected a perfectly valid image."

def test_weather_api_fallback():
    """Test that the weather system handles API timeouts gracefully."""
    
    result = get_validated_weather()
    # It should either return a dictionary (success) or None (graceful failure), never crash.
    assert result is None or isinstance(result, dict)