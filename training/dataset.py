import os
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Dataset
from PIL import Image
import numpy as np

# Same classes used in config
CLASS_NAMES = [
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

class SyntheticPlantDataset(Dataset):
    """
    Generates synthetic noise images to allow the pipeline to run and build
    without downloading a real dataset.
    """
    def __init__(self, num_samples: int = 100, transform=None):
        self.num_samples = num_samples
        self.transform = transform
        self.classes = CLASS_NAMES

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # Generate random image
        img = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        img = Image.fromarray(img)
        label = np.random.randint(0, len(self.classes))
        
        if self.transform:
            img = self.transform(img)
            
        return img, label

def get_transforms(is_train: bool = True):
    """Get standard augmentation and normalization transforms."""
    if is_train:
        return transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

def get_dataloaders(data_dir: str = None, batch_size: int = 32):
    """Returns train and validation dataloaders."""
    train_transform = get_transforms(is_train=True)
    val_transform = get_transforms(is_train=False)

    if data_dir and os.path.exists(data_dir):
        # Use real dataset (e.g., PlantVillage structure)
        train_dir = os.path.join(data_dir, 'train')
        val_dir = os.path.join(data_dir, 'val')
        
        train_dataset = datasets.ImageFolder(train_dir, transform=train_transform)
        val_dataset = datasets.ImageFolder(val_dir, transform=val_transform)
    else:
        # Fallback to synthetic data for development
        print("WARNING: Data directory not found or not provided. Using synthetic data.")
        train_dataset = SyntheticPlantDataset(num_samples=1000, transform=train_transform)
        val_dataset = SyntheticPlantDataset(num_samples=200, transform=val_transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    return train_loader, val_loader
