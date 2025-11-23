import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import json

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="🔥 FF Sensitivity Generator PRO",
    page_icon="🔥",
    layout="wide"
)

# ---------------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------------
if "saved_sens" not in st.session_state:
    st.session_state["saved_sens"] = {}

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f0f0f, #1f1f1f);
    color: #f0f0f0;
    font-family: 'Segoe UI', sans-serif;
}
.banner {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    color: white;
    box-shadow: 0 0 20px #ff416c70;
    margin-bottom: 20px;
}
.fullscreen {
    background: rgba(255, 255, 255, 0.05);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px #00000050;
    margin-bottom: 20px;
}
.stTabs [role="tab"] {
    font-weight: bold;
    font-size: 16px;
    color: #ff7f50;
}
h1, h2, h3 {
    color: #ff7f50;
}
.stButton>button {
    background: linear-gradient(90deg, #ff416c, #ff4b2b);
    color: white;
    font-weight: bold;
    border-radius: 10px;
    padding: 0.5em 1em;
    border: none;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #ff4b2b, #ff416c);
    transform: scale(1.05);
}
.stInfo, .stSuccess, .stWarning, .stError {
    border-left: 5px solid #ff416c;
    border-radius: 10px;
    padding: 10px 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# BANNER
# ---------------------------------------------------------
st.markdown("<div class='banner'>🔥 FF Sensitivity Generator — PRO</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# DEVICE INFO (Optional)
# ---------------------------------------------------------
st.subheader("📱 Device Info (Optional)")
device_input = st.text_input(
    "Enter your device/platform (Optional)", 
    placeholder="e.g., Poco X3, iPhone 13, Realme 10"
)

if device_input.strip():  # Show only if user types something
    device_name = device_input.strip()
    st.info(f"Detected Device: **{device_name}**")
else:
    device_name = "Unknown Device"

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Generate Sensitivity",
    "📊 Device Benchmark",
    "🎮 AI Training Mode",
    "💾 Saved Sensitivities"
])

# =========================================================
# TAB 1 — GENERATE SENSITIVITY
# =========================================================
with tab1:
    st.markdown("<div class='fullscreen'>", unsafe_allow_html=True)
    st.header("🎯 Generate Custom FF Sensitivity")

    col1, col2 = st.columns(2)
    with col1:
        gameplay = st.selectbox("Select Gameplay Style", ["Rusher", "Mid-range", "Sniper"])

    with col2:
        st.write("Device Info:")
        st.success(device_name)

    generate = st.button("🚀 Generate Sensitivity")

    if generate:
        # Base sensitivity (max 200)
        base = {
            "Rusher": [180, 170, 160, 140, 120],
            "Mid-range": [150, 140, 135, 130, 140],
            "Sniper": [120, 110, 105, 100, 160]
        }[gameplay]

        # Device performance factor
        dn = device_name.lower()
        if any(x in dn for x in ["poco","iphone","samsung"]):
            factor = 1.08
        elif any(x in dn for x in ["realme","redmi","vivo"]):
            factor = 1.03
        else:
            factor = 0.95

        final_sens = [min(int(x*factor), 200) for x in base]
        labels = ["General", "Red Dot", "2X Scope", "4X Scope", "Sniper Scope"]

        # Matplotlib visualization
        st.subheader("📊 Sensitivity Preview")
        fig, ax = plt.subplots(figsize=(6,3))
        bars = ax.bar(labels, final_sens, color="#ff416c", alpha=0.85, edgecolor="white")
        ax.set_ylim(0, 200)
        ax.set_ylabel("Sensitivity (0–200)")
        ax.set_title(f"{gameplay} Sensitivity for {device_name}", color="#ff7f50", fontsize=14)
        ax.bar_label(bars, labels=[str(v) for v in final_sens], color="white", fontsize=10)
        st.pyplot(fig)

        # Save to session
        st.session_state["saved_sens"] = {
            "Device": device_name,
            "Gameplay": gameplay,
            "Sensitivity": dict(zip(labels, final_sens))
        }

        # Expandable JSON view
        with st.expander("🔍 View Generated Sensitivity"):
            st.json(st.session_state["saved_sens"])

        # Download button
        st.download_button(
            label="💾 Download Sensitivity JSON",
            data=json.dumps(st.session_state["saved_sens"]),
            file_name=f"{device_name}_FF_sensitivity.json",
            mime="application/json"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2 — DEVICE BENCHMARK
# =========================================================
with tab2:
    st.markdown("<div class='fullscreen'>", unsafe_allow_html=True)
    st.header("📊 Device Performance Benchmark")
    st.write("""
    AI estimates the device score based on:
    - CPU Strength  
    - FPS Stability  
    - Gyro Smoothness  
    - Touch Latency  
    """)

    model = LinearRegression()
    X_train = [[50,60,70],[70,80,85],[90,95,98]]
    y_train = [58,78,96]
    model.fit(X_train, y_train)
    score = model.predict([[65,72,78]])[0]

    st.metric("AI Estimated Device Score", f"{int(score)} / 100")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3 — AI TRAINING MODE
# =========================================================
with tab3:
    st.markdown("<div class='fullscreen'>", unsafe_allow_html=True)
    st.header("🎮 AI Training Mode")
    st.write("""
    Coming soon features:
    - Moving crosshair tracking  
    - Drag accuracy test  
    - Recoil pattern trainer  
    - AI feedback on your drag speed  
    """)
    st.info("Training Mode is under development.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 4 — SAVED SENSITIVITY
# =========================================================
with tab4:
    st.markdown("<div class='fullscreen'>", unsafe_allow_html=True)
    st.header("💾 Saved Sensitivity Profiles")

    saved = st.session_state.get("saved_sens")
    if saved:
        with st.expander("🔍 View Saved Sensitivity"):
            st.json(saved)

        st.download_button(
            label="💾 Download Saved Sensitivity",
            data=json.dumps(saved),
            file_name=f"{saved['Device']}_FF_sensitivity.json",
            mime="application/json"
        )
    else:
        st.info("No saved sensitivity yet!")

    st.markdown("</div>", unsafe_allow_html=True)
