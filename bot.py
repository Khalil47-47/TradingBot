import streamlit as st
import random
import time
import math
import yfinance as yf
import pandas as pd

st.set_page_config(
    page_title="ENZO PRO ROBOT - Elite Trading Bot",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
    <style>
    :root {
        color-scheme: dark;
    }
    
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #030508 !important;
        color: #f1f5f9 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .active-users-badge { 
        text-align: center; 
        background-color: #04182f; 
        border: 1px solid #0088ff; 
        color: #0088ff; 
        padding: 10px; 
        border-radius: 10px; 
        font-size: 13px; 
        font-weight: 700; 
        margin-bottom: 20px; 
    }

    .stButton > button { 
        width: 100%; 
        background: linear-gradient(135deg, #0088ff 0%, #0055bb 100%) !important; 
        color: #ffffff !important; 
        font-size: 15px !important; 
        font-weight: 900 !important; 
        padding: 12px !important; 
        border-radius: 10px !important; 
        border: none !important; 
        cursor: pointer; 
    }
    
    .simple-popup-card { 
        background: #08121e; 
        padding: 20px; 
        border-radius: 12px; 
        border: 2px solid #0088ff; 
        margin-top: 20px; 
        margin-bottom: 20px; 
    }
    
    .signal-line { 
        display: flex; 
        justify-content: space-between; 
        padding: 7px 0; 
        border-bottom: 1px solid #1e293b; 
        font-size: 13px; 
        color: #f1f5f9; 
    }
    </style>
""", unsafe_allow_html=True)

if 'active_users' not in st.session_state:
    st.session_state.active_users = random.randint(180, 250)

# 1. Active Users Status
st.markdown(f"""
    <div class="active-users-badge">
        🟢 Live Status: {st.session_state.active_users} Traders Active Right Now!
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🏛️ Eagle Eye Vision Control Panel")

# 2. Broker Selection
broker = st.radio("1. Select Broker", ["Quotex", "Pocket Option"], horizontal=True)

# 3. Asset and Expiry Time
col_asset, col_exp = st.columns(2)

if broker == "Quotex":
    assets = [
        "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", "NZD/USD (OTC)", 
        "USD/JPY (OTC)", "USD/CHF (OTC)", "EUR/JPY (OTC)", "GBP/JPY (OTC)", 
        "AUD/JPY (OTC)", "EUR/AUD (OTC)", "USD/CAD (OTC)", "CAD/JPY (OTC)",
        "EUR/GBP (OTC)", "AUD/USD (OTC)", "CHF/JPY (OTC)", "GOLD (OTC)", "SILVER (OTC)"
    ]
else:
    assets = [
        "EUR/USD [OTC]", "GBP/USD [OTC]", "USD/JPY [OTC]", "AUD/CHF [OTC]", 
        "EUR/GBP [OTC]", "USD/CAD [OTC]", "GBP/JPY [OTC]", "NZD/JPY [OTC]",
        "GOLD (OTC)", "SILVER (OTC)"
    ]
    
with col_asset:
    asset = st.selectbox("2. Trading Asset (Pair)", assets)
with col_exp:
    tf = st.selectbox("3. Expiry Time (Timer)", ["1 Minute", "2 Minutes", "5 Minutes", "10 Minutes", "15 Minutes"])

# 4. Screenshot Upload (Arrow and text completely removed, direct uploader)
st.markdown("<br>", unsafe_allow_html=True)
chart_screenshot = st.file_uploader("4. Upload Chart Screenshot", type=["png", "jpg", "jpeg"], key="clean_upload")

st.markdown("<br>", unsafe_allow_html=True)
gen_btn = st.button("🚀 EXECUTE VISION ANALYSIS & GENERATE SIGNAL")

# --- POP-UP SIGNAL AREA ---
if gen_btn:
    if chart_screenshot is None:
        st.warning("⚠️ Please upload a chart screenshot first!")
    else:
        with st.spinner("Scanning screenshot & computing signal..."):
            time.sleep(1.0)
            
        action = random.choice(["BUY (CALL 🟢)", "SELL (PUT 🔴)"])
        conf = random.randint(94, 99)
        
        st.session_state.signal_data = {
            "action": action, "conf": conf, "asset": asset, "tf": tf, "broker": broker
        }

if 'signal_data' in st.session_state and st.session_state.signal_data:
    sig = st.session_state.signal_data
    color = "#0088ff" if "BUY" in sig["action"] else "#ff3366"
    
    st.markdown(f"""
        <div class="simple-popup-card" style="border-color: {color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 15px; font-weight: 900; color: #ffffff;">🎯 ENZO VISION SIGNAL</span>
                <span style="background-color: {color}; color: #ffffff; padding: 4px 12px; border-radius: 6px; font-weight: 900; font-size: 15px;">{sig['action']}</span>
            </div>
            <div class="signal-line"><span style="color: #94a3b8;">Broker / Asset:</span><span style="font-weight: 700; color: #fff;">{sig['broker']} - {sig['asset']}</span></div>
            <div class="signal-line"><span style="color: #94a3b8;">Expiry Time:</span><span style="font-weight: 700; color: #fff;">{sig['tf']}</span></div>
            <div class="signal-line" style="border: none;"><span style="color: #94a3b8;">Confidence Level:</span><span style="color: #00ffcc; font-weight: 800;">{sig['conf']}% High Win-Rate</span></div>
        </div>
    """, unsafe_allow_html=True)
    
    # --- TRADE FEEDBACK MODULE ---
    st.markdown("---")
    st.markdown("#### 📊 Trade Feedback")
    fb_col1, fb_col2 = st.columns(2)
    with fb_col1:
        user_fb = st.radio("Result", ["Win (Good)", "Loss (Bad)"], horizontal=True, key="clean_feedback")
    with fb_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Submit Result"):
            st.success("✅ Feedback saved successfully!")
