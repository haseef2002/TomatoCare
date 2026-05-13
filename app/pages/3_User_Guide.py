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

# Page Configuration
st.set_page_config(page_title="User Guide | TomatoCare", page_icon="📖", layout="wide")

# Modern Styling
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .guide-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px; border-top: 5px solid #2e7d32; }
    .feature-header { color: #1b5e20; font-weight: bold; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📖 TomatoCare User Guide & System Features")
st.markdown("Welcome to the **TomatoCare Expert System**, an advanced phytopathology platform designed for high-accuracy tomato disease diagnosis and field management.")

# --- SECTION 1: CORE WORKFLOW ---
st.header("🚀 How to Perform a Diagnosis")
st.markdown("""
Follow these three simple steps to get an expert-level diagnostic report:
1. **Field Acquisition:** Use the **Field Camera** button to take a live photo of a symptomatic leaf or upload a high-resolution image from your gallery.
2. **Environmental Context:** The system automatically fetches live weather data (Temperature & Humidity) based on your location to improve diagnostic accuracy.
3. **Review Results:** Analyze the system's certainty score, view the AI heatmap, and download your **PDF Treatment Plan**.
""")

# --- SECTION 2: ADVANCED FEATURES (THE "WHY") ---
st.header("🛠️ Advanced System Features")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown('<div class="guide-card">', unsafe_allow_html=True)
        st.markdown('<p class="feature-header">🔍 Neural Image Quality Gate</p>', unsafe_allow_html=True)
        st.write("Before analysis, our 'Gatekeeper' algorithm checks for motion blur, glare, and low contrast. This ensures the AI only processes images clear enough for accurate lesion detection.")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="guide-card">', unsafe_allow_html=True)
        st.markdown('<p class="feature-header">🌍 Multimodal Late Fusion</p>', unsafe_allow_html=True)
        st.write("TomatoCare doesn't just look at photos. It fuses visual AI patterns with live weather metadata to calculate a real-world 'Environmental Risk Index' for your crops.")
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    with st.container():
        st.markdown('<div class="guide-card">', unsafe_allow_html=True)
        st.markdown('<p class="feature-header">🕵️ Explainable AI (XAI)</p>', unsafe_allow_html=True)
        st.write("We provide full transparency. **Grad-CAM** heatmaps show exactly where the AI saw the disease, and **SHAP** charts show how much the weather influenced the final result.")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="guide-card">', unsafe_allow_html=True)
        st.markdown('<p class="feature-header">📊 Predictive Analytics</p>', unsafe_allow_html=True)
        st.write("Monitor your farm's health over time with the **30-Day Trend Dashboard** and stay ahead of outbreaks with the **7-Day Risk Forecast**.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3: SAFETY & COMPLIANCE ---
st.divider()
st.header("⚖️ Safety & Accuracy Standards")
st.info("""
**Responsible AI:** To prevent incorrect chemical application, TomatoCare uses a **Dynamic Confidence Gate**. If the AI certainty is below the required safety threshold (e.g., 80%), the system will request a clearer photo rather than providing a prescription. [cite: 34, 36]
""")

st.caption("TomatoCare v1.0.0 | Developed for IIT Final Year Project 2026")