import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
st.set_page_config(page_title="Farm Analytics | TomatoCare", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .status-card { background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px; border-left: 6px solid #2e7d32; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Farm Health Analytics")
st.markdown("### 30-Day Pathogen Prevalence & Trend Monitoring")

# Generate Mock Historical Data (Replace with DB queries for production)
np.random.seed(42)
dates_30 = [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(30)][::-1]

# Simulated scan counts
healthy_trend = np.random.poisson(lam=4, size=30)
blight_trend = np.random.poisson(lam=1, size=30)
# Adding a simulated spike for insight
blight_trend[20:25] += 5 

# Trend Visualization
fig_trends = go.Figure()
fig_trends.add_trace(go.Scatter(x=dates_30, y=healthy_trend, mode='lines', fill='tozeroy', 
                                 name="Healthy Crops", line=dict(color="#2ecc71", width=3)))
fig_trends.add_trace(go.Scatter(x=dates_30, y=blight_trend, mode='lines+markers', 
                                 name="Disease Outbreaks", line=dict(color="#e74c3c", width=3)))

fig_trends.update_layout(
    xaxis_title="Timeline",
    yaxis_title="Total Scans",
    hovermode="x unified",
    height=450,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig_trends, use_container_width=True)

# Analytical Insight Card
st.info("💡 **AI Analytical Insight:** Disease detection frequency increased by **25%** following recent localized precipitation. Cross-reference with the 7-Day Forecast to adjust preventative fungicide schedules.")

st.divider()

# Performance Metrics
st.subheader("📋 Monthly Performance Summary")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.metric("Total Scans (30d)", int(sum(healthy_trend) + sum(blight_trend)))
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.metric("Top Threat", "Early Blight", delta="High Risk", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.metric("Overall Farm Health", "78%", delta="+3% vs last month")
    st.markdown('</div>', unsafe_allow_html=True)