import torch
import onnx
import onnxruntime as ort
from pathlib import Path
from training.model import create_model
from training.dataset import CLASS_NAMES

def export_to_onnx(weights_path: str = "models/best_model.pth", 
                   output_path: str = "models/classifier_fp32.onnx"):
    """
    Exports the trained PyTorch model to ONNX format with dynamic batch sizes.
    """
    print(f"Exporting model from {weights_path} to ONNX...")
    
    # Initialize model
    num_classes = len(CLASS_NAMES)
    model = create_model(num_classes)
    
    # Load weights if available, else export untrained for testing
    if Path(weights_path).exists():
        # Map location cpu ensures we can export on machines without CUDA
        model.load_state_dict(torch.load(weights_path, map_location=torch.device('cpu')))
        print("Loaded trained weights.")
    else:
        print(f"WARNING: {weights_path} not found. Exporting untrained model for testing.")
        # Ensure models directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    model.eval()

    # Dummy input for tracing (Batch Size, Channels, Height, Width)
    dummy_input = torch.randn(1, 3, 224, 224)

    # Export
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=14,          # Opset 14 is highly compatible and modern
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )

    print(f"Successfully exported to {output_path}")

    # Verify the exported model
    onnx_model = onnx.load(output_path)
    onnx.checker.check_model(onnx_model)
    print("ONNX model checker passed.")

if __name__ == "__main__":
    export_to_onnx()
