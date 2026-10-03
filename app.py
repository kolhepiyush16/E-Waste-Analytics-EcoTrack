import streamlit as st
import pandas as pd
import joblib


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="EcoTrack | E-Waste Intelligence",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DESIGN SYSTEM (CSS)
# Palette:
#   Navy      #0B1020  (brand / sidebar / footer)
#   Emerald   #10B981  (primary accent)
#   Sky       #0EA5E9  (secondary accent)
#   Amber     #F59E0B  (warning accent)
#   Indigo    #6366F1  (highlight accent)
#   Canvas    #F1F5F9  (page background)
#   Ink       #0F172A / Slate #475569 (text)
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

    :root {
        --navy: #0B1020;
        --indigo-900: #1E1B4B;
        --emerald: #10B981;
        --emerald-dark: #047857;
        --cyan: #06B6D4;
        --sky: #0EA5E9;
        --violet: #8B5CF6;
        --amber: #F59E0B;
        --canvas: #F4F7FB;
        --card: #FFFFFF;
        --ink: #0F172A;
        --slate: #475569;
        --muted: #64748B;
        --line: rgba(15,23,42,0.08);
        --radius: 18px;
        --shadow-sm: 0 1px 2px rgba(15,23,42,0.04), 0 4px 12px rgba(15,23,42,0.05);
        --shadow-md: 0 10px 30px rgba(15,23,42,0.10);
    }

    @keyframes fadeUp {
        from {opacity: 0; transform: translateY(14px);}
        to   {opacity: 1; transform: translateY(0);}
    }
    @keyframes gradientShift {
        0%   {background-position: 0% 50%;}
        50%  {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    @keyframes spinSlow {
        from {transform: rotate(0deg);}
        to   {transform: rotate(360deg);}
    }
    @keyframes pulseDot {
        0%   {box-shadow: 0 0 0 0 rgba(52,211,153,0.7);}
        70%  {box-shadow: 0 0 0 9px rgba(52,211,153,0);}
        100% {box-shadow: 0 0 0 0 rgba(52,211,153,0);}
    }
    @keyframes glowPulse {
        0%, 100% {box-shadow: 0 14px 34px rgba(15,23,42,0.22);}
        50%      {box-shadow: 0 14px 48px rgba(15,23,42,0.38);}
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ---------- Canvas with soft gradient mesh ---------- */
    .stApp {
        background:
            radial-gradient(900px 500px at 8% -5%, rgba(16,185,129,0.14), transparent 60%),
            radial-gradient(800px 480px at 95% 0%, rgba(139,92,246,0.13), transparent 60%),
            radial-gradient(700px 420px at 60% 100%, rgba(6,182,212,0.10), transparent 60%),
            var(--canvas);
        background-attachment: fixed;
    }
    .stApp .main p, .stApp .main li, .stApp .main label {
        color: var(--slate);
    }
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 130px;
        max-width: 1280px;
        animation: fadeUp 0.5s ease both;
    }
    #MainMenu, footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}

    ::-webkit-scrollbar {width: 10px; height: 10px;}
    ::-webkit-scrollbar-thumb {background: #CBD5E1; border-radius: 10px;}
    ::-webkit-scrollbar-thumb:hover {background: #94A3B8;}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(420px 260px at 0% 0%, rgba(16,185,129,0.28), transparent 65%),
            radial-gradient(380px 300px at 100% 100%, rgba(139,92,246,0.25), transparent 65%),
            linear-gradient(180deg, var(--navy) 0%, var(--indigo-900) 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    section[data-testid="stSidebar"] > div {
        padding-bottom: 110px;
    }
    section[data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.10);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 0.35rem;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
        display: none;               /* hide the default radio circle */
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 0.7rem 1rem;
        border-radius: 12px;
        border: 1px solid transparent;
        transition: all 0.2s ease;
        cursor: pointer;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background: rgba(255,255,255,0.07);
        border-color: rgba(255,255,255,0.10);
        transform: translateX(3px);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(90deg, #10B981, #06B6D4);
        box-shadow: 0 8px 20px rgba(16,185,129,0.35);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) * {
        color: #04120D !important;
        font-weight: 700;
    }
    .side-brand {
        text-align: center;
        padding: 0.8rem 0 0.4rem 0;
    }
    .side-brand .logo {
        width: 68px; height: 68px;
        margin: 0 auto 0.6rem auto;
        border-radius: 20px;
        background: linear-gradient(135deg, #10B981, #06B6D4 60%, #8B5CF6);
        display: flex; align-items: center; justify-content: center;
        font-size: 2.1rem;
        box-shadow: 0 12px 28px rgba(16,185,129,0.45);
    }
    .side-brand .name {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.55rem; font-weight: 800; letter-spacing: 0.3px;
        color: #FFFFFF !important;
    }
    .side-brand .tag {
        font-size: 0.78rem; opacity: 0.7; margin-top: 2px;
    }

    /* ---------- Hero ---------- */
    .hero {
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        padding: 2.9rem 3rem;
        margin-bottom: 1.8rem;
        background: linear-gradient(120deg, #0B1020 0%, #1E1B4B 32%, #065F46 70%, #0891B2 100%);
        background-size: 220% 220%;
        animation: gradientShift 14s ease infinite;
        box-shadow: 0 24px 50px rgba(30,27,75,0.35);
        border: 1px solid rgba(255,255,255,0.08);
    }
    .hero::before {                       /* dotted grid texture */
        content: "";
        position: absolute; inset: 0;
        background-image: radial-gradient(rgba(255,255,255,0.10) 1px, transparent 1px);
        background-size: 22px 22px;
        mask-image: linear-gradient(90deg, transparent, #000 60%);
        -webkit-mask-image: linear-gradient(90deg, transparent, #000 60%);
    }
    .hero::after {                        /* glow orbs */
        content: "";
        position: absolute; inset: 0;
        background:
            radial-gradient(360px 260px at 88% 12%, rgba(16,185,129,0.50), transparent 70%),
            radial-gradient(300px 240px at 70% 110%, rgba(139,92,246,0.45), transparent 70%);
        pointer-events: none;
    }
    .hero .mark {
        position: absolute; right: 3.2rem; top: 50%;
        margin-top: -90px;
        font-size: 11rem; line-height: 1;
        opacity: 0.16; z-index: 1;
        animation: spinSlow 40s linear infinite;
        filter: drop-shadow(0 0 30px rgba(52,211,153,0.6));
    }
    .hero .pill {
        position: relative; z-index: 2;
        display: inline-flex; align-items: center; gap: 0.5rem;
        background: rgba(255,255,255,0.10);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.22);
        color: #A7F3D0 !important;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 1.6px;
        padding: 0.35rem 0.9rem; border-radius: 999px;
        margin-bottom: 1rem;
    }
    .hero .pill .dot {
        width: 8px; height: 8px; border-radius: 50%;
        background: #34D399; display: inline-block;
        animation: pulseDot 2s infinite;
    }
    .hero h1 {
        position: relative; z-index: 2;
        margin: 0;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.7rem; font-weight: 800; letter-spacing: -0.8px;
        color: #FFFFFF !important; line-height: 1.12;
    }
    .hero p {
        position: relative; z-index: 2;
        margin: 0.9rem 0 0 0; max-width: 700px;
        font-size: 1.05rem; line-height: 1.6;
        color: #CBD5E1 !important;
    }

    /* ---------- Section titles ---------- */
    .section-title {
        display: flex; align-items: center; gap: 0.7rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.3rem; font-weight: 800; letter-spacing: -0.2px;
        color: var(--ink);
        margin: 2rem 0 1rem 0;
    }
    .section-title::before {
        content: "";
        width: 6px; height: 1.5rem; border-radius: 6px;
        background: linear-gradient(180deg, var(--emerald), var(--cyan), var(--violet));
    }
    .section-title::after {
        content: "";
        flex: 1; height: 1px;
        background: linear-gradient(90deg, rgba(15,23,42,0.14), transparent);
    }

    /* ---------- KPI cards ---------- */
    .kpi-card {
        position: relative; overflow: hidden;
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: var(--radius);
        padding: 1.3rem 1.4rem;
        box-shadow: var(--shadow-sm);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .kpi-card::after {                    /* soft accent glow */
        content: "";
        position: absolute; right: -40px; top: -40px;
        width: 130px; height: 130px; border-radius: 50%;
        background: radial-gradient(circle, color-mix(in srgb, var(--accent, #10B981) 28%, transparent), transparent 70%);
    }
    .kpi-card::before {                   /* accent line */
        content: "";
        position: absolute; left: 0; right: 0; bottom: 0; height: 4px;
        background: linear-gradient(90deg, var(--accent, #10B981), color-mix(in srgb, var(--accent, #10B981) 40%, white));
    }
    .kpi-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 38px color-mix(in srgb, var(--accent, #10B981) 28%, transparent);
    }
    .kpi-icon {
        position: relative; z-index: 1;
        width: 46px; height: 46px; border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.4rem;
        background: linear-gradient(135deg, var(--accent, #10B981), color-mix(in srgb, var(--accent, #10B981) 55%, white));
        box-shadow: 0 8px 18px color-mix(in srgb, var(--accent, #10B981) 40%, transparent);
        margin-bottom: 0.9rem;
    }
    .kpi-label {
        position: relative; z-index: 1;
        font-size: 0.74rem; font-weight: 700; letter-spacing: 0.9px;
        text-transform: uppercase; color: var(--muted) !important;
    }
    .kpi-value {
        position: relative; z-index: 1;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.85rem; font-weight: 800; letter-spacing: -0.5px;
        color: var(--ink) !important;
        margin-top: 0.15rem; margin-bottom: 0.3rem;
    }

    /* ---------- Feature cards ---------- */
    .info-card {
        position: relative; overflow: hidden;
        height: 100%;
        background: linear-gradient(180deg, color-mix(in srgb, var(--accent, #10B981) 9%, white), #FFFFFF 55%);
        border: 1px solid var(--line);
        border-radius: var(--radius);
        padding: 1.6rem;
        box-shadow: var(--shadow-sm);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .info-card::before {
        content: "";
        position: absolute; left: 0; right: 0; top: 0; height: 5px;
        background: linear-gradient(90deg, var(--accent, #10B981), color-mix(in srgb, var(--accent, #10B981) 40%, white));
    }
    .info-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 38px color-mix(in srgb, var(--accent, #10B981) 26%, transparent);
    }
    .info-card h4 {
        margin: 0.2rem 0 0.55rem 0;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.12rem; font-weight: 800;
        color: var(--ink) !important;
    }
    .info-card p {
        margin: 0; font-size: 0.93rem; line-height: 1.6;
        color: var(--slate) !important;
    }

    /* ---------- Insight rows ---------- */
    .insight {
        background: linear-gradient(90deg, color-mix(in srgb, var(--accent, #10B981) 10%, white), #FFFFFF 70%);
        border: 1px solid var(--line);
        border-left: 5px solid var(--accent, #10B981);
        border-radius: 14px;
        padding: 1.05rem 1.3rem;
        margin-bottom: 0.8rem;
        box-shadow: var(--shadow-sm);
        color: var(--ink) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .insight:hover {
        transform: translateX(6px);
        box-shadow: var(--shadow-md);
    }
    .insight b { color: var(--accent, #047857) !important; }

    /* ---------- Tech badges ---------- */
    .badge {
        display: inline-block;
        background: var(--card);
        color: var(--ink) !important;
        border: 1px solid var(--line);
        padding: 0.55rem 1.2rem;
        border-radius: 999px;
        font-weight: 600; font-size: 0.9rem;
        margin: 0.3rem 0.45rem 0.3rem 0;
        box-shadow: var(--shadow-sm);
        transition: all 0.2s ease;
    }
    .badge:hover {
        transform: translateY(-3px);
        border-color: var(--emerald);
        box-shadow: 0 10px 22px rgba(16,185,129,0.25);
    }

    /* ---------- Chart containers ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: var(--card);
        border: 1px solid var(--line) !important;
        border-radius: var(--radius);
        box-shadow: var(--shadow-sm);
        padding: 0.6rem 0.8rem;
        transition: box-shadow 0.25s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: var(--shadow-md);
    }

    /* ---------- Inputs ---------- */
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        border-radius: 12px !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: var(--emerald) !important;
        box-shadow: 0 0 0 3px rgba(16,185,129,0.20);
    }

    /* ---------- Risk result ---------- */
    .risk-box {
        text-align: center;
        padding: 2.2rem 1rem;
        border-radius: 22px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.1rem; font-weight: 800; letter-spacing: 1.5px;
        color: #FFFFFF !important;
        animation: glowPulse 3s ease-in-out infinite;
    }
    .risk-low    { background: linear-gradient(135deg, #047857, #34D399); }
    .risk-medium { background: linear-gradient(135deg, #B45309, #FBBF24); }
    .risk-high   { background: linear-gradient(135deg, #991B1B, #FB7185); }

    /* ---------- Buttons ---------- */
    div.stButton > button {
        background: linear-gradient(90deg, #10B981, #06B6D4);
        color: #04120D !important;
        border: none; border-radius: 14px;
        padding: 0.8rem 1rem; font-weight: 800; letter-spacing: 0.3px;
        box-shadow: 0 10px 24px rgba(16,185,129,0.35);
        transition: all 0.25s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 32px rgba(6,182,212,0.45);
        color: #04120D !important;
    }

    /* ---------- Fixed footer (never scrolls) ---------- */
    .footer {
        position: fixed;
        left: 0; right: 0; bottom: 0;
        z-index: 1000000;
        background: linear-gradient(90deg, #0B1020, #1E1B4B 60%, #0B1020);
        padding: 0.8rem 2rem;
        display: flex; flex-wrap: wrap;
        align-items: center; justify-content: space-between;
        gap: 0.4rem 2rem;
        box-shadow: 0 -10px 30px rgba(11,16,32,0.35);
    }
    .footer::before {
        content: "";
        position: absolute; left: 0; right: 0; top: 0; height: 3px;
        background: linear-gradient(90deg, #10B981, #06B6D4, #8B5CF6, #10B981);
        background-size: 200% 100%;
        animation: gradientShift 6s linear infinite;
    }
    .footer .left  { text-align: left; }
    .footer .right { text-align: right; }
    .footer .brand {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.1rem; font-weight: 800; color: #FFFFFF !important;
    }
    .footer .line {
        font-size: 0.8rem; color: #94A3B8 !important; line-height: 1.5;
    }
    .footer .accent {
        color: #6EE7B7 !important; font-weight: 700;
    }
    @media (max-width: 700px) {
        .hero { padding: 2rem 1.5rem; }
        .hero h1 { font-size: 2rem; }
        .hero .mark { display: none; }
        .footer { padding: 0.6rem 1rem; justify-content: center; }
        .footer .left, .footer .right { text-align: center; }
        .block-container { padding-bottom: 170px; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def hero(tag, title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="mark">♻️</div>
            <span class="pill"><i class="dot"></i>{tag}</span>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def section(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True
    )


def kpi(icon, label, value, accent="#10B981"):
    st.markdown(
        f"""
        <div class="kpi-card" style="--accent:{accent};">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def info_card(accent, title, text):
    st.markdown(
        f"""
        <div class="info-card" style="--accent:{accent};">
            <h4>{title}</h4>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def insight(accent, text):
    st.markdown(
        f'<div class="insight" style="--accent:{accent};">{text}</div>',
        unsafe_allow_html=True
    )


def chart_title(text):
    st.markdown(
        f'<div class="chart-title">{text}</div>',
        unsafe_allow_html=True
    )


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/processed/ewaste_cleaned.csv"
    )


df = load_data()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div class="side-brand">
        <div class="logo">♻️</div>
        <div class="name">EcoTrack</div>
        <div class="tag">E-Waste Intelligence Platform</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "🧭 Navigation",
    [
        "🏠 Home",
        "📊 Dashboard",
        "📈 E-Waste Analysis",
        "🔮 Prediction",
        "⚠️ Risk Classification",
        "💡 Insights"
    ]
)


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    hero(
        "DATA-DRIVEN SUSTAINABILITY",
        "♻️ EcoTrack",
        "E-Waste Analytics, Risk Classification & Predictive Management System. "
        "Analyze generation, collection, recycling, disposal and hazardous "
        "materials using data analytics and machine learning."
    )

    section("Dataset at a Glance")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi("📋", "Total Records", f"{len(df):,}", "#10B981")

    with col2:
        kpi("📱", "Device Types", f"{df['Device_Type'].nunique()}", "#0EA5E9")

    with col3:
        kpi("🏙️", "Cities Covered", f"{df['City'].nunique()}", "#F59E0B")

    with col4:
        kpi("📅", "Financial Years", f"{df['Financial_Year'].nunique()}", "#6366F1")

    section("Project Modules")

    col1, col2, col3 = st.columns(3)

    with col1:
        info_card(
            "#10B981",
            "📊 Analyze",
            "Explore e-waste generation across devices, cities, "
            "recycling performance and hazardous materials."
        )

    with col2:
        info_card(
            "#0EA5E9",
            "🔮 Predict",
            "Estimate future e-waste generation using a "
            "Linear Regression model."
        )

    with col3:
        info_card(
            "#F59E0B",
            "⚠️ Classify",
            "Classify e-waste management risk as Low, Medium "
            "or High using a KNN classifier."
        )

    section("Technology Stack")

    st.markdown(
        """
        <span class="badge">🐍 Python</span>
        <span class="badge">🐼 Pandas</span>
        <span class="badge">🔢 NumPy</span>
        <span class="badge">📊 Matplotlib</span>
        <span class="badge">🤖 Scikit-learn</span>
        <span class="badge">🚀 Streamlit</span>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DASHBOARD
# =========================================================

elif page == "📊 Dashboard":

    hero(
        "OVERVIEW",
        "📊 EcoTrack Dashboard",
        "A consolidated view of the analyzed e-waste dataset."
    )

    total_records = len(df)

    total_ewaste = df["E_Waste_kg"].sum()

    total_collected = df["Collected_kg"].sum()

    total_recycled = df["Recycled_kg"].sum()

    recycling_rate = (
        total_recycled / total_ewaste * 100
        if total_ewaste > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi("📋", "Records", f"{total_records:,}", "#6366F1")

    with col2:
        kpi("♻️", "E-Waste", f"{total_ewaste:,.0f} kg", "#10B981")

    with col3:
        kpi("📦", "Collected", f"{total_collected:,.0f} kg", "#0EA5E9")

    with col4:
        kpi("🔄", "Recycling", f"{recycling_rate:.2f}%", "#F59E0B")

    section("E-Waste Generation Trend")

    yearly = (
        df.groupby("Financial_Year")["E_Waste_kg"]
        .sum()
    )

    with st.container(border=True):
        st.line_chart(yearly, color="#10B981")

    col1, col2 = st.columns(2)

    with col1:

        section("E-Waste by Device")

        device_data = (
            df.groupby("Device_Type")["E_Waste_kg"]
            .sum()
            .sort_values(ascending=False)
        )

        with st.container(border=True):
            st.bar_chart(device_data, color="#0EA5E9")

    with col2:

        section("E-Waste by City")

        city_data = (
            df.groupby("City")["E_Waste_kg"]
            .sum()
            .sort_values(ascending=False)
        )

        with st.container(border=True):
            st.bar_chart(city_data, color="#6366F1")

    section("Recycling vs Disposal")

    recycled = df["Recycled_kg"].sum()

    disposed = df["Disposed_kg"].sum()

    recycling_disposal = pd.DataFrame(
        {
            "Category": [
                "Recycled",
                "Disposed"
            ],
            "Quantity_kg": [
                recycled,
                disposed
            ]
        }
    )

    with st.container(border=True):
        st.bar_chart(
            recycling_disposal.set_index("Category"),
            color="#14B8A6"
        )


# =========================================================
# E-WASTE ANALYSIS
# =========================================================

elif page == "📈 E-Waste Analysis":

    hero(
        "DEEP DIVE",
        "📈 E-Waste Analysis",
        "Detailed analysis of e-waste generation, recycling and hazardous materials."
    )

    section("Device-wise E-Waste")

    device_data = (
        df.groupby("Device_Type")["E_Waste_kg"]
        .sum()
        .sort_values(ascending=False)
    )

    with st.container(border=True):
        st.bar_chart(device_data, color="#0EA5E9")

    insight(
        "#0EA5E9",
        f"📱 Highest e-waste generating device: "
        f"<b>{device_data.idxmax()}</b>"
    )

    section("City-wise E-Waste")

    city_data = (
        df.groupby("City")["E_Waste_kg"]
        .sum()
        .sort_values(ascending=False)
    )

    with st.container(border=True):
        st.bar_chart(city_data, color="#6366F1")

    insight(
        "#6366F1",
        f"🏙️ Highest e-waste generating city: "
        f"<b>{city_data.idxmax()}</b>"
    )

    section("Recycling Rate by Device")

    recycling_data = (
        df.groupby("Device_Type")["Recycling_Rate_pct"]
        .mean()
        .sort_values(ascending=False)
    )

    with st.container(border=True):
        st.bar_chart(recycling_data, color="#10B981")

    section("Hazardous Material Distribution")

    hazardous_data = (
        df["Hazardous_Material"]
        .value_counts()
    )

    with st.container(border=True):
        st.bar_chart(hazardous_data, color="#F59E0B")


# =========================================================
# PREDICTION
# =========================================================

elif page == "🔮 Prediction":

    hero(
        "MACHINE LEARNING",
        "🔮 E-Waste Prediction",
        "Linear Regression is used to estimate future e-waste generation."
    )

    try:

        model = joblib.load(
            "models/linear_regression.pkl"
        )

        yearly_data = (
            df.groupby("Financial_Year")["E_Waste_kg"]
            .sum()
            .reset_index()
        )

        yearly_data["Year"] = (
            yearly_data["Financial_Year"]
            .str[:4]
            .astype(int)
        )

        first_year = int(
            yearly_data["Year"].min()
        )

        last_year = int(
            yearly_data["Year"].max()
        )

        selected_year = st.number_input(
            "📅 Select Future Year",
            min_value=last_year + 1,
            max_value=2050,
            value=2030,
            step=1
        )

        selected_input = pd.DataFrame(
            {
                "Year": [selected_year]
            }
        )

        selected_prediction = model.predict(
            selected_input
        )[0]

        col1, col2 = st.columns(2)

        with col1:
            kpi(
                "🔮",
                f"Predicted E-Waste for {selected_year}",
                f"{selected_prediction:,.2f} kg",
                "#10B981"
            )

        with col2:
            kpi(
                "📅",
                "Last Year in Dataset",
                f"{last_year}",
                "#0EA5E9"
            )

        actual = yearly_data[
            ["Year", "E_Waste_kg"]
        ].copy()

        actual.rename(
            columns={
                "E_Waste_kg": "Actual"
            },
            inplace=True
        )

        prediction_years = list(
            range(
                first_year,
                selected_year + 1
            )
        )

        prediction_input = pd.DataFrame(
            {
                "Year": prediction_years
            }
        )

        prediction_values = model.predict(
            prediction_input
        )

        prediction = pd.DataFrame(
            {
                "Year": prediction_years,
                "Prediction": prediction_values
            }
        )

        graph_data = pd.merge(
            actual,
            prediction,
            on="Year",
            how="outer"
        )

        graph_data.sort_values(
            "Year",
            inplace=True
        )

        graph_data.set_index(
            "Year",
            inplace=True
        )

        section("Actual vs Prediction")

        with st.container(border=True):
            st.line_chart(
                graph_data[
                    ["Actual", "Prediction"]
                ],
                color=["#0EA5E9", "#10B981"]
            )

        st.caption(
            f"Prediction line extends to {selected_year}."
        )

        section("Prediction Details")

        result = pd.DataFrame(
            {
                "Year": [selected_year],
                "Predicted E-Waste (kg)": [
                    round(
                        selected_prediction,
                        2
                    )
                ]
            }
        )

        st.dataframe(
            result,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:

        st.error(
            f"Prediction model error: {e}"
        )


# =========================================================
# RISK CLASSIFICATION
# =========================================================

elif page == "⚠️ Risk Classification":

    hero(
        "MACHINE LEARNING",
        "⚠️ E-Waste Risk Classification",
        "KNN classifies e-waste management risk as Low, Medium or High."
    )

    try:

        knn_model = joblib.load(
            "models/knn_classifier.pkl"
        )

        scaler = joblib.load(
            "models/knn_scaler.pkl"
        )

        section("Enter E-Waste Parameters")

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:

                e_waste = st.number_input(
                    "E-Waste Generated (kg)",
                    min_value=0.0,
                    value=1000.0
                )

                collection_rate = st.number_input(
                    "Collection Rate (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=70.0
                )

                recycling_rate = st.number_input(
                    "Recycling Rate (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=50.0
                )

            with col2:

                disposal_rate = st.number_input(
                    "Disposal Rate (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=30.0
                )

                growth_rate = st.number_input(
                    "Growth Rate (%)",
                    value=5.0
                )

                hazardous_material = st.number_input(
                    "Hazardous Material (g)",
                    min_value=0.0,
                    value=100.0
                )

        st.write("")

        if st.button(
            "🔍 Classify Risk",
            use_container_width=True
        ):

            input_data = pd.DataFrame(
                {
                    "E_Waste_kg": [e_waste],
                    "Collection_Rate_pct": [
                        collection_rate
                    ],
                    "Recycling_Rate_pct": [
                        recycling_rate
                    ],
                    "Disposal_Rate_pct": [
                        disposal_rate
                    ],
                    "Growth_Rate_pct": [
                        growth_rate
                    ],
                    "Hazardous_Material_g": [
                        hazardous_material
                    ]
                }
            )

            scaled_input = scaler.transform(
                input_data
            )

            risk_prediction = knn_model.predict(
                scaled_input
            )[0]

            section("Risk Classification Result")

            if risk_prediction == "Low":

                st.markdown(
                    '<div class="risk-box risk-low">🟢 LOW RISK</div>',
                    unsafe_allow_html=True
                )

            elif risk_prediction == "Medium":

                st.markdown(
                    '<div class="risk-box risk-medium">🟡 MEDIUM RISK</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '<div class="risk-box risk-high">🔴 HIGH RISK</div>',
                    unsafe_allow_html=True
                )

    except Exception as e:

        st.error(
            f"Risk model error: {e}"
        )


# =========================================================
# INSIGHTS
# =========================================================

elif page == "💡 Insights":

    hero(
        "FINDINGS",
        "💡 EcoTrack Insights",
        "Key findings generated from the analyzed dataset."
    )

    yearly = (
        df.groupby("Financial_Year")["E_Waste_kg"]
        .sum()
    )

    highest_year = yearly.idxmax()

    highest_value = yearly.max()

    device = (
        df.groupby("Device_Type")["E_Waste_kg"]
        .sum()
    )

    highest_device = device.idxmax()

    city = (
        df.groupby("City")["E_Waste_kg"]
        .sum()
    )

    highest_city = city.idxmax()

    total_recycled = df["Recycled_kg"].sum()

    total_ewaste = df["E_Waste_kg"].sum()

    recycling_percentage = (
        total_recycled /
        total_ewaste *
        100
    )

    section("Key Findings")

    insight(
        "#10B981",
        f"📈 Highest e-waste generation was observed in "
        f"<b>{highest_year}</b>, with approximately "
        f"<b>{highest_value:,.0f} kg</b>."
    )

    insight(
        "#0EA5E9",
        f"📱 <b>{highest_device}</b> generated the highest "
        f"amount of e-waste in the dataset."
    )

    insight(
        "#6366F1",
        f"🏙️ <b>{highest_city}</b> recorded the highest "
        f"e-waste generation in the dataset."
    )

    insight(
        "#F59E0B",
        f"♻️ Calculated recycling proportion: "
        f"<b>{recycling_percentage:.2f}%</b>."
    )

    section("Recommendations")

    col1, col2, col3 = st.columns(3)

    with col1:
        info_card(
            "#10B981",
            "🏗️ Collection",
            "Improve e-waste collection infrastructure."
        )

    with col2:
        info_card(
            "#0EA5E9",
            "♻️ Recovery",
            "Increase recycling and recovery activities."
        )

    with col3:
        info_card(
            "#F59E0B",
            "☣️ Safety",
            "Monitor hazardous materials carefully."
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        info_card(
            "#6366F1",
            "📍 Hotspots",
            "Identify high e-waste generating locations."
        )

    with col2:
        info_card(
            "#14B8A6",
            "🔮 Planning",
            "Use predictive analytics for future planning."
        )


# =========================================================
# FIXED FOOTER (stays at the bottom of the screen)
# =========================================================

st.markdown(
    """
    <div class="footer">
        <div class="left">
            <div class="brand">♻️ EcoTrack</div>
            <div class="line">© 2026 All Rights Reserved</div>
            <div class="line">Built with ❤️ by <span class="accent">Piyush Kolhe</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
