import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights

def create_model(num_classes: int) -> nn.Module:
    """
    Creates a ResNet18 model pre-trained on ImageNet.
    Replaces the final fully connected layer for our specific number of classes.
    """
    # Load pre-trained weights
    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    
    # Replace the final layer
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    return model

if __name__ == "__main__":
    # Test model creation
    from training.dataset import CLASS_NAMES
    model = create_model(len(CLASS_NAMES))
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    print(f"Model output shape: {output.shape}")
