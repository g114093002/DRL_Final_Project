import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* High-End Research Console Style */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        :root {
            --bg-deep: #0B1220;
            --sidebar-bg: #081018;
            --card-bg: rgba(17, 24, 39, 0.78);
            --primary-accent: #38BDF8;
            --text-main: #E2E8F0;
            --text-muted: #94A3B8;
            --border-soft: rgba(255, 255, 255, 0.06);
            --grid-line: rgba(255, 255, 255, 0.04);
        }

        .main {
            background-color: var(--bg-deep);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        /* Typography Scaling */
        h1 { font-size: 52px !important; font-weight: 700 !important; color: white !important; margin-bottom: 8px !important; letter-spacing: -0.04em !important; }
        h2 { font-size: 30px !important; font-weight: 600 !important; color: white !important; margin-top: 32px !important; margin-bottom: 16px !important; border: none !important; }
        h3 { font-size: 18px !important; font-weight: 500 !important; color: var(--text-muted) !important; margin-bottom: 12px !important; }
        p, li { font-size: 15px; color: var(--text-muted); line-height: 1.6; }

        /* KPI Cards: High Density */
        div[data-testid="stMetric"] {
            background: var(--card-bg);
            border: 1px solid var(--border-soft);
            border-radius: 6px;
            padding: 12px 16px !important;
            box-shadow: 0 0 20px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            border-color: rgba(56, 189, 248, 0.2);
            box-shadow: 0 0 30px rgba(56, 189, 248, 0.05);
        }
        div[data-testid="stMetric"] label p {
            font-size: 11px !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted) !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: 22px !important;
            font-weight: 600 !important;
            color: white !important;
        }

        /* Denser Layout */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            max-width: 1400px !important;
        }
        
        /* Sidebar: Strict Console Look */
        .stSidebar {
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-soft);
        }
        .sidebar-header {
            color: var(--primary-accent);
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            margin-bottom: 8px;
            opacity: 0.8;
        }

        /* Specialized Action Button */
        div.stButton > button:first-child {
            background: #111827;
            border: 1px solid var(--primary-accent);
            color: var(--primary-accent);
            text-transform: uppercase;
            font-weight: 600;
            font-size: 12px;
            letter-spacing: 0.08em;
            padding: 8px 16px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }
        div.stButton > button:first-child:hover {
            background: var(--primary-accent);
            color: #000;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }

        /* Plotly Custom Container Fix for rounded corners */
        .js-plotly-plot {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-soft);
            background-color: #0C1425 !important;
        }

        /* methodology note */
        .methodology-note {
            background: rgba(56, 189, 248, 0.03);
            border: 1px solid rgba(56, 189, 248, 0.1);
            color: var(--text-muted);
            padding: 12px 16px;
            border-radius: 4px;
            font-size: 13px;
            margin-bottom: 24px;
        }

        /* Tabs Refinement */
        .stTabs [data-baseweb="tab-list"] {
            border-bottom: 1px solid var(--border-soft);
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 14px;
            height: 44px;
        }
        </style>
    """, unsafe_allow_html=True)
