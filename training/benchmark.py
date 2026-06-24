import time
import numpy as np
import onnxruntime as ort
from pathlib import Path

def benchmark_model(model_path: str, num_runs: int = 100, target_ms: float = 50.0):
    """
    Benchmarks an ONNX model to measure CPU inference latency.
    """
    if not Path(model_path).exists():
        print(f"ERROR: Model {model_path} not found.")
        return

    print(f"\n--- Benchmarking {model_path} ---")
    
    # Configure session for CPU
    sess_options = ort.SessionOptions()
    sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    sess_options.intra_op_num_threads = 2
    sess_options.inter_op_num_threads = 1
    
    session = ort.InferenceSession(model_path, sess_options=sess_options, providers=['CPUExecutionProvider'])
    input_name = session.get_inputs()[0].name
    
    # Dummy input (Batch=1, Channels=3, H=224, W=224)
    dummy_input = np.random.randn(1, 3, 224, 224).astype(np.float32)

    # Warmup
    print("Warming up (10 runs)...")
    for _ in range(10):
        session.run(None, {input_name: dummy_input})

    # Benchmark
    print(f"Running benchmark ({num_runs} runs)...")
    latencies = []
    
    for _ in range(num_runs):
        t0 = time.perf_counter()
        session.run(None, {input_name: dummy_input})
        latencies.append((time.perf_counter() - t0) * 1000.0)

    # Stats
    mean_lat = np.mean(latencies)
    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)
    p99 = np.percentile(latencies, 99)

    print(f"Mean Latency: {mean_lat:.2f} ms")
    print(f"p50 Latency:  {p50:.2f} ms")
    print(f"p95 Latency:  {p95:.2f} ms")
    print(f"p99 Latency:  {p99:.2f} ms")
    
    if mean_lat < target_ms:
        print(f"✅ SUCCESS: Mean latency ({mean_lat:.2f}ms) is below target ({target_ms}ms).")
    else:
        print(f"❌ WARNING: Mean latency ({mean_lat:.2f}ms) exceeds target ({target_ms}ms).")

if __name__ == "__main__":
    fp32_model = "models/classifier_fp32.onnx"
    int8_model = "models/classifier_int8.onnx"
    
    benchmark_model(fp32_model, num_runs=50)
    benchmark_model(int8_model, num_runs=100, target_ms=50.0)
