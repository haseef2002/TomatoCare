# evaluate.py

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from src.config import CLASS_NAMES

def generate_thesis_metrics(y_true, y_pred):
    """Generates legally and academically justifiable metrics."""
    print("=== ACADEMIC CLASSIFICATION REPORT ===")
    print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))
    
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title('TomatoCare AI: Multi-Class Confusion Matrix', fontsize=16)
    plt.ylabel('Ground Truth (Actual)', fontsize=12)
    plt.xlabel('AI Prediction', fontsize=12)
    plt.tight_layout()
    plt.savefig('outputs/plots/confusion_matrix.png')
    print("Saved confusion matrix to outputs/plots/confusion_matrix.png")

# Example usage for testing
if __name__ == "__main__":
    # Simulated test data
    y_true = np.random.randint(0, 10, 100)
    y_pred = y_true.copy()
    y_pred[::10] = np.random.randint(0, 10, 10) # Inject 10% errors
    generate_thesis_metrics(y_true, y_pred)