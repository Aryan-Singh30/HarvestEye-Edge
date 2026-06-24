# 🌾 HarvestEye-Edge

> **AI-powered crop defect detection at the edge — sub-50ms inference on CPU.**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-INT8-FF6F00?logo=onnx&logoColor=white)](https://onnxruntime.ai)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🎯 What Is This?

HarvestEye-Edge is an **end-to-end crop disease detection service** that takes photos of crop leaves, **segments infected regions**, **classifies the disease**, and serves results with **sub-50ms latency** — optimized for CPU-based edge environments like farm-gate computers.

### How It Works

```
📷 Leaf Image → 🔄 Preprocessing → 🧠 ONNX Inference (INT8) → 🗺️ Heatmap + Classification → 📊 Audit Log
     ↓                                                                      ↓
  Camera/Upload                                                     < 50ms on CPU
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Static)                     │
│   Drag-Drop Upload │ Camera Capture │ Heatmap Overlay   │
│   Latency Flame Chart │ Scan Dashboard │ API Docs       │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP POST /api/v1/scan
┌──────────────────────▼──────────────────────────────────┐
│                  Nginx Reverse Proxy                     │
│            Rate Limiting │ CORS │ Gzip                   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   FastAPI Server                         │
│                                                          │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐ │
│  │ Preprocess   │──▶│ ONNX Runtime │──▶│ Postprocess   │ │
│  │ (NumPy/CV2)  │   │ (INT8 CPU)   │   │ (Heatmap)     │ │
│  └─────────────┘   └──────────────┘   └──────┬───────┘ │
│                                               │         │
│                    ┌──────────────────────────▼───────┐ │
│                    │  PostgreSQL (Async Audit Logs)    │ │
│                    └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 🔬 **Disease Heatmap** | Visual overlay showing exactly where infection is detected on the leaf |
| ⚡ **Latency Flame Chart** | Real-time breakdown of preprocessing, inference, and postprocessing times |
| 🖥️ **Edge Simulator** | Compare inference speeds across Cloud GPU, Edge CPU, and Raspberry Pi |
| 📊 **Scan Dashboard** | Historical scan analytics with disease distribution charts |
| 📷 **Camera Capture** | Direct camera access on mobile devices for field scanning |
| 📖 **API Documentation** | Interactive API docs with curl examples and response schemas |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **ML Training** | PyTorch, torchvision (ResNet18 transfer learning) |
| **Inference** | ONNX Runtime with INT8 Dynamic Quantization |
| **Backend** | FastAPI, asyncio, asyncpg |
| **Database** | PostgreSQL (audit logging) |
| **Frontend** | HTML5, Vanilla CSS, Vanilla JavaScript |
| **Reverse Proxy** | Nginx |
| **Containerization** | Docker & Docker Compose |

---

## 📦 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (for training only)

### Run with Docker
```bash
# Clone the repository
git clone https://github.com/yourusername/HarvestEye-Edge.git
cd HarvestEye-Edge

# Start all services
docker compose up --build

# Open in browser
# Frontend: http://localhost:8080
# API:      http://localhost:8000/docs
```

### Train Your Own Model
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Train (uses synthetic data by default)
python -m training.train --epochs 10 --batch-size 32

# Export to ONNX
python -m training.export_onnx

# Quantize to INT8
python -m training.quantize

# Benchmark
python -m training.benchmark
```

---

## 📡 API Reference

### POST `/api/v1/scan`
Upload a leaf image for disease detection.

```bash
curl -X POST http://localhost:8000/api/v1/scan \
  -F "file=@leaf_image.jpg"
```

**Response:**
```json
{
  "scan_id": "550e8400-e29b-41d4-a716-446655440000",
  "defect_class": "Tomato_Early_blight",
  "confidence": 0.947,
  "probabilities": {
    "Apple_scab": 0.002,
    "Tomato_Early_blight": 0.947,
    "Healthy": 0.012
  },
  "latency": {
    "preprocessing_ms": 3.2,
    "inference_ms": 28.5,
    "postprocessing_ms": 1.1,
    "total_ms": 32.8
  },
  "timestamp": "2026-06-23T08:30:00Z"
}
```

### GET `/api/v1/history`
Retrieve paginated scan history.

### GET `/api/v1/stats`
Get aggregate scan statistics.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with 🌱 for sustainable agriculture
</p>
