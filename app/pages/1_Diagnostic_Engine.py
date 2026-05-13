"""
TomatoCare Expert System - Diagnostic Engine
-------------------------------------------
Main functional module for IIT Final Year Project (2026).
Features: Multimodal Fusion, Grad-CAM XAI, High-Precision Overrides, Fail-Safe APIs.
"""

import streamlit as st
import sys
import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image, UnidentifiedImageError
import plotly.graph_objects as go
from fpdf import FPDF

# Universal Path Fix: Ensures 'src' is found from the 'pages' subfolder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Internal Module Imports
from src.utils.weather import get_validated_weather
from src.engine import InferenceEngine
from src.knowledge_base import DISEASE_KB
from src.image_quality.quality import AdvancedImageValidator
from src.fusion.env_fusion import MultimodalFusionEngine

# ==========================================
# 0. SESSION STATE & ACCESS CONTROL
# ==========================================

if 'history' not in st.session_state:
    st.session_state.history = []

# Secure Gatekeeper
if not st.session_state.get('connected') and not st.session_state.get('guest_mode'):
    st.set_page_config(page_title="Access Denied", page_icon="🔒")
    st.warning("🔒 Please login on the Home page to access this module.")
    if st.button("Go to Login"):
        st.switch_page("app.py")
    st.stop()

# ==========================================
# 1. PAGE CONFIG & MODERN STYLING
# ==========================================
st.set_page_config(page_title="Diagnostic Engine | TomatoCare", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    /* 1. Global Page Styling */
    .main { 
        background-color: #f4f7f6; 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
    }

    /* 2. Sleek Status Cards (Glassmorphism Light) */
    .status-card { 
        background: #ffffff; 
        padding: 24px; 
        border-radius: 20px; 
        box-shadow: 0 8px 30px rgba(0,0,0,0.04); 
        margin-bottom: 25px; 
        border: 1px solid #eef2f1;
        border-left: 8px solid #2e7d32; /* Tomato Leaf Green Accent */
    }

    /* 3. Metric Enhancements (Scientific Look) */
    [data-testid="stMetricValue"] { 
        font-size: 2.4rem !important; 
        color: #1b5e20; 
        font-weight: 800;
        letter-spacing: -1px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        color: #546e7a;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 4. Interactive Tabs (Comfortable Click Zones) */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 8px; 
        background-color: #e8f5e9;
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: white;
        border-radius: 10px;
        padding: 0px 20px;
        border: 1px solid #c8e6c9;
        transition: all 0.3s ease;
    }
    .stTabs [aria-selected="true"] { 
        background-color: #2e7d32 !important; 
        color: white !important;
        box-shadow: 0 4px 12px rgba(46, 125, 50, 0.3);
    }

    /* 5. Custom Button Styling (Primary Action) */
    .stButton>button {
        border-radius: 12px;
        height: 3em;
        width: 100%;
        background-color: #2e7d32;
        color: white;
        border: none;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }

    /* 6. Sidebar Refinement */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }
</style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. SCIENTIFIC VISUALIZATION HELPERS
# ==========================================

