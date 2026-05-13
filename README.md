# TomatoCare AI: Multimodal Disease Diagnosis Expert System

##  Overview
A Software Engineering Final Year Project implementing an Explainable AI (XAI) framework for tomato pathology. 
The system integrates **MobileNetV2 CNN architecture** with **Real-time Environmental Data** (OpenWeather API) to provide high-accuracy, context-aware diagnoses.

##  Key Features
- **Authentication:** Features a secure, encrypted local JSON registration.
- **Defensive Image Filtering:** Prevents "Garbage-In, Garbage-Out" by computationally filtering images for motion blur, overexposure, and occlusion prior to AI inference.
- **Multimodal Sensor Fusion:** Combines visual lesion detection with live macro-climate suitability (Temperature & Humidity) to calculate an accurate Environmental Risk Index.
- **Explainable AI (XAI):** Generates PyTorch-based **Grad-CAM** heatmaps to visually prove exactly where the AI detected the pathogen.
- **Expert Knowledge Base:** Provides chemically and biologically accurate treatment plans, dynamic dosage calculators, and verifiable institutional references.

##  Installation & Setup Guide

# Step 1: Clone the Repository

git clone 
cd TomatoCare_Project

#Step 2: Create and Activate the Virtual Environment (venv)

For Windows Users (Cursor / VS Code Terminal):
python -m venv venv
venv\Scripts\activate

For macOS / Linux Users:
python3 -m venv venv
source venv/bin/activate

#Step 3: Install Dependencies
pip install -r requirements.txt

 Running the Application
Always ensure your virtual environment is activated (venv) before running any project commands. Ensure you run this from the root directory.

To launch the Expert System GUI:
streamlit run app/app.py


System Micro-Architecture
The codebase follows strict Single Responsibility Principles (SRP) via a dedicated micro-architecture:

Plaintext
TomatoCare_Project/
├── app/                     # Frontend Application Layer
│   ├── app.py               # Main Streamlit Dashboard
│   └── users.json           # Secure local encrypted user database
├── data/                    # Raw & Processed Datasets
├── outputs/                 # Saved model weights (.pth)
└── src/                     # Core Business & AI Logic
    ├── config/              # Global Configurations
    ├── evaluation/          # Confusion matrices and testing scripts
    ├── explainability/      # Grad-CAM visualizations
    ├── fusion/              # Multimodal Probabilistic Late Fusion logic
    ├── image_quality/       # Laplacian Variance & HSV Occlusion filtering
    ├── knowledge/           # Identification guides
    ├── models/              # Model loaders
    ├── training/            # PyTorch model training pipeline
    └── utils/               # Helpers
        ├── auth.py          # Dual-Pathway Authentication routing
        └── weather.py       # Geocoder and OpenWeather API integration

## References
- Sandler, M., et al. (2018). *MobileNetV2: Inverted Residuals and Linear Bottlenecks.*
- Lundberg, S. M. (2017). *A Unified Approach to Interpreting Model Predictions (SHAP).*
