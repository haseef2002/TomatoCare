import streamlit as st
import sys
import os

# Path fix to find 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 1. Initialize History Global Variable
if 'history' not in st.session_state:
    st.session_state.history = []

# 2. Access Control Gatekeeper
if not st.session_state.get('connected') and not st.session_state.get('guest_mode'):
    st.warning("🔒 Please login on the Home page to access this module.")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# Path fix to reach 'src' from the 'pages' subfolder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.knowledge_base import DISEASE_KB

st.set_page_config(page_title="Scientific References | TomatoCare", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .ref-card { background: white; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #1b5e20; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Academic & Institutional Foundation")
st.markdown("""
To ensure complete transparency, legal compliance, and scientific validity, all diagnostic logic, chemical dosages, and environmental risk parameters within TomatoCare are derived from peer-reviewed phytopathology guidelines.
""")

st.header("1. Pathogen-Specific Clinical Protocols")
st.write("The following institutional sources verify the treatment plans and fatality risks identified by the engine.")

# Dynamically generate reference cards from your Knowledge Base
for key in DISEASE_KB:
    data = DISEASE_KB[key]
    with st.container():
        st.markdown(f"""
        <div class="ref-card">
            <h4 style="margin:0;">{data['common']}</h4>
            <p style="font-size: 0.9rem; color: #666;">Verified via: {data['ref_source']}</p>
        </div>
        """, unsafe_allow_html=True)
        st.link_button(f"🌐 View Official {data['common']} Protocol", data['ref_url'])
        st.divider()

st.header("2. Software Architecture & AI Licenses")
st.markdown("""
The TomatoCare system utilizes high-performance open-source frameworks and verified datasets:

* **Deep Learning Architecture**: MobileNetV2 (Sandler et al., 2018).
* **Explainable AI (XAI)**: Grad-CAM (Selvaraju et al., 2017) and SHAP (Lundberg & Lee, 2017).
* **Training Dataset**: PlantVillage Tomato Subset (Mohanty et al., 2016).
* **Weather Intelligence**: Open-Meteo (Non-Commercial License) and OpenWeatherMap API.
* **UI Framework**: Streamlit (Apache 2.0 License).
""")

st.info("⚖️ **Disclaimer:** This system is an AI-powered decision-support tool. Diagnosis results should be verified by a certified agronomist before large-scale chemical application.")