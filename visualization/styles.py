import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Modern Research Theme */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

        :root {
            --primary-bg: #0d1117;
            --secondary-bg: #161b22;
            --accent-cyan: #00f2ff;
            --accent-green: #00ffaa;
            --accent-purple: #bf5af2;
            --text-main: #e6edf3;
            --text-dim: #8b949e;
            --glass-bg: rgba(22, 27, 34, 0.8);
            --border-glow: rgba(0, 242, 255, 0.3);
        }

        .main {
            background-color: var(--primary-bg);
            background-image: radial-gradient(circle at 50% 0%, #1a2333 0%, #0d1117 100%);
            color: var(--text-main);
            font-family: 'Inter', sans-serif;
        }

        /* Glassmorphism Cards */
        div[data-testid="stMetric"] {
            background: var(--glass-bg);
            border: 1px solid var(--border-glow);
            border-radius: 12px;
            padding: 24px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-4px);
            border-color: var(--accent-cyan);
            box-shadow: 0 8px 30px rgba(0, 242, 255, 0.2);
        }
        
        div[data-testid="stMetric"] label {
            color: var(--text-dim) !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
        }
        
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: var(--accent-cyan) !important;
            font-weight: 700 !important;
            font-size: 1.8rem !important;
        }

        /* Professional Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            padding: 4px;
            background: var(--secondary-bg);
            border-radius: 12px;
            margin-bottom: 2rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 48px;
            padding: 0 24px !important;
            background-color: transparent;
            border-radius: 8px;
            color: var(--text-dim);
            font-weight: 600;
            border: none;
            transition: all 0.2s;
        }
        .stTabs [aria-selected="true"] {
            background-color: var(--primary-bg) !important;
            color: var(--accent-cyan) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-main);
        }

        /* Research Headings */
        h1, h2, h3 {
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        h1 {
            background: linear-gradient(90deg, #fff, var(--accent-cyan));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
        }

        /* Hero Section */
        .hero-banner {
            padding: 3rem;
            background: linear-gradient(135deg, rgba(0, 242, 255, 0.05) 0%, rgba(191, 90, 242, 0.05) 100%);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 3rem;
        }

        /* Methodology Note */
        .methodology-note {
            padding: 1rem;
            background: rgba(191, 90, 242, 0.1);
            border-left: 4px solid var(--accent-purple);
            border-radius: 4px;
            font-size: 0.85rem;
            color: var(--text-main);
            margin: 1rem 0;
        }

        /* Sidebar Cleanup */
        .stSidebar {
            background-color: var(--secondary-bg);
            border-right: 1px solid #30363d;
        }
        
        /* Tooltip and Help */
        .stTooltipIcon {
            color: var(--accent-cyan) !important;
        }

        /* Plotly Container */
        .plotly-graph-div {
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        </style>
    """, unsafe_allow_html=True)
