import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Professional Research Theme: Strict Palette */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        :root {
            --bg-deep: #0B1020;
            --card-bg: rgba(20, 25, 40, 0.72);
            --primary-accent: #38BDF8;
            --success: #34D399;
            --danger: #F87171;
            --warning: #FBBF24;
            --text-primary: #E5E7EB;
            --text-secondary: #94A3B8;
            --border-muted: rgba(148, 163, 184, 0.1);
        }

        .main {
            background-color: var(--bg-deep);
            color: var(--text-primary);
            font-family: 'Inter', sans-serif;
            padding-top: 2rem;
        }

        /* Minimalist Card Styling */
        div[data-testid="stMetric"] {
            background: var(--card-bg);
            border: 1px solid var(--border-muted);
            border-radius: 8px;
            padding: 20px !important;
            box-shadow: none;
            backdrop-filter: blur(8px);
            transition: border-color 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            border-color: rgba(56, 189, 248, 0.3);
        }
        
        div[data-testid="stMetric"] label {
            color: var(--text-secondary) !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.025em !important;
            text-transform: none !important;
        }
        
        div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-size: 1.5rem !important;
        }

        /* Precise Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            padding: 0;
            background-color: transparent;
            border-bottom: 1px solid var(--border-muted);
            margin-bottom: 2.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            padding: 0 16px !important;
            background-color: transparent;
            border-bottom: 2px solid transparent;
            color: var(--text-secondary);
            font-weight: 500;
            font-size: 0.95rem;
            transition: all 0.2s;
        }
        .stTabs [aria-selected="true"] {
            color: var(--primary-accent) !important;
            border-bottom: 3px solid var(--primary-accent) !important;
            background-color: transparent !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary);
        }

        /* Clean Typography */
        h1, h2, h3 {
            color: var(--text-primary);
            font-weight: 600;
            letter-spacing: -0.025em;
            margin-top: 0;
        }
        
        h1 { font-size: 2.25rem; margin-bottom: 0.5rem; }
        h2 { font-size: 1.5rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border-muted); padding-bottom: 0.5rem; }
        h3 { font-size: 1.1rem; color: var(--text-secondary); }

        /* Sidebar: Minimalist */
        .stSidebar {
            background-color: #060914;
            border-right: 1px solid var(--border-muted);
        }
        .stSidebar [data-testid="stExpander"] {
            background-color: transparent;
            border: 1px solid var(--border-muted);
            border-radius: 6px;
            margin-bottom: 0.75rem;
        }

        /* Navigation Flow Components */
        .research-step {
            border-left: 2px solid var(--border-muted);
            padding-left: 1.5rem;
            margin-bottom: 2rem;
        }
        .research-step-active {
            border-left: 2px solid var(--primary-accent);
        }

        /* Buttons */
        .stButton button {
            border-radius: 6px;
            font-weight: 500;
            letter-spacing: 0.02em;
        }
        
        /* Unified Container */
        .block-container {
            padding-top: 3rem !important;
            max-width: 1200px !important;
        }

        /* methodology note */
        .methodology-note {
            padding: 12px 16px;
            background: rgba(148, 163, 184, 0.05);
            border: 1px solid var(--border-muted);
            border-radius: 6px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin: 1.5rem 0;
            line-height: 1.5;
        }
        </style>
    """, unsafe_allow_html=True)
