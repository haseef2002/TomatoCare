🍅 TomatoCare AI: Multimodal Disease Diagnosis Expert System

## 🚀 Overview
TomatoCare AI is a Final Year Software Engineering Project implementing an **Explainable AI (XAI) framework** for tomato pathology. The system moves beyond traditional "black-box" image classifiers by integrating a **MobileNetV2 CNN architecture** with **Real-time Environmental Data** (via OpenWeather API) using Probabilistic Late Fusion.

## 🛠️ Key Features
- **Defensive Image Filtering:** Prevents "Garbage-In, Garbage-Out" by computationally filtering images for motion blur, overexposure, and occlusion (HSV masking) prior to AI inference.
- **Multimodal Sensor Fusion:** Combines visual lesion detection with live macro-climate suitability (Temperature & Humidity) to calculate an accurate, mathematically grounded Environmental Risk Index.
- **Explainable AI (XAI):** Generates PyTorch-based **Grad-CAM** heatmaps to visually prove to the user exactly where the AI detected the pathogen.
- **Expert Knowledge Base:** Provides chemically and biologically accurate treatment plans, dynamic dosage calculators (scaled per acre), and verifiable institutional references.

---

## 💻 Installation & Setup Guide

To ensure this project runs smoothly without conflicting with your system's global Python packages, it is designed to be run inside an isolated **Python Virtual Environment (`venv`)**.

### Prerequisites
- Python 3.9 or 3.10 installed on your system.
- Git installed.

### Step 1: Clone the Repository
```bash
git clone 
cd TomatoCare_Project
Step 2: Create and Activate the Virtual Environment (venv)
Creating a virtual environment isolates the project's dependencies (like specific versions of PyTorch and OpenCV).

For Windows Users (Command Prompt / VS Code / Cursor Terminal):

# 1. Create the virtual environment named 'venv'
python -m venv venv

# 2. Activate the virtual environment
venv\Scripts\activate
(Note: Once activated, you will see (venv) appear at the start of your terminal line. If you are using Windows PowerShell and receive an execution policy error, run: Set-ExecutionPolicy Unrestricted -Scope CurrentUser first).


For macOS / Linux Users:

# 1. Create the virtual environment
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate
Step 3: Install Dependencies

#With your (venv) activated, install the required packages:
pip install -r requirements.txt


# GPU Acceleration Note (NVIDIA Users): > If you have an NVIDIA GPU (e.g., RTX 3060/4070) and want to train the model locally, overwrite the default PyTorch installation with the CUDA-enabled version inside your active venv:
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu118](https://download.pytorch.org/whl/cu118)

# Step 4: Configure API Keys
The system requires an OpenWeather API key and Google Auth credentials to function fully.

Create a folder named .streamlit in the root directory.

Inside it, create a file named secrets.toml.

Add your keys securely:

Ini, TOML
OPENWEATHER_API_KEY = "your_api_key_here"
google_auth_credentials = "your_google_json_string_here"

# Running the Application
Always ensure your virtual environment is activated (venv) before running any project commands.

To launch the Expert System GUI:

# To launch the Expert System GUI:
streamlit run app.py
To train the model from scratch:

# To train the model from scratch:
python src/training/train.py

# To deactivate the environment when finished:
deactivate