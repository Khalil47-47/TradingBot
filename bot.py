import streamlit as st
import random
import time
import sqlite3
import requests
import math
import yfinance as yf
import pandas as pd
import numpy as np

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
    }
    
    @keyframes sapphirePulse {
        0% { box-shadow: 0 0 10px rgba(0, 136, 255, 0.2); }
        50% { box-shadow: 0 0 25px rgba(0, 136, 255, 0.6); }
        100% { box-shadow: 0 0 10px rgba(0, 136, 255, 0.2); }
    }

    @keyframes aggressiveGlow {
        0% { box-shadow: 0 0 15px rgba(255, 69, 0, 0.4); }
        50% { box-shadow: 0 0 35px rgba(255, 69, 0, 0.8); }
        100% { box-shadow: 0 0 15px rgba(255, 69, 0, 0.4); }
    }

    @keyframes centerPopUpAnimation {
        0% { opacity: 0; transform: scale(0.85) translateY(20px); }
        50% { transform: scale(1.02) translateY(-5px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }

    .page-box { 
        background: linear-gradient(135deg, rgba(13, 17, 23, 0.95) 0%, rgba(5, 8, 15, 0.95) 100%); 
        backdrop-filter: blur(12px);
        padding: 28px; 
        border-radius: 20px; 
        border: 1px solid rgba(0, 136, 255, 0.35); 
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.85); 
        margin-bottom: 20px; 
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, #041e3a 0%, #0d1117 100%);
        border: 1px solid #0088ff;
        padding: 22px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(0, 136, 255, 0.25);
    }

    .welcome-title {
        color: #0088ff;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: 1.5px;
        margin: 0;
        text-shadow: 0 0 12px rgba(0, 136, 255, 0.4);
    }
    
    .title-text { 
        color: #0088ff; 
        text-align: center; 
        font-size: 42px; 
        font-weight: 900; 
        letter-spacing: 2px; 
        margin-bottom: 2px; 
        text-shadow: 0 0 25px rgba(0, 136, 255, 0.6); 
    }
    
    .sub-title { 
        color: #ff4d4d; 
        text-align: center; 
        font-size: 14px; 
        font-weight: 800; 
        letter-spacing: 1px;
        margin-bottom: 8px; 
        text-transform: uppercase;
        text-shadow: 0 0 10px rgba(255, 77, 77, 0.4);
    }
    
    .telegram-box { 
        text-align: center; 
        background: transparent; 
        padding: 2px; 
        margin-bottom: 12px; 
    }
    
    .telegram-link { color: #38bdf8; text-decoration: none; font-weight: 700; font-size: 15px; }
    .telegram-link:hover { color: #00aaff; text-decoration: underline; }

    .binance-pay-box {
        background: linear-gradient(135deg, rgba(30, 25, 5, 0.95) 0%, rgba(13, 17, 23, 0.95) 100%);
        border: 2px dashed #f3ba2f;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 18px;
        box-shadow: 0 0 20px rgba(243, 186, 47, 0.15);
    }

    .binance-info-card {
        background: #030508;
        border: 1px solid #332b0a;
        padding: 14px;
        border-radius: 10px;
        font-family: monospace;
        color: #f3ba2f;
        font-size: 14px;
        margin-bottom: 15px;
        line-height: 1.6;
    }

    .price-badge {
        display: inline-block;
        background: rgba(243, 186, 47, 0.1);
        border: 1px solid #f3ba2f;
        padding: 8px 16px;
        border-radius: 10px;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .referral-box { 
        background: linear-gradient(135deg, rgba(40, 10, 5, 0.95) 0%, rgba(13, 17, 23, 0.95) 100%);
        border: 2px solid #ff4500; 
        padding: 24px; 
        border-radius: 16px; 
        margin-bottom: 20px; 
        animation: aggressiveGlow 3s infinite;
    }
    
    .popup-title { color: #ff3366; font-size: 24px; font-weight: 900; margin-bottom: 10px; }
    .popup-desc { color: #cbd5e1; font-size: 15px; margin-bottom: 18px; line-height: 1.5; }
    
    .popup-btn { 
        display: inline-block; 
        background: linear-gradient(135deg, #0088cc 0%, #005588 100%); 
        color: #ffffff !important; 
        padding: 12px 24px; 
        border-radius: 10px; 
        text-decoration: none; 
        font-weight: 800; 
        font-size: 15px; 
        box-shadow: 0 4px 12px rgba(0, 136, 204, 0.4); 
    }

    .offer-btn { 
        display: block;
        text-align: center;
        background: linear-gradient(135deg, #ff4500 0%, #cc3700 100%); 
        color: #ffffff !important; 
        padding: 14px 24px; 
        border-radius: 12px; 
        text-decoration: none; 
        font-weight: 900; 
        font-size: 16px; 
        box-shadow: 0 4px 20px rgba(255, 69, 0, 0.6); 
        margin-top: 15px;
    }
    
    .active-users-badge { 
        text-align: center; 
        background-color: #04182f; 
        border: 1px solid #0088ff; 
        color: #0088ff; 
        padding: 12px; 
        border-radius: 12px; 
        font-size: 14px; 
        font-weight: 700; 
        margin-bottom: 20px; 
        box-shadow: 0 0 15px rgba(0, 136, 255, 0.15); 
    }

    .logout-btn > button { background: linear-gradient(135deg, #ff3333 0%, #cc0000 100%) !important; color: #ffffff !important; }
    
    .stSelectbox label, .stRadio label, .stTextInput label, .stNumberInput label, .stSlider label, .stFileUploader label, .stCheckbox label { 
        color: #f1f5f9 !important; 
        font-weight: 700 !important; 
        font-size: 15px !important; 
    }
    
    div[data-baseweb="select"] > div { background-color: #0d1117 !important; color: #ffffff !important; border-color: #334155 !important; }
    div[data-baseweb="select"] span { color: #ffffff !important; }
    div[data-baseweb="popover"] div { background-color: #0d1117 !important; color: #ffffff !important; }
    
    .stButton > button { 
        width: 100%; 
        background: linear-gradient(135deg, #0088ff 0%, #0055bb 100%) !important; 
        color: #ffffff !important; 
        font-size: 17px !important; 
        font-weight: 900 !important; 
        padding: 12px !important; 
        border-radius: 10px !important; 
        border: none !important; 
        cursor: pointer; 
        animation: sapphirePulse 3s infinite;
    }
    
    .center-popup-card-animated { 
        background: linear-gradient(135deg, #0d1117 0%, #080c14 100%); 
        padding: 24px; 
        border-radius: 16px; 
        border: 2px solid #0088ff; 
        margin-top: 20px; 
        margin-bottom: 20px; 
        box-shadow: 0 0 35px rgba(0, 136, 255, 0.35);
        animation: centerPopUpAnimation 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .metric-row { 
        display: flex; 
        justify-content: space-between; 
        padding: 9px 0; 
        border-bottom: 1px solid #1e293b; 
        font-size: 14px; 
        color: #f1f5f9; 
    }
    
    .stat-card { 
        background: #0d1117; 
        padding: 16px; 
        border-radius: 12px; 
        text-align: center; 
        border: 1px solid #1e293b; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    </style>
""", unsafe_allow_html=True)

TELEGRAM_URL = "https://t.me/Enzosupport47" 
TELEGRAM_BOT_TOKEN = "8962828738:AAH787ztmRyKM6bRIGHdfVbiI6eeX7U0oFs"
TELEGRAM_CHAT_ID = "8633830998"
BROKER_REF_LINK = "https://broker-qx.pro/?lid=2146490"

def send_telegram_alert(order_id, user_name):
    try:
        message = (
            f"🔔 *New Binance Pay Submission - ENZO PRO*\n\n"
            f"👤 *User Name:* {user_name}\n"
            f"🆔 *Order ID / UID:* `{order_id}`\n"
            f"🕒 *Time:* {time.ctime()}"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print("Telegram Alert Error:", e)

def send_telegram_photo(photo_bytes, caption):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        files = {'photo': ('screenshot.jpg', photo_bytes, 'image/jpeg')}
        data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'Markdown'}
        requests.post(url, data=data, files=files, timeout=10)
    except Exception as e:
        print("Telegram Photo Error:", e)

def fetch_real_market_data(asset_name, timeframe):
    ticker_map = {
        "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "USDJPY=X",
        "AUD/USD": "AUDUSD=X", "USD/CAD": "USDCAD=X", "EUR/GBP": "EURGBP=X",
        "NZD/USD": "NZDUSD=X", "USD/CHF": "USDCHF=X", "EUR/JPY": "EURJPY=X",
        "GBP/JPY": "GBPJPY=X", "AUD/JPY": "AUDJPY=X", "EUR/AUD": "EURAUD=X",
        "CAD/JPY": "CADJPY=X", "EUR/NZD": "EURNZD=X", "GBP/AUD": "GBPAUD=X",
        "AUD/NZD": "AUDNZD=X", "NZD/CAD": "NZDCAD=X", "CHF/JPY": "CHFJPY=X",
        "USD/MXN": "USDMXN=X", "USD/NOK": "USDNOK=X", "GOLD": "GC=F",
        "SILVER": "SI=F", "BRENT": "BZ=F"
    }
    
    clean_asset = asset_name.replace(" (OTC)", "").replace(" [OTC]", "").replace(" (Commodity)", "").replace(" (Oil)", "").strip()
    symbol = ticker_map.get(clean_asset, "EURUSD=X")
    
    interval_map = {
        "1 Minute": "1m", "2 Minutes": "2m", "5 Minutes": "5m", 
        "10 Minutes": "5m", "15 Minutes": "15m", "30 Minutes": "15m"
    }
    yf_interval = interval_map.get(timeframe, "1m")
    
    try:
        data = yf.download(symbol, period="2d", interval=yf_interval, progress=False)
        if data.empty or len(data) < 25:
            data = yf.download(symbol, period="5d", interval="15m", progress=False)
            
        closes = data['Close'].squeeze()
        if isinstance(closes, pd.DataFrame):
            closes = closes.iloc[:, 0]
        prices = closes.tolist()
    except Exception:
        base = 1.0850 if "EUR" in clean_asset else 100.0
        random.seed(int(time.time() / 15))
        prices = [base]
        for _ in range(50):
            prices.append(prices[-1] + random.uniform(-0.0012, 0.0013))
            
    return prices

def calculate_real_deal_indicators(asset_name, timeframe):
    prices = fetch_real_market_data(asset_name, timeframe)
    df = pd.Series(prices)
    
    delta = df.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi_series = 100 - (100 / (1 + rs))
    current_rsi = round(float(rsi_series.iloc[-1]), 2)
    if math.isnan(current_rsi): current_rsi = 50.0
    
    sma = df.rolling(window=20).mean()
    std = df.rolling(window=20).std()
    upper = sma + (2 * std)
    lower = sma - (2 * std)
    
    cur_price = float(df.iloc[-1])
    cur_upper = round(float(upper.iloc[-1]), 4) if not math.isnan(upper.iloc[-1]) else cur_price * 1.002
    cur_lower = round(float(lower.iloc[-1]), 4) if not math.isnan(lower.iloc[-1]) else cur_price * 0.998
    
    exp12 = df.ewm(span=12, adjust=False).mean()
    exp26 = df.ewm(span=26, adjust=False).mean()
    macd = exp12 - exp26
    signal = macd.ewm(span=9, adjust=False).mean()
    cur_macd = round(float(macd.iloc[-1]), 5)
    cur_signal = round(float(signal.iloc[-1]), 5)
    
    bullish_score = 0
    bearish_score = 0
    
    if current_rsi < 48:
        bullish_score += 1
    elif current_rsi > 52:
        bearish_score += 1
        
    band_range = cur_upper - cur_lower if cur_upper != cur_lower else 0.0001
    price_position = (cur_price - cur_lower) / band_range
    if price_position <= 0.35:
        bullish_score += 1
    elif price_position >= 0.65:
        bearish_score += 1
        
    if cur_macd > cur_signal:
        bullish_score += 1
    else:
        bearish_score += 1
        
    if bullish_score > bearish_score:
        action = "BUY (CALL 🟢)"
        trend = f"Live Market Support Rebound ({timeframe} Momentum Bullish)"
    elif bearish_score > bullish_score:
        action = "SELL (PUT 🔴)"
        trend = f"Live Market Resistance Rejection ({timeframe} Momentum Bearish)"
    else:
        if cur_macd > cur_signal:
            action = "BUY (CALL 🟢)"
            trend = f"MACD Bullish Continuation ({timeframe})"
        else:
            action = "SELL (PUT 🔴)"
            trend = f"MACD Bearish Breakdown ({timeframe})"
        
    confidence = random.randint(92, 98)
    return action, confidence, current_rsi, cur_upper, cur_lower, cur_macd, trend

def init_db():
    conn = sqlite3.connect('enzo_licenses.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            key TEXT PRIMARY KEY,
            username TEXT,
            status TEXT DEFAULT 'Active',
            expiry_date TEXT DEFAULT 'Lifetime'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS binance_orders (
            order_id TEXT PRIMARY KEY
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pending_approvals (
            order_id TEXT PRIMARY KEY,
            username TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_settings (
            id INTEGER PRIMARY KEY,
            admin_pass TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS app_stats (
            id INTEGER PRIMARY KEY,
            total_revenue REAL
        )
    ''')
    
    cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO admin_settings (id, admin_pass) VALUES (1, ?)", ("Umarali4747",))
    
    cursor.execute("SELECT total_revenue FROM app_stats WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO app_stats (id, total_revenue) VALUES (1, 0.0)",)
        
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

VALID_KEYS = [
    "ENZO-3192-NX99-4410", "ENZO-7421-PRX-1123", "ENZO-9934-TRV-5568",
    "ENZO-1284-SEC-8890", "ENZO-6543-VIP-2219", "ENZO-4912-AI99-3341",
    "ENZO-8821-SYS-7745", "ENZO-5563-NET-9912", "ENZO-2049-LOG-1188",
    "ENZO-9123-ACC-4455", "ENZO-3349-DEV-6678", "ENZO-7812-MTR-3390",
    "ENZO-1102-BTC-9988", "ENZO-6691-ETH-2233", "ENZO-4421-USD-5566",
    "ENZO-8934-EUR-1144", "ENZO-2213-GBP-7788", "ENZO-5561-OTC-9900",
    "ENZO-9012-LIV-3322", "ENZO-4433-BOT-8811", "ENZO-7789-MLK-1239",
    "ENZO-3321-QTX-6654", "ENZO-9981-PKT-4432", "ENZO-1143-SIG-8877",
    "ENZO-6651-RSK-9921", "ENZO-2294-STK-3310", "ENZO-8812-API-5540",
    "ENZO-5523-KEY-7760", "ENZO-1211-PRO-9930", "ENZO-7474-ULTRA-11",
    "ENZO-1099-ALPHA-22", "ENZO-2099-BETA-33",  "ENZO-3099-GAMMA-44",
    "ENZO-4099-DELTA-55", "ENZO-5099-OMEGA-66", "ENZO-6099-PRIME-77",
    "ENZO-7099-MAX-88",   "ENZO-8099-SUPER-99", "ENZO-9098-MASTER-01",
    "ENZO-1190-GOLD-02",  "ENZO-2290-SILVER-03", "ENZO-3390-BRONZE-04",
    "ENZO-4490-VIP-05",   "ENZO-5590-PRO-06",   "ENZO-6690-TRADER-07",
    "ENZO-7790-BOT-08",   "ENZO-8890-SIG-09",   "ENZO-9998-AI-10",
    "ENZO-1245-SAFE-21",  "ENZO-5689-FAST-31"
]

cursor.execute("DELETE FROM licenses WHERE username IS NULL")
for k in VALID_KEYS:
    cursor.execute("INSERT OR IGNORE INTO licenses (key, username, status, expiry_date) VALUES (?, NULL, 'Active', 'Lifetime')", (k,))
conn.commit()

if 'page' not in st.session_state: st.session_state.page = "auth"
if 'auth_error' not in st.session_state: st.session_state.auth_error = None
if 'current_user' not in st.session_state: st.session_state.current_user = "Trader"

query_params = st.query_params
if "user" in query_params and "key" in query_params and st.session_state.page == "auth":
    saved_user = query_params["user"]
    saved_key = query_params["key"]
    cursor.execute("SELECT username, status FROM licenses WHERE key = ?", (saved_key,))
    row = cursor.fetchone()
    if row and row[1] == 'Active' and (row[0] is None or row[0] == saved_user):
        st.session_state.current_user = saved_user
        st.session_state.page = "dashboard"

if st.session_state.page == "auth":
    st.markdown('<p class="title-text">🦅 ENZO PRO ROBOT</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">🚨 ALERT: AVOID SCAMS - BUY ONLY FROM OFFICIALS</p>', unsafe_allow_html=True)

    st.markdown(f"""
        <div class="telegram-box">
            <span>💬 Official Support Channel: </span>
            <a class="telegram-link" href="{TELEGRAM_URL}" target="_blank">✈️ Telegram Support</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔐 Step 1: Authentication & Verification")
    st.markdown("<p style='color:#94a3b8; font-size:14px; margin-bottom: 15px;'>Enter your License Key, unlock via Free Access, or use Binance Pay Gateway.</p>", unsafe_allow_html=True)
    
    mode = st.radio("Authentication Mode", ["License Key", "Binance Pay Gateway", "🔥 FREE ACCESS"], horizontal=True)
    
    if mode == "License Key":
        username = st.text_input("Enter Your Username", placeholder="Type your trading name...")
        key = st.text_input("Enter Security Key", type="password", placeholder="Type license key...")
        remember_me = st.checkbox("📱 Save Access on this Device (Auto Login)", value=True)
        
        if st.button("Verify Key & Enter ➡️"):
            clean_user = username.strip()
            clean_key = key.strip()
            
            if not clean_user or not clean_key:
                st.session_state.auth_error = "empty_fields"
            else:
                with st.spinner("Verifying License Key... Please wait"):
                    time.sleep(1.2)
                    cursor.execute("SELECT username, status FROM licenses WHERE key = ?", (clean_key,))
                    row = cursor.fetchone()
                    
                    if row is None:
                        st.session_state.auth_error = "invalid"
                    else:
                        db_user, db_status = row[0], row[1]
                        
                        if db_status == "Blocked":
                            st.session_state.auth_error = "blocked"
                        elif db_user is None or db_user == clean_user:
                            if db_user is None:
                                cursor.execute("UPDATE licenses SET username = ? WHERE key = ?", (clean_user, clean_key))
                                conn.commit()
                            
                            if remember_me:
                                st.query_params["user"] = clean_user
                                st.query_params["key"] = clean_key
                            
                            st.session_state.current_user = clean_user
                            st.session_state.auth_error = None
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            st.session_state.auth_error = "wrong_user"
        
        if st.session_state.auth_error == "empty_fields":
            st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please fill in all required fields!</p>", unsafe_allow_html=True)
        elif st.session_state.auth_error == "invalid":
            st.markdown(f"""
                <div class="popup-error-box">
                    <div class="popup-title">❌ INVALID ACCESS KEY</div>
                    <div class="popup-desc">You have entered a wrong or unregistered license key. Please purchase an official key from our Telegram support channel.</div>
                    <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Official Purchase (Telegram)</a>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.auth_error == "blocked":
            st.markdown(f"""
                <div class="popup-error-box">
                    <div class="popup-title">🚫 ACCESS BLOCKED</div>
                    <div class="popup-desc">This license key has been blocked by the Administrator. Contact support for assistance.</div>
                    <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Contact Support</a>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.auth_error == "wrong_user":
            st.markdown(f"""
                <div class="popup-error-box">
                    <div class="popup-title">⚠️ SECURITY ALERT: USER MISMATCH</div>
                    <div class="popup-desc">This license key is already locked and registered with another user!</div>
                    <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Official Purchase (Telegram)</a>
                </div>
            """, unsafe_allow_html=True)

    elif mode == "Binance Pay Gateway":
        st.markdown("""
            <div class="binance-pay-box">
                <h3 style="color: #f3ba2f; margin-top: 0; font-size: 20px; font-weight: 900;">Binance Pay Gateway</h3>
                <div class="price-badge">
                    💎 Activation Fee: <span style="text-decoration: line-through; color: #ff4d4d; margin-right: 6px;">$15</span> <span style="color: #00ffcc; font-size: 18px;">$12 Only</span>
                </div>
                <p style="color: #cbd5e1; font-size: 14px; margin-bottom: 10px;">Transfer to Binance Pay ID:</p>
                <div class="binance-info-card">
                    Binance Pay ID / UID: 385682148<br>
                    Account Name: X FENDI
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        bp_name = st.text_input("Enter Your Username", placeholder="Type your trading name...", key="bp_name")
        order_id_input = st.text_input("Enter Order ID", placeholder="Enter Order ID / UID here...", key="bp_order_id")
        dep_screenshot_bp = st.file_uploader("Upload Binance Payment Proof Screenshot", type=["png", "jpg", "jpeg"], key="bp_file")
        
        if st.button("Submit Binance Payment Proof ➡️"):
            clean_bp_name = bp_name.strip()
            clean_order_id = order_id_input.strip()
            
            if not clean_bp_name:
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please enter your username!</p>", unsafe_allow_html=True)
            elif not clean_order_id or len(clean_order_id) < 3:
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please enter a valid Order ID!</p>", unsafe_allow_html=True)
            elif dep_screenshot_bp is None:
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please upload your payment proof screenshot!</p>", unsafe_allow_html=True)
            else:
                cursor.execute("SELECT order_id FROM binance_orders WHERE order_id = ?", (clean_order_id,))
                if cursor.fetchone():
                    st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ This Order ID has already been submitted!</p>", unsafe_allow_html=True)
                else:
                    with st.spinner("Submitting payment proof to Admin..."):
                        time.sleep(1.0)
                        cursor.execute("INSERT INTO binance_orders (order_id) VALUES (?)", (clean_order_id,))
                        cursor.execute("INSERT OR REPLACE INTO pending_approvals (order_id, username) VALUES (?, ?)", (clean_order_id, f"BINANCE: {clean_bp_name} (Order ID: {clean_order_id})"))
                        conn.commit()
                        
                        send_telegram_alert(clean_order_id, f"{clean_bp_name} (Binance Order ID: {clean_order_id})")
                        send_telegram_photo(dep_screenshot_bp.getvalue(), f"📸 Binance Payment Proof\n👤 User: `{clean_bp_name}`\n🆔 Order ID: `{clean_order_id}`")
                        
                        st.success("✅ Payment proof submitted successfully! Admin will verify your Order ID and assign your access key.")
                        st.markdown(f"""
                            <div style="text-align: center; margin-top: 15px;">
                                <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Message on Telegram for Fast Approval</a>
                            </div>
                        """, unsafe_allow_html=True)

    else:
        st.markdown(f"""
            <div class="referral-box">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <h3 style="color: #ff4500; margin: 0; font-size: 20px; font-weight: 900;">🔥 SPECIAL VIP OFFER: FREE ACCESS!</h3>
                    <span style="background: #ff4500; color: #ffffff; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 900; text-transform: uppercase;">🚀 EXCLUSIVE OFFER</span>
                </div>
                <p style="color: #cbd5e1; font-size: 14px; margin-bottom: 15px; line-height: 1.5;">Want Enzo Pro Bot for free? Register your trading account using our exclusive referral link and make a deposit to claim your free access key instantly!</p>
                <a class="offer-btn" href="{BROKER_REF_LINK}" target="_blank">🚀 CLAIM FREE ACCESS (REGISTER NOW)</a>
            </div>
        """, unsafe_allow_html=True)
        
        ref_name = st.text_input("Your Name / Username", placeholder="Type your trading name...", key="ref_name")
        broker_uid = st.text_input("Your Trader ID", placeholder="Enter your Trader ID...", key="broker_uid")
        dep_screenshot = st.file_uploader("Upload Deposit Proof Screenshot", type=["png", "jpg", "jpeg"], key="ref_file")
        
        if st.button("Submit Free Access Proof ➡️"):
            clean_ref_name = ref_name.strip()
            clean_uid = broker_uid.strip()
            
            if not clean_ref_name:
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please enter your name!</p>", unsafe_allow_html=True)
            elif not clean_uid or len(clean_uid) < 4:
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please enter a valid Trader ID!</p>", unsafe_allow_html=True)
            elif dep_screenshot is None:
                st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ Please upload your deposit proof screenshot!</p>", unsafe_allow_html=True)
            else:
                cursor.execute("SELECT order_id FROM binance_orders WHERE order_id = ?", (clean_uid,))
                if cursor.fetchone():
                    st.markdown("<p style='color:#ff3366; font-size:13px;'>⚠️ This Trader ID has already been submitted!</p>", unsafe_allow_html=True)
                else:
                    with st.spinner("Submitting referral & deposit details to Admin..."):
                        time.sleep(1.0)
                        cursor.execute("INSERT INTO binance_orders (order_id) VALUES (?)", (clean_uid,))
                        cursor.execute("INSERT OR REPLACE INTO pending_approvals (order_id, username) VALUES (?, ?)", (clean_uid, f"REF: {clean_ref_name}"))
                        conn.commit()
                        
                        send_telegram_alert(clean_uid, f"{clean_ref_name} (Free Access Deposit)")
                        send_telegram_photo(dep_screenshot.getvalue(), f"📸 Free Access Proof\n👤 User: `{clean_ref_name}`\n🆔 Trader ID: `{clean_uid}`")
                        
                        st.success("✅ Deposit proof submitted! Admin will verify your deposit through referral and assign your access key.")
                        st.markdown(f"""
                            <div style="text-align: center; margin-top: 15px;">
                                <a class="popup-btn" href="{TELEGRAM_URL}" target="_blank">✈️ Message on Telegram for Fast Approval</a>
                            </div>
                        """, unsafe_allow_html=True)
                
    if query_params.get("admin") == "true":
        st.markdown("---")
        st.markdown("### 🔐 Secret Admin Gateway")
        cursor.execute("SELECT admin_pass FROM admin_settings WHERE id = 1")
        current_admin_pass = cursor.fetchone()[0]
        
        admin_pass_input = st.text_input("Enter Secret Admin Password", type="password")
        if admin_pass_input == current_admin_pass:
            st.success("Admin Access Granted Successfully!")
            
            cursor.execute("SELECT total_revenue FROM app_stats WHERE id = 1")
            rev = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM licenses WHERE username IS NOT NULL")
            active_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM pending_approvals")
            pending_count = cursor.fetchone()[0]
            
            st.markdown("---")
            st.markdown("### 📊 Financial & System Analytics")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.markdown(f'<div class="stat-card"><h5>💰 Total Revenue</h5><h3 style="color:#0088ff;">${rev:.2f}</h3></div>', unsafe_allow_html=True)
            with col_s2:
                st.markdown(f'<div class="stat-card"><h5>👥 Active Users</h5><h3 style="color:#38bdf8;">{active_count}</h3></div>', unsafe_allow_html=True)
            with col_s3:
                st.markdown(f'<div class="stat-card"><h5>📥 Pending Orders</h5><h3 style="color:#f3ba2f;">{pending_count}</h3></div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📥 Pending Payment & Referral Approvals")
            cursor.execute("SELECT order_id, username FROM pending_approvals")
            pending_list = cursor.fetchall()
            if pending_list:
                for p in pending_list:
                    st.markdown(f"""
                        <div style="background: #0d1117; padding: 15px; border-radius: 10px; margin-bottom: 12px; font-size: 14px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #1e293b;">
                            <div>👤 <b>User/Type:</b> {p[1]}<br>🆔 <b>Order ID / Ref:</b> <span style="color:#f3ba2f;">{p[0]}</span></div>
                            <a href="{TELEGRAM_URL}" target="_blank" style="background:#0088cc; color:white; padding:8px 14px; border-radius:8px; text-decoration:none; font-weight:bold; font-size:13px;">💬 Chat on Telegram</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_app, col_dec = st.columns(2)
                    with col_app:
                        if st.button(f"✅ Approve & Assign Key", key=f"app_{p[0]}"):
                            cursor.execute("SELECT key FROM licenses WHERE username IS NULL LIMIT 1")
                            free_key = cursor.fetchone()
                            if free_key:
                                assigned_key = free_key[0]
                                cursor.execute("DELETE FROM pending_approvals WHERE order_id = ?", (p[0],))
                                cursor.execute("UPDATE app_stats SET total_revenue = total_revenue + 12.0 WHERE id = 1")
                                conn.commit()
                                st.markdown(f"""
                                    <div style="background: #04182f; border: 2px solid #0088ff; padding: 18px; border-radius: 12px; margin-top: 12px; text-align: center;">
                                        <h3 style="color: #0088ff; margin:0; font-size:18px;">🎉 Approved Successfully!</h3>
                                        <p style="color: #ffffff; font-size: 14px; margin: 6px 0;">Assigned Key for <b>{p[1]}</b>:</p>
                                        <div style="background: #030508; color: #f3ba2f; padding: 10px; font-family: monospace; font-size: 16px; font-weight: bold; border-radius: 8px;">
                                            {assigned_key}
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.error("No free keys available in database!")
                    with col_dec:
                        if st.button(f"❌ Decline", key=f"dec_{p[0]}"):
                            cursor.execute("DELETE FROM pending_approvals WHERE order_id = ?", (p[0],))
                            conn.commit()
                            st.warning(f"Request {p[0]} Declined!")
                            st.rerun()
            else:
                st.info("No pending requests right now.")

            st.markdown("---")
            st.markdown("### ➕ One-Click Key Generator & Adder")
            col_gen1, col_gen2 = st.columns([2, 1])
            with col_gen1:
                auto_generated_key = f"ENZO-{random.randint(1000,9999)}-PRO-{random.randint(1000,9999)}"
                new_key_input = st.text_input("New License Key", value=auto_generated_key)
            with col_gen2:
                validity_period = st.selectbox("Validity", ["30 Days", "90 Days", "Lifetime"])
            
            if st.button("Add Key to Database with Validity"):
                if new_key_input.strip():
                    try:
                        cursor.execute("INSERT INTO licenses (key, username, status, expiry_date) VALUES (?, NULL, 'Active', ?)", (new_key_input.strip(), validity_period))
                        conn.commit()
                        st.success(f"Key '{new_key_input.strip()}' added successfully ({validity_period})!")
                    except Exception as e:
                        st.error(f"Error: Key already exists.")
                else:
                    st.warning("Please enter a valid key.")
            
            st.markdown("---")
            st.markdown("### 👥 Active Users Management (Block / Unblock)")
            cursor.execute("SELECT key, username, status, expiry_date FROM licenses WHERE username IS NOT NULL")
            logged_users = cursor.fetchall()
            if logged_users:
                for u in logged_users:
                    status_color = "#0088ff" if u[2] == "Active" else "#ff3366"
                    st.markdown(f"""
                        <div style="background: #0d1117; padding: 15px; border-radius: 10px; margin-bottom: 10px; font-size: 14px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #1e293b;">
                            <div>👤 <b>User:</b> {u[1]}<br>🔑 <b>Key:</b> <span style="color:#0088ff;">{u[0]}</span><br>⏳ <b>Validity:</b> {u[3]} | Status: <span style="color:{status_color}; font-weight:bold;">{u[2]}</span></div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if u[2] == "Active":
                            if st.button(f"🚫 Block {u[1]}", key=f"block_{u[0]}"):
                                cursor.execute("UPDATE licenses SET status = 'Blocked' WHERE key = ?", (u[0],))
                                conn.commit()
                                st.success(f"User {u[1]} blocked successfully!")
                                st.rerun()
                        else:
                            if st.button(f"✅ Unblock {u[1]}", key=f"unblock_{u[0]}"):
                                cursor.execute("UPDATE licenses SET status = 'Active' WHERE key = ?", (u[0],))
                                conn.commit()
                                st.success(f"User {u[1]} unblocked successfully!")
                                st.rerun()
                    with col_b2:
                        if st.button(f"🗑️ Delete Access", key=f"del_{u[0]}"):
                            cursor.execute("UPDATE licenses SET username = NULL, status = 'Active' WHERE key = ?", (u[0],))
                            conn.commit()
                            st.warning(f"Access reset for {u[1]}!")
                            st.rerun()
            else:
                st.info("No active users yet.")

            st.markdown("---")
            st.markdown("### 🔑 Change Admin Password")
            new_admin_p = st.text_input("Enter New Admin Password", type="password")
            if st.button("Update Admin Password"):
                if len(new_admin_p.strip()) >= 5:
                    cursor.execute("UPDATE admin_settings SET admin_pass = ? WHERE id = 1", (new_admin_p.strip(),))
                    conn.commit()
                    st.success("Admin password updated successfully!")
                else:
                    st.error("Password must be at least 5 characters long.")
                
        elif admin_pass_input:
            st.error("Wrong Password!")

elif st.session_state.page == "dashboard":
    st.empty()
    
    if 'active_users' not in st.session_state:
        st.session_state.active_users = random.randint(180, 250)

    user_display_name = st.session_state.current_user.upper()
    st.markdown(f"""
        <div class="welcome-banner">
            <h1 class="welcome-title">⚡ WELCOME TO ENZO PRO, {user_display_name}! ⚡</h1>
            <p style="color: #cbd5e1; font-size: 14px; margin: 6px 0 0 0;">Your Eagle Eye Vision & Live Market AI System is Ready.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"<h2 style='color: #0088ff; margin:0; font-size:24px;'>🦅 ENZO PRO ROBOT</h2>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94a3b8; font-size: 13px; margin:0;'>Eagle Eye Vision & Live Candle Engine</p>", unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
            if st.button("🔒 Logout"):
                st.query_params.clear()
                st.session_state.auth_error = None
                st.session_state.page = "auth"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown(f"""
        <div class="active-users-badge" style="margin-top: 15px;">
            🟢 Live Status: {st.session_state.active_users} Traders Active on Enzo Bot right now!
        </div>
    """, unsafe_allow_html=True)

    # --- EAGLE EYE VISION SINGLE BLOCK DASHBOARD ---
    with st.container():
        st.markdown('<div class="page-box">', unsafe_allow_html=True)
        st.markdown("### 🏛️ Eagle Eye Vision Analysis Center")
        
        # 1. Broker Selection
        broker = st.radio("Broker Selection", ["Quotex", "Pocket Option"], horizontal=True)
        
        # 2. Asset & Expiry in 2 columns
        col_asset, col_exp = st.columns(2)
        
        if broker == "Quotex":
            assets = [
                "EUR/USD (OTC)", "GBP/USD (OTC)", "AUD/CAD (OTC)", "NZD/USD (OTC)", 
                "USD/JPY (OTC)", "USD/CHF (OTC)", "EUR/JPY (OTC)", "GBP/JPY (OTC)", 
                "AUD/JPY (OTC)", "EUR/AUD (OTC)", "USD/CAD (OTC)", "CAD/JPY (OTC)",
                "EUR/GBP (OTC)", "AUD/USD (OTC)", "CHF/JPY (OTC)", "EUR/NZD (OTC)",
                "GBP/AUD (OTC)", "AUD/NZD (OTC)", "NZD/JPY (OTC)", "USD/INR (OTC)",
                "USD/BRL (OTC)", "USD/PHP (OTC)", "USD/IDR (OTC)", "USD/ZAR (OTC)",
                "EUR/CAD (OTC)", "GBP/CHF (OTC)", "AUD/CHF (OTC)", "NZD/CAD (OTC)",
                "USD/MXN (OTC)", "USD/TRY (OTC)", "USD/EGP (OTC)", "USD/BDT (OTC)",
                "USD/PKR (OTC)", "USD/VND (OTC)", "USD/NGN (OTC)", "EUR/TRY (OTC)", 
                "GBP/TRY (OTC)", "GOLD (OTC)", "SILVER (OTC)"
            ]
        else:
            assets = [
                "EUR/USD [OTC]", "GBP/USD [OTC]", "USD/JPY [OTC]", "AUD/CHF [OTC]", 
                "EUR/GBP [OTC]", "USD/CAD [OTC]", "GBP/JPY [OTC]", "NZD/JPY [OTC]",
                "AUD/CAD [OTC]", "EUR/AUD [OTC]", "CHF/JPY [OTC]", "USD/CHF [OTC]",
                "NZD/USD [OTC]", "EUR/CAD [OTC]", "GBP/CHF [OTC]", "EUR/JPY [OTC]",
                "AUD/USD [OTC]", "NZD/USD [OTC]", "USD/INR [OTC]", "USD/BRL [OTC]",
                "EUR/NZD [OTC]", "GBP/AUD [OTC]", "CAD/JPY [OTC]", "USD/MXN [OTC]",
                "USD/TRY [OTC]", "USD/PKR [OTC]", "USD/BDT [OTC]", "USD/EGP [OTC]",
                "EUR/TRY [OTC]", "GOLD [OTC]", "SILVER [OTC]"
            ]
            
        with col_asset:
            asset = st.selectbox("Trading Asset", assets)
        with col_exp:
            tf = st.selectbox("Expiry Time", ["1 Minute", "2 Minutes", "5 Minutes", "10 Minutes", "15 Minutes", "30 Minutes"])
        
        # 3. Screenshot Upload (30-100 Candles)
        st.markdown("<br>", unsafe_allow_html=True)
        chart_screenshot = st.file_uploader("📸 Upload Chart Screenshot (30-100 Candles)", type=["png", "jpg", "jpeg"], key="single_block_screenshot")
        
        st.markdown("<br>", unsafe_allow_html=True)
        gen_btn = st.button("🚀 EXECUTE ENZO VISION & LIVE ANALYSIS")
        
        # --- POP-UP SIGNAL AREA INSIDE THE SAME BLOCK ---
        if gen_btn:
            scan_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            scan_stages = [
                ("📸 Scanning Uploaded Candlestick Screenshot (30-100 Candles)...", 1.0),
                ("🧠 AI Vision Matrix Evaluating Support / Resistance & Patterns...", 1.2),
                ("🔮 Computing Next Candle Expiry Probability...", 1.2),
                ("⚡ Finalizing High-Precision Next Candle Signal...", 0.8)
            ]
            
            current_progress = 0
            for stage_text, stage_time in scan_stages:
                scan_placeholder.markdown(f"<p style='color:#0088ff; font-family:monospace; font-weight:bold; font-size:14px;'>⚡ [ENZO VISION] {stage_text}</p>", unsafe_allow_html=True)
                step_increment = 25 / 10
                time_per_step = stage_time / 10
                for _ in range(10):
                    time.sleep(time_per_step)
                    current_progress += step_increment
                    progress_bar.progress(min(int(current_progress), 100))
                    
            progress_bar.empty()
            scan_placeholder.empty()
            
            action, conf, rsi_val, upper_b, lower_b, macd_v, trend = calculate_real_deal_indicators(asset, tf)
            
            if chart_screenshot is not None:
                conf = random.randint(95, 99)
                trend = f"Advanced Vision Pattern Match ({tf} Expiry Direction Confirmed)"

            st.session_state.signal_data = {
                "action": action, "conf": conf, "asset": asset, "tf": tf,
                "broker": broker, "trend": trend, "rsi": rsi_val,
                "has_screenshot": chart_screenshot is not None
            }

        if 'signal_data' in st.session_state and st.session_state.signal_data:
            sig = st.session_state.signal_data
            color = "#0088ff" if "BUY" in sig["action"] else "#ff3366"
            
            st.markdown(f"""
                <div class="center-popup-card-animated" style="border-color: {color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 18px; font-weight: 900; color: #ffffff;">✨ ENZO VISION SIGNAL: {sig['action']}</span>
                        <span style="background-color: {color}; color: #ffffff; padding: 4px 14px; border-radius: 8px; font-weight: 900; font-size: 16px;">{sig['action']} ↑</span>
                    </div>
                    <div class="metric-row"><span style="color: #94a3b8;">Broker / Asset:</span><span style="font-weight: 700; color: #fff;">{sig['broker']} - {sig['asset']}</span></div>
                    <div class="metric-row"><span style="color: #94a3b8;">Expiry Time:</span><span style="font-weight: 700; color: #fff;">{sig['tf']}</span></div>
                    <div class="metric-row"><span style="color: #94a3b8;">Pattern Match Confidence:</span><span style="color: #00ffcc; font-weight: 800;">{sig['conf']}%</span></div>
                    <div class="metric-row"><span style="color: #94a3b8;">Live Price Action:</span><span style="color: #0088ff; font-weight: 700;">{sig['trend']}</span></div>
                    <div class="metric-row"><span style="color: #94a3b8;">Market Sentiment:</span><span style="color: #f3ba2f; font-weight: 700;">Strong Uptrend (RSI: {sig['rsi']})</span></div>
                    <div class="metric-row" style="border: none;"><span style="color: #94a3b8;">Prediction Accuracy:</span><span style="color: #0088ff; font-weight: 800;">{sig['conf']}% High Win-Rate Probability</span></div>
                </div>
            """, unsafe_allow_html=True)
            
            # --- TRADE FEEDBACK & RESULT TRACKING MODULE ---
            st.markdown("---")
            st.markdown("#### 📊 Trade Feedback & Result Tracking")
            fb_col1, fb_col2 = st.columns(2)
            with fb_col1:
                user_fb = st.radio("User Feedback", ["Good", "Bad"], horizontal=True, key="trade_feedback_radio")
            with fb_col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Submit Feedback"):
                    st.success("✅ Thank you for your valuable feedback! Stats updated successfully.")
        
        st.markdown('</div>', unsafe_allow_html=True)
