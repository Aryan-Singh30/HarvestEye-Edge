# Build stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .

# Install dependencies required for building some python packages if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python packages into a specific directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Install runtime dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

# Set PYTHONPATH so absolute imports work
ENV PYTHONPATH=/

# Expose port
EXPOSE 8000

# Run FastAPI app with Uvicorn
# We use 1 worker because ONNX Runtime manages its own thread pool and
# we want to avoid thread contention on CPU-constrained edge devices.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
