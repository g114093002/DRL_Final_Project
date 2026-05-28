import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .main {
            background-color: #0e1117;
        }
        .stMetric {
            background-color: #1e2130;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        h1, h2, h3 {
            color: #00d4ff;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #1e2130;
            border-radius: 5px 5px 0 0;
            color: white;
            padding: 10px 20px;
        }
        .stTabs [aria-selected="true"] {
            border-bottom: 2px solid #00d4ff;
        }
        </style>
    """, unsafe_allow_html=True)
