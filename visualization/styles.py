import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* High-End Research Console Style */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg-deep: #080C14;
            --sidebar-bg: #05080F;
            --card-bg: rgba(17, 24, 39, 0.85);
            --primary-accent: #38BDF8;
            --text-main: #F1F5F9; /* Brighter white */
            --text-muted: #CBD5E1; /* High contrast gray */
            --border-soft: rgba(255, 255, 255, 0.1);
            --grid-line: rgba(255, 255, 255, 0.05);
        }

        .main {
            background-color: var(--bg-deep);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        /* Typography Scaling */
        h1 { font-size: 48px !important; font-weight: 700 !important; color: white !important; margin-bottom: 8px !important; letter-spacing: -0.04em !important; }
        h2 { font-size: 28px !important; font-weight: 600 !important; color: white !important; margin-top: 32px !important; margin-bottom: 24px !important; border: none !important; }
        h3 { font-size: 20px !important; font-weight: 600 !important; color: var(--primary-accent) !important; margin-bottom: 12px !important; }
        p, li { font-size: 16px; color: var(--text-muted); line-height: 1.6; font-weight: 400; }

        /* KPI Cards: High Density */
        div[data-testid="stMetric"] {
            background: var(--card-bg);
            border: 1px solid var(--border-soft);
            border-radius: 8px;
            padding: 16px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        }
        div[data-testid="stMetric"] label p {
            font-size: 12px !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--text-muted) !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: 26px !important;
            font-weight: 700 !important;
            color: white !important;
        }

        /* Tabs Refinement: High Contrast */
        .stTabs [data-baseweb="tab-list"] {
            border-bottom: 1px solid var(--border-soft);
            gap: 12px;
            padding-bottom: 4px;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 15px !important;
            font-weight: 600 !important;
            color: var(--text-muted) !important;
            height: 48px;
            background-color: transparent !important;
        }
        .stTabs [aria-selected="true"] {
            color: var(--primary-accent) !important;
            border-bottom: 3px solid var(--primary-accent) !important;
        }

        /* Sidebar: Strict Console Look */
        .stSidebar {
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-soft);
        }
        .sidebar-header {
            color: var(--primary-accent);
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 12px;
            padding-top: 10px;
        }

        /* Plotly Custom Container Fix: Add top spacing */
        .js-plotly-plot {
            margin-top: 1.5rem !important;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-soft);
            background-color: #0F172A !important;
        }

        /* methodology note: High Contrast */
        .methodology-note {
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.2);
            color: #E2E8F0;
            padding: 16px 20px;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 32px;
            line-height: 1.6;
        }

        .block-container {
            padding-top: 3rem !important;
            max-width: 1400px !important;
        }
        </style>
    """, unsafe_allow_html=True)
