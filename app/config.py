from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Tuple

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:harvesteye_pass@db:5432/harvesteye"
    
    # Model Configuration
    MODEL_PATH: str = "/app/models/classifier_int8.onnx"
    INPUT_SIZE: Tuple[int, int] = (224, 224)
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Class definitions (matches the training dataset folder names)
    CLASS_NAMES: List[str] = [
        "Apple_scab",
        "Black_rot",
        "Cedar_apple_rust",
        "Healthy",
        "Tomato_Bacterial_spot",
        "Tomato_Early_blight",
        "Tomato_Late_blight",
        "Tomato_Leaf_Mold",
        "Tomato_healthy"
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
