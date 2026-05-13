# src/engine.py
import cv2
import numpy as np
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import os

from src.config.config import CLASS_NAMES, MODEL_PATH
from src.utils.logger import get_logger

# Initialize it for this specific file
logger = get_logger(__name__)

class InferenceEngine:
    """
    Handles deep learning inference and XAI (Grad-CAM) generation.
    Optimized for IIT Final Year Project: Features Hook-based Heatmap Extraction.
    """
    def __init__(self):
        # Default to CPU for maximum compatibility during project viva/demo
        self.device = torch.device("cpu")
        
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                 std=[0.229, 0.224, 0.225])
        ])
        
        # XAI Hook Variables
        self.gradients = None
        self.activations = None
        
        self.model = self._load_model()
        
        # Register the hooks only if weights were found
        if self.model is not None:
            self._register_hooks()

    def _register_hooks(self):
        """Attaches sensors to the final convolutional layer to extract spatial features."""
        # For MobileNetV2, 'features[-1]' is the final 1x1 conv layer before global pooling
        target_layer = self.model.features[-1]
        target_layer.register_forward_hook(self._save_activation)
        # Using full_backward_hook for torch 2.0+ stability
        target_layer.register_full_backward_hook(self._save_gradient)

    def _save_activation(self, module, input, output):
        self.activations = output

    def _save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def _load_model(self):
            try:
                if not os.path.exists(MODEL_PATH):
                    # Upgraded to Critical Log
                    logger.critical(f"CRITICAL: Weights missing at {MODEL_PATH}")
                    return None

                # Load MobileNetV2 Architecture
                model = models.mobilenet_v2(weights=None)
                
                # Match the classifier head to our Tomato dataset (e.g., 10 classes)
                num_ftrs = model.classifier[1].in_features
                model.classifier[1] = nn.Linear(num_ftrs, len(CLASS_NAMES))
                
                # Load trained weights
                model.load_state_dict(torch.load(MODEL_PATH, map_location=self.device))
                model.to(self.device)
                model.eval() 
                
                # Info Log (Tracks silent successes in the background)
                logger.info("MobileNetV2 model loaded successfully into memory.")
                
                return model
            except Exception as e:
                # Error Log with full traceback (exc_info=True)
                logger.error(f"Model Initialization Error: {e}", exc_info=True)
                return None
    def predict(self, image_pil):
        """
        Predicts disease and returns (Class, Confidence, Grad-CAM Image).
        """
        if self.model is None:
            return "SYSTEM OFFLINE", 0.0, None
            
        try:
            # 1. Pre-process
            input_tensor = self.transform(image_pil).unsqueeze(0).to(self.device)
            input_tensor.requires_grad = True # Required for Backward pass (Grad-CAM)
            
            # 2. Forward pass
            outputs = self.model(input_tensor)
            probs = torch.nn.functional.softmax(outputs[0], dim=0)
            conf, idx = torch.max(probs, 0)
            
            # 3. Generate XAI Heatmap
            heatmap = self._generate_gradcam(original_image=image_pil, target_class_idx=idx.item(), outputs=outputs)
            
            return CLASS_NAMES[idx.item()], conf.item(), heatmap
            
        except Exception as e:
            print(f"Inference Engine Exception: {str(e)}")
            return "Prediction Error", 0.0, None

    def _generate_gradcam(self, original_image, target_class_idx, outputs):
        """
        Mathematically generates the heat-map highlighting diagnostic features.
        """
        try:
            # Clear existing gradients
            self.model.zero_grad()
            
            # Backward pass for the specific predicted class
            class_loss = outputs[0, target_class_idx]
            class_loss.backward(retain_graph=True)
            
            if self.gradients is None or self.activations is None:
                return None
                
            # Global Average Pooling of the Gradients
            pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
            
            # Weighted channel combination
            activations = self.activations.detach()[0]
            for i in range(activations.size(0)):
                activations[i, :, :] *= pooled_gradients[i]
            
            # Apply ReLU to the combined heatmap (we only care about positive influences)
            heatmap = torch.mean(activations, dim=0).squeeze().cpu().numpy()
            heatmap = np.maximum(heatmap, 0)
            
            # Normalize for Visualization
            if np.max(heatmap) > 0:
                heatmap /= np.max(heatmap)
            else:
                return None
                
            # OpenCV Processing: Jet Colormap Blending
            heatmap = cv2.resize(heatmap, (224, 224))
            heatmap = np.uint8(255 * heatmap)
            heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
            
            # Overlay heatmap on original image (resized)
            original_resized = np.array(original_image.resize((224, 224)))
            # Convert RGB to BGR for OpenCV weight blending
            original_resized = cv2.cvtColor(original_resized, cv2.COLOR_RGB2BGR)
            
            # Superimpose
            result = cv2.addWeighted(heatmap, 0.4, original_resized, 0.6, 0)
            
            # Final output conversion back to RGB for Streamlit compatibility
            return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            
        except Exception as e:
            print(f"Grad-CAM Generation Error: {e}")
            return None