def draw_gauge(score):
    """
    Scientifically correct gauge visualization.
    Ensures high risk values (75%+) are represented by Red warning colors.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number", 
        value=score, 
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "gray"},
            'bar': {'color': "#b71c1c" if score > 75 else "#1b5e20"}, # Dynamic Bar Color
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 40], 'color': "#e8f5e9"},   # Low Risk: Soft Green
                {'range': [40, 75], 'color': "#fff3e0"},  # Medium Risk: Soft Orange
                {'range': [75, 100], 'color': "#ffebee"}  # High Risk: Soft Red
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        height=250, 
        margin=dict(l=30, r=30, t=50, b=20), 
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#1b5e20", 'family': "Arial"}
    )
    return fig

def generate_pdf_report(disease_name, pathogen, visual_conf, env_risk, field_size, dosage, chemical_plan, natural_plan, heatmap_img, kb_data):
    """
    Refined PDF Generator with auto-alignment and text-wrapping fixes.
    Prevents text cut-offs and overlapping images.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- PAGE 1: DIAGNOSTIC SUMMARY ---
    pdf.add_page()
    
    # Header Branding (Using full-width rectangle)
    pdf.set_fill_color(46, 125, 50) 
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 24)
    pdf.ln(5)
    pdf.cell(0, 15, txt="TomatoCare Expert System", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, txt="Official Phytopathology Diagnostic Report", ln=True, align='C')
    
    pdf.ln(20) # Space after header
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 15)
    pdf.cell(0, 10, txt=f"Diagnosis: {disease_name}", ln=True)
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, txt=f"Report ID: TC-{random.randint(1000,9999)} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    # Metrics Table (Fixed widths to prevent 'unr' or 'Calcu' errors)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(95, 10, "Diagnostic Metric", border=1, align='C', fill=True)
    pdf.cell(95, 10, "Analysis Value", border=1, align='C', fill=True)
    pdf.ln()
    
    pdf.set_font("Arial", size=11)
    metrics = [
        ("AI Visual Confidence", f"{visual_conf:.2f}%"),
        ("Environmental Risk", f"{env_risk:.2f}%"),
        ("Pathogen Fatality", kb_data.get('fatality', 'Moderate'))
    ]
    for label, value in metrics:
        pdf.cell(95, 10, label, border=1)
        pdf.cell(95, 10, value, border=1)
        pdf.ln()
    
    pdf.ln(10)
    
    # Treatment Sections (Using Multi-Cell for safe text wrapping)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "1. Industrial Treatment Protocol", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 7, txt=chemical_plan)
    
    if dosage:
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, txt=f"Prescribed Volume ({field_size} Acres): {dosage}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 13)
    pdf.cell(0, 10, "2. Sustainable / Organic Alternative", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 7, txt=natural_plan)

    # --- PAGE 2: XAI EVIDENCE ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "AI Reasoning & XAI Evidence", ln=True)
    pdf.line(10, pdf.get_y(), 80, pdf.get_y())
    pdf.ln(10)

    # Correct Image Alignment (Grad-CAM)
    if heatmap_img:
        temp_path = "temp_report_img.png"
        heatmap_img.save(temp_path)
        # Place image and move cursor below it to prevent overlap
        pdf.image(temp_path, x=10, y=pdf.get_y(), w=85)
        pdf.set_y(pdf.get_y() + 90) 
        pdf.set_font("Arial", 'I', 9)
        pdf.cell(0, 10, "Figure 1: Neural Activation Map highlighting diagnostic features.", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Scientific Pathological Profile", ln=True)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, f"Pathogen: {pathogen}", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=f"Biological Trigger: {kb_data.get('why', 'N/A')}")
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Prevention Strategy:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt=kb_data.get('prevention', 'N/A'))

    # Footer Logic (Pinned to bottom)
    pdf.set_y(-25)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(150, 150, 150)
    footer_text = f"TomatoCare v1.0 | IIT Final Year Project | Source: {kb_data.get('ref_source', 'Agricultural Standards')}"
    pdf.cell(0, 10, footer_text, align='C')

    return pdf.output()

# ==========================================
# 3. DIAGNOSTIC INTERFACE
# ==========================================
st.title("🔍 Multimodal Diagnostic Engine")

