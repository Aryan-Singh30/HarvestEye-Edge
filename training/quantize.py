import os
from pathlib import Path
import onnxruntime as ort
from onnxruntime.quantization import quantize_dynamic, QuantType

def quantize_onnx_model(input_model_path: str = "models/classifier_fp32.onnx",
                        output_model_path: str = "models/classifier_int8.onnx"):
    """
    Applies dynamic INT8 quantization to an ONNX model.
    This drastically reduces model size and accelerates inference on CPUs.
    """
    if not Path(input_model_path).exists():
        print(f"ERROR: Input model {input_model_path} does not exist. Run export_onnx.py first.")
        return

    print(f"Quantizing {input_model_path} to INT8...")

    quantize_dynamic(
        model_input=input_model_path,
        model_output=output_model_path,
        weight_type=QuantType.QUInt8
    )

    # Compare file sizes
    fp32_size = os.path.getsize(input_model_path) / (1024 * 1024)
    int8_size = os.path.getsize(output_model_path) / (1024 * 1024)

    print(f"Quantization complete. Saved to {output_model_path}")
    print(f"Original size (FP32): {fp32_size:.2f} MB")
    print(f"Quantized size (INT8): {int8_size:.2f} MB")
    print(f"Compression ratio: {fp32_size / int8_size:.2f}x")

if __name__ == "__main__":
    quantize_onnx_model()
