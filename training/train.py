import argparse
import os
import torch
import torch.nn as nn
import torch.optim as optim
from pathlib import Path
from training.dataset import get_dataloaders, CLASS_NAMES
from training.model import create_model

def train_model(data_dir: str, epochs: int, batch_size: int, lr: float):
    # Setup device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Ensure models directory exists
    Path("models").mkdir(parents=True, exist_ok=True)
    best_model_path = Path("models/best_model.pth")

    # Get data
    train_loader, val_loader = get_dataloaders(data_dir, batch_size)
    num_classes = len(CLASS_NAMES)

    # Initialize model
    model = create_model(num_classes).to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', factor=0.1, patience=3)

    best_val_acc = 0.0

    print("Starting training...")
    for epoch in range(epochs):
        # Training Phase
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = correct / total

        # Validation Phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * inputs.size(0)
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()

        val_epoch_loss = val_loss / len(val_loader.dataset)
        val_epoch_acc = val_correct / val_total

        print(f"Epoch {epoch+1}/{epochs} | "
              f"Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f} | "
              f"Val Loss: {val_epoch_loss:.4f} Acc: {val_epoch_acc:.4f}")

        # Learning rate scheduling
        scheduler.step(val_epoch_acc)

        # Save best model
        if val_epoch_acc > best_val_acc:
            best_val_acc = val_epoch_acc
            torch.save(model.state_dict(), best_model_path)
            print(f"--> Saved new best model with Val Acc: {best_val_acc:.4f}")

    print(f"Training complete. Best Validation Accuracy: {best_val_acc:.4f}")
    print(f"Model saved to {best_model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train HarvestEye-Edge Classifier")
    parser.add_argument("--data-dir", type=str, default=None, help="Path to PlantVillage dataset (optional)")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--lr", type=float, default=1e-3, help="Learning rate")
    
    args = parser.parse_args()
    train_model(args.data_dir, args.epochs, args.batch_size, args.lr)
