import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Main background */
        .main {
            background: linear-gradient(135deg, #0b0d17 0%, #1a1c2c 100%);
            color: #e0e0e0;
        }
        
        /* Metric Card Styling */
        div[data-testid="stMetric"] {
            background: rgba(30, 33, 48, 0.7);
            border: 1px solid rgba(0, 212, 255, 0.2);
            border-radius: 12px;
            padding: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            backdrop-filter: blur(4px);
            transition: transform 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px);
            border-color: #00d4ff;
        }
        
        /* Tab Styling - Fixing the squished look */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: #262730;
            border-radius: 8px 8px 0 0;
            padding: 10px 25px !important;
            font-weight: 600;
            color: #888;
            border: none;
            transition: all 0.2s ease;
        }
        .stTabs [aria-selected="true"] {
            background-color: #1e2130 !important;
            color: #00d4ff !important;
            border-bottom: 3px solid #00d4ff !important;
        }
        
        /* Header colors */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.5px;
            background: linear-gradient(90deg, #00d4ff, #00ffaa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Sidebar styling */
        .stSidebar {
            background-color: #0e1117;
        }
        </style>
    """, unsafe_allow_html=True)