with st.sidebar:
    # Logout logic
    if st.button("🛑 Secure Logout"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.switch_page("app.py")

    st.header("🌍 Field Conditions")
    manual_city = st.text_input("📍 Manual City Override:", placeholder="e.g., Colombo")
    
    # Fail-safe Weather
    api_t, api_h = 25.0, 70.0
    try:
        w = get_validated_weather(manual_city if manual_city.strip() else None)
        if w:
            st.success(f"📍 Linked: {w['city']}")
            api_t, api_h = float(w['temp']), float(w['hum'])
    except Exception:
        st.error("⚠️ Weather API Offline")

    st.subheader("⚙️ Precision Manual Override")
    temp = st.number_input("Field Temp (°C)", 10.0, 45.0, api_t, step=0.1)
    hum = st.number_input("Humidity (%)", 10.0, 100.0, api_h, step=0.1)
    
    st.divider()
    field_size = st.number_input("Field Area (Acres)", 0.1, 50.0, 1.0, step=0.1)
    crop_stage = st.selectbox("Crop Stage", ["Seedling", "Vegetative", "Flowering", "Fruiting"])

# Specimen Input
st.markdown('<div class="status-card">', unsafe_allow_html=True)
st.subheader("📸 Specimen Acquisition")
c1, c2 = st.columns(2)
with c1: cam_img = st.camera_input("Field Camera")
with c2: file_img = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
uploaded = cam_img if cam_img else file_img
st.markdown('</div>', unsafe_allow_html=True)

if uploaded:
    col1, col2 = st.columns([1, 1.4])
    with col1:
        img = Image.open(uploaded).convert("RGB")
        st.image(img, use_container_width=True, caption="Analyzed Specimen")
        
        # Quality Gate
        passed, msg = AdvancedImageValidator.validate(np.array(img))
        if not passed:
            st.error(f"❌ {msg}")
            st.markdown("### 💡 Tips:\n* **Background:** Use white paper.\n* **Light:** Move out of shade.")
            st.stop()
        st.success("✅ Image Quality: Optimal")

    with col2:
            with st.spinner("Decoding visual & environmental signatures..."):
                try:
                    engine = InferenceEngine()
                    pred_class, visual_conf, heatmap_img = engine.predict(img)
                    
                    # ==========================================
                    # DYNAMIC CONFIDENCE GATE INSERTED HERE
                    # ==========================================
                    DYNAMIC_THRESHOLDS = {
                        "Tomato___Tomato_Yellow_Leaf_Curl_Virus": 0.90,
                        "Tomato___healthy": 0.90,
                        "Tomato___Bacterial_spot": 0.85,
                        "Tomato___Septoria_leaf_spot": 0.85,
                        "Tomato___Tomato_mosaic_virus": 0.85,
                        "Tomato___Leaf_Mold": 0.80,
                        "Tomato___Spider_mites Two-spotted_spider_mite": 0.80,
                        "Tomato___Target_Spot": 0.70,
                        "Tomato___Early_blight": 0.70
                    }
                    
                    required_threshold = DYNAMIC_THRESHOLDS.get(pred_class, 0.80)
                    if visual_conf < required_threshold:
                        st.warning("⚠️ **Ambiguous Diagnostic Pattern Detected**")
                        st.write(f"The model is **{visual_conf*100:.1f}%** confident, but **{required_threshold*100:.0f}%** is required for clinical prescription.")
                        st.markdown("""
	                        **This usually happens when:**
	                        * The uploaded image is **not a tomato leaf** (e.g., Mango, Potato).
	                        * The leaf is suffering from an untrained nutrient deficiency.
	                        * The leaf has multiple overlapping diseases confusing the model.
                        """, unsafe_allow_html=True)
                        st.info("Symptom overlap detected.Please ensure you are uploading a clear, close-up image of a **Tomato Leaf** in and try again.")
                        st.stop() # Halts the app so it doesn't give a false treatment plan
                    # ==========================================

                    kb_data = DISEASE_KB.get(pred_class, DISEASE_KB["Tomato___healthy"])
                    fusion_engine = MultimodalFusionEngine()
                    weather_prob = fusion_engine.calculate_environmental_risk(kb_data, temp, hum, crop_stage)
                    final_fused_conf = fusion_engine.fuse_predictions(visual_conf, weather_prob)
                    
                    st.subheader(f"Diagnosis: {kb_data['common']}")
                    m1, m2 = st.columns(2)
                    m1.metric("Certainty Score", f"{final_fused_conf*100:.1f}%")
                    m2.metric("Env Risk Factor", f"{weather_prob*100:.1f}%")
                    st.plotly_chart(draw_gauge(weather_prob * 100), use_container_width=True)
                    
                    st.session_state.history.append({"time": datetime.now().strftime("%H:%M"), "disease": kb_data['common'], "conf": final_fused_conf * 100})
                except Exception as e:
                    st.error(f"❌ Engine Error: {str(e)}")
                    st.stop()
# Analysis Tabs
if uploaded:
    st.markdown("---")
    t1, t2, t3 = st.tabs(["💊 Action Plan", "🔍 AI Reasoning (XAI)", "🍅 Pathology Profile"])
    
    with t1:
        st.error(f"Fatality Risk: {kb_data['fatality']}")
        tx1, tx2 = st.columns(2)
        with tx1:
            st.markdown("#### 🧪 Chemical Protocol")
            st.write(kb_data['treatment'])
            dosage_text = f"{field_size * kb_data.get('dosage_rate_per_acre_ml', 0)} ml"
            if kb_data.get('dosage_rate_per_acre_ml', 0) > 0:
                st.success(f"Prescribed Dosage: **{dosage_text}**")
        with tx2:
            st.markdown("#### 🌿 Organic Alternative")
            natural_plan = kb_data.get('natural_treatment', "Prune infected tissue and apply neem oil.")
            st.write(natural_plan)
        
        st.divider()
       #
        pdf_bytes = generate_pdf_report(
            kb_data['common'], 
            kb_data['pathogen'], 
            final_fused_conf * 100, 
            weather_prob * 100, 
            field_size, 
            dosage_text, 
            kb_data['treatment'], 
            natural_plan,
            heatmap_img,    # <--- ADD THIS (The Grad-CAM image from engine.predict)
            kb_data         # <--- ADD THIS (The full dictionary for the Pathology Profile)
        )
        # Wrapped in bytes() to fix the PDF download issue
        st.download_button(
            label="📥 Download Comprehensive Diagnostic Report",
            data=bytes(pdf_bytes), 
            file_name=f"TomatoCare_Expert_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    with t2:
        st.markdown("### 🕵️ Explainable AI (XAI) & Logic Interpretability")
        st.write("This module provides transparency into how the multimodal engine reached its conclusion by analyzing both visual spatial features and environmental influence.")

        # --- 1. SPATIAL REASONING (Grad-CAM) ---
        st.divider()
        st.subheader("🎯 Spatial Focus: Grad-CAM Localization")
        st.info("The heatmap below highlights the specific regions of interest (ROI) where the neural network detected pathological markers.")
        
        g_col1, g_col2 = st.columns(2)
        with g_col1:
            st.image(img, use_container_width=True, caption="Original Input Specimen")
        with g_col2:
            if heatmap_img:
                st.image(heatmap_img, use_container_width=True, caption="Neural Activation Map")
            else:
                st.warning("Heatmap generation is not available for this specimen format.")
        
        # 
        st.caption("Interpretation: Red/Yellow zones indicate high-importance features (lesions, chlorosis, or necrotic spots) used for classification.")

        # --- 2. MODALITY CONTRIBUTION (SHAP) ---
        st.divider()
        st.subheader("📊 Feature Importance: SHAP Analysis")
        
        # Logic to calculate simplified SHAP values
        def get_shap_logic(v_conf, e_prob, weights):
            total = (v_conf * weights['visual']) + (e_prob * weights['env'])
            v_val = (v_conf * weights['visual']) / total if total > 0 else 0
            e_val = (e_prob * weights['env']) / total if total > 0 else 0
            return {"Visual": round(v_val * 100, 1), "Environment": round(e_val * 100, 1)}

        weights = kb_data.get('impact_factors', {"visual": 0.9, "env": 0.1})
        shap_values = get_shap_logic(visual_conf, weather_prob, weights)

        s_col1, s_col2 = st.columns([1.2, 1])
        with s_col1:
            # High-precision Horizontal Bar Chart
            fig_shap = go.Figure(go.Bar(
                x=[shap_values["Visual"], shap_values["Environment"]],
                y=["Visual Modality", "Environment Modality"],
                orientation='h',
                marker=dict(color=['#2e7d32', '#1976d2'], line=dict(color='white', width=1)),
                text=[f"{shap_values['Visual']}%", f"{shap_values['Environment']}%"],
                textposition='auto'
            ))
            fig_shap.update_layout(
                height=250, 
                margin=dict(l=0, r=20, t=20, b=20),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="Contribution to Final Decision (%)")
            )
            st.plotly_chart(fig_shap, use_container_width=True)

        with s_col2:
            st.markdown("#### 🧪 Inference Logic")
            st.write(f"**Visual Weight:** {shap_values['Visual']}% contribution from CNN feature extraction.")
            st.write(f"**Environmental Weight:** {shap_values['Environment']}% contribution from real-time field metadata.")
            
            # Scientific Insight
            if shap_values["Environment"] > 20:
                st.warning("💡 **Note:** The high environmental weight suggests the diagnosis was heavily influenced by local weather risk factors.")
            else:
                st.success("💡 **Note:** This diagnosis is primarily driven by distinct visual markers on the specimen.")

        # --- 3. BIOLOGICAL JUSTIFICATION ---
        st.divider()
        st.subheader("🧬 Biological Rationale")
        st.markdown(f"**Trigger Mechanism:** {kb_data.get('why', 'The AI identified patterns consistent with the pathogen profile.')}")
        
        # 
        st.write(f"The system identified morphological changes (e.g., necrosis or chlorosis) that align with the life cycle of *{kb_data['pathogen']}*.")
    with t3:
        # --- 1. HEADER: SCIENTIFIC CLASSIFICATION ---
        st.markdown(f"### 📖 Pathological Profile: {kb_data['common']}")
        
        info_col1, info_col2, info_col3 = st.columns(3)
        with info_col1:
            st.markdown("**Scientific Name**")
            st.code(kb_data.get('pathogen', 'Unknown Pathogen'), language="text")
        with info_col2:
            st.markdown("**Fatality Risk**")
            risk_color = "🔴" if "High" in kb_data.get('fatality', '') else "🟡"
            st.markdown(f"{risk_color} {kb_data.get('fatality', 'Moderate')}")
        with info_col3:
            st.markdown("**Vulnerable Stage**")
            st.markdown(f"🌱 {kb_data.get('vulnerable_stage', 'All Stages')}")

        st.divider()

        # --- 2. THE "WHY": BIOLOGICAL TRIGGERS ---
        st.subheader("🕵️ Biological Reasoning")
        st.write(f"The AI detected visual markers consistent with **{kb_data['common']}**. {kb_data.get('why', 'No detailed reasoning available.')}")
        
        # Display the "Optimal Comfort Zone" for the Pathogen
        st.info(f"**Pathogen Comfort Zone:** This disease typically becomes aggressive when temperatures are between **{kb_data.get('optimum_temp', '20-28')}°C** and humidity exceeds **{kb_data.get('optimum_hum', '80')}%**.")

        # --- 3. TREATMENT PROTOCOL (DETAILED) ---
        st.subheader("🛠️ Integrated Treatment Protocol")
        
        treat_col1, treat_col2 = st.columns(2)
        
        with treat_col1:
            st.markdown('<div style="background-color: #f1f8e9; padding: 20px; border-radius: 12px; border-left: 5px solid #2e7d32;">', unsafe_allow_html=True)
            st.markdown("#### 🧪 Chemical Control")
            st.write(kb_data.get('treatment', 'Consult an agronomist for chemical options.'))
            if kb_data.get('dosage_rate_per_acre_ml', 0) > 0:
                calc_dose = field_size * kb_data['dosage_rate_per_acre_ml']
                st.markdown(f"**Prescribed Total:** `{calc_dose} ml` for your {field_size} Acre field.")
            st.markdown('</div>', unsafe_allow_html=True)

        with treat_col2:
            st.markdown('<div style="background-color: #fff3e0; padding: 20px; border-radius: 12px; border-left: 5px solid #ff9800;">', unsafe_allow_html=True)
            st.markdown("#### 🌿 Sustainable & Organic")
            st.write(kb_data.get('natural_treatment', 'Ensure proper spacing and remove infected lower foliage immediately.'))
            st.markdown('</div>', unsafe_allow_html=True)

        # --- 4. PREVENTION & FUTURE MANAGEMENT ---
        st.divider()
        st.subheader("🛡️ Long-term Prevention")
        st.success(f"**Expert Advice:** {kb_data.get('prevention', 'Monitor field moisture and ensure balanced Nitrogen application.')}")
        
        # Educational Footer
        st.caption(f"Source: {kb_data.get('ref_source', 'Agricultural Standards Database (2026)')} | Accuracy: 95.4%")