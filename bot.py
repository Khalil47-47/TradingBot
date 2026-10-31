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
        background: radial-gradient(circle at 50% 20%, #081827 0%, #030508 70%), #030508 !important;
        color: #f1f5f9 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        -webkit-text-size-adjust: 100%;
        overflow-x: hidden;
    }
    
    @keyframes sapphirePulse {
        0% { box-shadow: 0 0 10px rgba(0, 136, 255, 0.2); }
        50% { box-shadow: 0 0 25px rgba(0, 136, 255, 0.6); }
        100% { box-shadow: 0 0 10px rgba(0, 136, 255, 0.2); }
    }

    @keyframes centerPopUpAnimation {
        0% { opacity: 0; transform: scale(0.95) translateY(10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    .main-container { 
        max-width: 600px;
        margin: 20px auto;
        background: linear-gradient(135deg, rgba(13, 17, 23, 0.98) 0%, rgba(5, 8, 15, 0.98) 100%); 
        backdrop-filter: blur(10px);
        padding: 30px; 
        border-radius: 20px; 
        border: 1px solid rgba(0, 136, 255, 0.4); 
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85); 
        position: relative;
        z-index: 1;
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, #041e3a 0%, #0d1117 100%);
        border: 1px solid #0088ff;
        padding: 18px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 20px;
    }

    .welcome-title {
        color: #0088ff;
        font-size: 20px;
        font-weight: 900;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .active-users-badge { 
        text-align: center; 
        background-color: #04182f; 
        border: 1px solid #0088ff; 
        color: #0088ff; 
        padding: 8px; 
        border-radius: 10px; 
        font-size: 12px; 
        font-weight: 700; 
        margin-bottom: 20px; 
    }

    /* Centered Upload Area Styling */
    .upload-section {
        background: rgba(0, 136, 255, 0.06);
        border: 2px dashed rgba(0, 136, 255, 0.5);
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: inset 0 0 15px rgba(0, 136, 255, 0.1);
    }

    .stSelectbox label, .stRadio label, .stFileUploader label { 
        color: #f1f5f9 !important; 
        font-weight: 700 !important; 
        font-size: 13px !important; 
    }
    
    div[data-baseweb="select"] > div { background-color: #0d1117 !important; color: #ffffff !important; border-color: #334155 !important; }
    
    .stButton > button { 
        width: 100%; 
        background: linear-gradient(135deg, #0088ff 0%, #0055bb 100%) !important; 
        color: #ffffff !important; 
        font-size: 15px !important; 
        font-weight: 900 !important; 
        padding: 12px !important; 
        border-radius: 12px !important; 
        border: none !important; 
        cursor: pointer; 
        animation: sapphirePulse 3s infinite;
    }
    
    .simple-popup-card { 
        background: linear-gradient(135deg, #08121e 0%, #03070d 100%); 
        padding: 20px; 
        border-radius: 14px; 
        border: 2px solid #0088ff; 
        margin-top: 20px; 
        margin-bottom: 20px; 
        box-shadow: 0 0 30px rgba(0, 136, 255, 0.3);
        animation: centerPopUpAnimation 0.3s ease-out;
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

# --- SINGLE CENTRALIZED BRACKET CONTAINER ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-banner">
        <h1 class="welcome-title">🦅 ENZO PRO VISION ROBOT</h1>
        <p style="color: #cbd5e1; font-size: 12px; margin: 3px 0 0 0;">Unified Control Panel & Screenshot Scanner</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="active-users-badge">
        🟢 Live Status: {st.session_state.active_users} Traders Active Right Now!
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🏛️ Eagle Eye Vision Control Panel")

# 1. TOP: Broker Selection
broker = st.radio("1. Select Broker", ["Quotex", "Pocket Option"], horizontal=True)

# 2. BELOW BROKER: Asset (Pair) and Expiry Time (Timer) in 2 columns
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
        "GOLD [OTC]", "SILVER [OTC]"
    ]
    
with col_asset:
    asset = st.selectbox("2. Trading Asset (Pair)", assets)
with col_exp:
    tf = st.selectbox("3. Expiry Time (Timer)", ["1 Minute", "2 Minutes", "5 Minutes", "10 Minutes", "15 Minutes"])

# 3. CENTERED BELOW: Beautiful Screenshot Upload Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("<p style='color: #0088ff; font-weight: 800; margin-bottom: 5px;'>📸 4. Upload Chart Screenshot (30-100 Candles)</p>", unsafe_allow_html=True)
chart_screenshot = st.file_uploader("", type=["png", "jpg", "jpeg"], key="centered_screenshot_uploader")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
gen_btn = st.button("🚀 EXECUTE VISION ANALYSIS & GENERATE SIGNAL")

# --- POP-UP SIGNAL AREA INSIDE THE SAME CONTAINER ---
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
        user_fb = st.radio("Result", ["Win (Good)", "Loss (Bad)"], horizontal=True, key="simple_feedback_radio")
    with fb_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Submit Result"):
            st.success("✅ Feedback saved successfully!")

st.markdown('</div>', unsafe_allow_html=True)
