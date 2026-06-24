git config --global user.name "Aryan"
git config --global user.email "aryan@example.com"

# Phase 1: Foundation
git add README.md .gitignore
git commit -m "chore: initialize repository and documentation"

git add pyproject.toml requirements.txt
git commit -m "chore: add dependency management and requirements"

git add docker-compose.yml Dockerfile
git commit -m "chore: add base docker configuration"

# Phase 2: ML Pipeline
git add training/__init__.py
git commit -m "feat(ml): initialize training module"

git add training/dataset.py
git commit -m "feat(ml): implement PlantVillage dataset loader and augmentations"

git add training/model.py
git commit -m "feat(ml): define ResNet18 transfer learning architecture"

git add training/train.py
git commit -m "feat(ml): implement model training loop with validation"

git add training/export_onnx.py
git commit -m "feat(ml): add FP32 ONNX export pipeline"

git add training/quantize.py
git commit -m "feat(ml): implement INT8 dynamic quantization"

git add training/benchmark.py
git commit -m "perf(ml): add latency benchmarking script"

# Phase 3: Backend DB
git add app/__init__.py
git commit -m "feat(backend): initialize backend module"

git add app/database.py
git commit -m "feat(db): configure asyncpg PostgreSQL connection"

git add app/models.py
git commit -m "feat(db): define scan history database tables"

git add app/schemas.py
git commit -m "feat(backend): add Pydantic validation schemas"

git add app/crud.py
git commit -m "feat(db): implement async CRUD operations"

# Phase 4: API & Inference
git add app/inference.py
git commit -m "feat(inference): integrate ONNX Runtime engine"

git add app/main.py
git commit -m "feat(api): implement FastAPI server and scan endpoints"

# Phase 5: Nginx & Frontend Base
git add nginx/
git commit -m "feat(proxy): configure Nginx reverse proxy with rate limiting"

git add frontend/index.html
git commit -m "feat(ui): create main scanning interface layout"

git add frontend/css/
git commit -m "style(ui): apply Cargill theme and styling"

git add frontend/js/app.js
git commit -m "feat(ui): implement API client and connection logic"

git add frontend/js/upload.js
git commit -m "feat(ui): implement drag-and-drop and camera capture"

git add frontend/js/flamechart.js
git commit -m "feat(ui): add D3 latency flame chart visualizations"

# Phase 6: Advanced Frontend
git add frontend/dashboard.html
git commit -m "feat(ui): build historical analytics dashboard view"

git add frontend/api-docs.html
git commit -m "feat(ui): integrate swagger developer portal"

git add models/.gitkeep
git commit -m "chore: initialize models directory"

git add .
git commit -m "fix: resolve minor integration issues across stack"
