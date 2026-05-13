import streamlit as st
import sys
import os

# Adjust path to find 'src' from the app folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.auth import check_auth

st.set_page_config(page_title="TomatoCare Expert", page_icon="🍅", layout="wide")

# Handle Security Globally
check_auth()

def main():
    st.title("🍅 TomatoCare Expert System")
    st.subheader("Advanced Multimodal Phytopathology Platform")
    
    if st.session_state.get('connected'):
        st.success(f"Welcome, Expert: **{st.session_state['user_name']}**")
    
    st.markdown("""
    ### 🚀 Getting Started
    Select a module from the **sidebar** to begin:
    
    * **Diagnostic Engine:** Perform real-time AI leaf analysis and get treatment plans.
    * **Analytics Dashboard:** View 30-day farm health trends and outbreaks.
    * **Encyclopedia:** Browse the scientific database of tomato pathogens.
    
    ---
    **System Specifications:**
    * **Core Model:** MobileNetV2 (95.4% Accuracy) [cite: 4]
    * **Data Fusion:** Visual Signatures + Live Environmental Metadata
    * **Status:** Connected to OpenWeather/Open-Meteo API
    """)

if __name__ == "__main__":
    main()

if st.sidebar.button("🛑 Secure Logout"):
    # Clear all session data
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Redirect to the main entry point
    st.switch_page("app.py")