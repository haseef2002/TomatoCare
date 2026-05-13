import torch
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from src.config.config import CLASS_NAMES

class ModelEvaluator:
    """
    Generates academic-standard evaluation metrics for the thesis.
    """
    @staticmethod
    def generate_report(y_true, y_pred):
        """Prints a detailed classification report."""
        print("\n--- Classification Report ---")
        print(classification_report(y_true, y_pred, target_names=CLASS_NAMES))
        
    @staticmethod
    def plot_confusion_matrix(y_true, y_pred):
        """Generates a heatmap for the Confusion Matrix."""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cmap='Greens')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('TomatoCare AI: Confusion Matrix')
        plt.show()

