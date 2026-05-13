# src/training/data_loader.py
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split, Dataset

class DatasetWrapper(Dataset):
    """Wraps a dataset subset to apply specific transforms without leaking."""
    def __init__(self, subset, transform=None):
        self.subset = subset
        self.transform = transform

    def __getitem__(self, index):
        x, y = self.subset[index]
        if self.transform:
            x = self.transform(x)
        return x, y

    def __len__(self):
        return len(self.subset)

def get_dataloaders(data_dir, batch_size=32):
    # 1. Heavy Data Augmentation for Training (Prevents memorizing backgrounds)
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.8, 1.0)), # Zooms in slightly
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.RandomRotation(45),                       # Increased rotation
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2), 
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # 2. Strict Transforms for Validation/Testing (No augmentation)
    val_test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load base dataset WITHOUT transforms (we apply them in the wrapper)
    # Using a dummy transform temporarily to satisfy ImageFolder, but overriding it later
    base_transform = transforms.ToTensor()
    full_dataset = datasets.ImageFolder(root=data_dir, transform=None) 
    
    # Calculate splits (70/15/15)
    total_size = len(full_dataset)
    train_size = int(0.7 * total_size)
    val_size = int(0.15 * total_size)
    test_size = total_size - train_size - val_size

    train_subset, val_subset, test_subset = random_split(
        full_dataset, [train_size, val_size, test_size], 
        generator=torch.Generator().manual_seed(42)
    )

    # Wrap subsets to apply correct augmentations safely
    train_dataset = DatasetWrapper(train_subset, transform=train_transform)
    val_dataset = DatasetWrapper(val_subset, transform=val_test_transform)
    test_dataset = DatasetWrapper(test_subset, transform=val_test_transform)

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=2)

    return train_loader, val_loader, test_loader, full_dataset.classes