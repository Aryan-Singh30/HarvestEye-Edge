import cv2
import numpy as np
import hashlib
from typing import Tuple

def compute_hash(image_bytes: bytes) -> str:
    """Compute SHA256 hash of the image for deduplication/tracking."""
    return hashlib.sha256(image_bytes).hexdigest()

def preprocess_image(image_bytes: bytes, target_size: Tuple[int, int] = (224, 224)) -> np.ndarray:
    """
    Preprocess image bytes for ResNet ONNX inference.
    Uses OpenCV/NumPy for speed instead of PIL.
    """
    # Decode image bytes to numpy array (BGR format)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Invalid image data")

    # Resize to target size
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)
    
    # Convert BGR (OpenCV default) to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Convert to float32 and scale to [0, 1]
    img = img.astype(np.float32) / 255.0
    
    # ImageNet Normalization
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img = (img - mean) / std
    
    # Convert HWC (Height, Width, Channels) to CHW (Channels, Height, Width)
    img = np.transpose(img, (2, 0, 1))
    
    # Add batch dimension: BCHW
    img = np.expand_dims(img, axis=0)
    
    return img
