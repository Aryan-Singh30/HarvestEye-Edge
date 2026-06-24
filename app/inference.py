import time
import numpy as np
import onnxruntime as ort
from typing import Tuple, Dict
import logging

logger = logging.getLogger(__name__)

class ONNXEngine:
    def __init__(self, model_path: str, class_names: list[str]):
        """
        Initialize the ONNX Runtime session optimized for CPU edge inference.
        """
        self.class_names = class_names
        
        # Optimize execution for CPU (INT8 quantized models)
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        # Limit threads to prevent contention on edge devices
        # Typically 1-2 threads is optimal for small models on CPU
        sess_options.intra_op_num_threads = 2
        sess_options.inter_op_num_threads = 1
        
        try:
            self.session = ort.InferenceSession(
                model_path, 
                sess_options=sess_options,
                providers=['CPUExecutionProvider']
            )
            self.input_name = self.session.get_inputs()[0].name
            logger.info(f"Successfully loaded ONNX model from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load ONNX model: {e}")
            raise

    def predict(self, preprocessed_image: np.ndarray) -> Tuple[str, float, Dict[str, float], float, float]:
        """
        Run inference on a preprocessed image.
        Returns: (predicted_class, confidence, probabilities_dict, inference_ms, postprocessing_ms)
        """
        # 1. Inference
        t0 = time.perf_counter()
        raw_output = self.session.run(None, {self.input_name: preprocessed_image})[0]
        inference_ms = (time.perf_counter() - t0) * 1000.0

        # 2. Postprocessing (Softmax)
        t1 = time.perf_counter()
        
        # Stable softmax
        exp_scores = np.exp(raw_output[0] - np.max(raw_output[0]))
        probabilities = exp_scores / np.sum(exp_scores)
        
        predicted_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_idx])
        predicted_class = self.class_names[predicted_idx]
        
        # Create probabilities dictionary
        prob_dict = {
            self.class_names[i]: float(prob) 
            for i, prob in enumerate(probabilities)
        }
        
        postprocessing_ms = (time.perf_counter() - t1) * 1000.0

        return predicted_class, confidence, prob_dict, inference_ms, postprocessing_ms
