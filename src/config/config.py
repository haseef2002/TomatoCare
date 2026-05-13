# src/config/config.py
import os
import streamlit as st

# 1. DYNAMIC PATHING
# This calculates the project root (Tomatocare_Project) regardless of where the script is run.
# It goes up two levels from src/config/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# 2. SECURE SECRETS LOADING
OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "")

# 3. TARGET CLASSES
# Exact match for the PlantVillage dataset folders
CLASS_NAMES = [
    "Tomato___Bacterial_spot", 
    "Tomato___Early_blight", 
    "Tomato___Late_blight", 
    "Tomato___Leaf_Mold", 
    "Tomato___Septoria_leaf_spot", 
    "Tomato___Spider_mites_Two-spotted_spider_mite", 
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", 
    "Tomato___Tomato_mosaic_virus", 
    "Tomato___healthy"
]

# 4. ABSOLUTE MODEL PATH
# This ensures the InferenceEngine always finds the .pth file in outputs/models/
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "mobilenetv2_tomato.pth")

# 5. DATASET PATHS (For Training/Evaluation)
TRAIN_DATA_PATH = os.path.join(BASE_DIR, "data", "dataset_split", "train")
VAL_DATA_PATH = os.path.join(BASE_DIR, "data", "dataset_split", "val")
TEST_DATA_PATH = os.path.join(BASE_DIR, "data", "dataset_split", "test")