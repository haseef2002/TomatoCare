import streamlit as st
import sys
import os


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

st.set_page_config(page_title="Encyclopedia | TomatoCare", page_icon="🍅", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .encyclopedia-card { background: white; padding: 30px; border-radius: 15px; border-top: 8px solid #2e7d32; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🍅 Tomato Pathology Encyclopedia")
st.write("A verified scientific database of the 10 target classes identified by the TomatoCare Engine.")

# Disease Selection
selected_disease = st.selectbox("Select a Pathology to View Details:", 
                                list(DISEASE_KB.keys()), 
                                format_func=lambda x: DISEASE_KB[x]['common'])

data = DISEASE_KB[selected_disease]

# Content Display
st.markdown('<div class="encyclopedia-card">', unsafe_allow_html=True)
col_a, col_b = st.columns([1, 2])

with col_a:
    # Attempt to load a sample reference image from the project data
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    image_path = os.path.join(base_dir, 'data', 'samples', 'test_images', f"{selected_disease}.jpg")
    
    if os.path.exists(image_path):
        st.image(image_path, caption=f"Typical presentation of {data['common']}", use_container_width=True)
    else:
        st.info("📸 Reference image currently undergoing verification.")

with col_b:
    st.subheader(data['common'])
    st.write(f"**Scientific Pathogen:** *{data['pathogen']}*")
    st.write(f"**Primary Biological Trigger:** {data['why']}")
    
    st.divider()
    
    # Grid for vulnerability and prevention
    grid1, grid2 = st.columns(2)
    grid1.markdown(f"**Vulnerable Growth Stage:**\n{data['vulnerable_stage']}")
    grid2.markdown(f"**Pathogen Fatality Risk:**\n{data['fatality']}")
    
    st.markdown(f"**Prevention Strategy:**\n{data['prevention']}")
    
    # Environmental High-Risk parameters
    h_temp = data['risk_params']['temp']
    h_hum = data['risk_params']['hum']
    hum_str = f"{h_hum[0]}% - {h_hum[1]}%" if isinstance(h_hum, tuple) else f"> {h_hum}%"
    
    st.warning(f"🌡️ **Critical Environment:** High spread likely between {h_temp[0]}°C - {h_temp[1]}°C and Humidity {hum_str}.")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation Footer
st.divider()
st.caption("All data is derived from verified phytopathology sources. Refer to the 'Scientific References' module for official documentation.")