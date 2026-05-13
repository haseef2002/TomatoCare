# src/training/train.py
import os
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from src.training.data_loader import get_dataloaders

# --- Hyperparameters ---
DATA_DIR = "data/plantvillage_raw"
MODEL_SAVE_PATH = "outputs/models/mobilenetv2_tomato.pth"
EPOCHS = 15
BATCH_SIZE = 32
LEARNING_RATE = 0.001

def train_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    # 1. Load Data
    train_loader, val_loader, test_loader, class_names = get_dataloaders(DATA_DIR, BATCH_SIZE)
    print(f"Classes found ({len(class_names)}): {class_names}")

    # 2. Initialize Model (Transfer Learning)
    # Using weights=models.MobileNet_V2_Weights.DEFAULT instead of deprecated pretrained=True
    model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
    
    # Freeze early feature-extraction layers to speed up training & prevent overfitting
    for param in model.features.parameters():
        param.requires_grad = False

    # Replace the classifier head to match our 10 classes
    num_ftrs = model.classifier[1].in_features
    model.classifier[1] = nn.Sequential(
        nn.Dropout(p=0.3),
        nn.Linear(num_ftrs, len(class_names))
    )
    model = model.to(device)

    # 3. Define Loss & Optimizer
    criterion = nn.CrossEntropyLoss()
    # Only optimize the classifier parameters initially
    optimizer = optim.Adam(model.classifier.parameters(), lr=LEARNING_RATE)
    # Learning rate scheduler: Reduces LR if validation loss stops improving
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3)

    # 4. Training Loop
    best_model_wts = copy.deepcopy(model.state_dict())
    best_acc = 0.0

    for epoch in range(EPOCHS):
        print(f'Epoch {epoch+1}/{EPOCHS}')
        print('-' * 10)

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
                dataloader = train_loader
            else:
                model.eval()   # Set model to evaluate mode
                dataloader = val_loader

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data
            for inputs, labels in dataloader:
                inputs = inputs.to(device)
                labels = labels.to(device)

                optimizer.zero_grad()

                # Forward pass
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # Backward pass + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / len(dataloader.dataset)
            epoch_acc = running_corrects.double() / len(dataloader.dataset)

            print(f'{phase.capitalize()} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            if phase == 'val':
                scheduler.step(epoch_loss)
                # Deep copy the model if it's the best one so far
                if epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())

        print()

    print(f'Training complete. Best Validation Accuracy: {best_acc:.4f}')

    # 5. Save the Best Model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    model.load_state_dict(best_model_wts)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")

if __name__ == '__main__':
    train_model()