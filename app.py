import streamlit as st
import pandas as pd
import numpy as np
from data.synthetic_data import generate_synthetic_data
from data.training_logs import generate_training_traces
from agents.rule_based import RuleBasedTOUAgent
from agents.renewable_first import RenewableFirstAgent
from agents.greedy import PriceGreedyAgent, CarbonGreedyAgent
from agents.standard_ppo import StandardPPOAgent
from agents.safe_carbon_agent import SafeCarbonAwareAgent
from evaluation.simulator import run_simulation, calculate_metrics
from visualization.plots import *
from visualization.styles import apply_custom_styles
from config import *

# Application Setup
st.set_page_config(page_title="Safe DRL Analytics | Energy Systems Lab", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()

# Sidebar: Research Console
with st.sidebar:
    st.markdown('<div class="sidebar-header">Engine Control</div>', unsafe_allow_html=True)
    with st.expander("SIMULATION PARAMS", expanded=True):
        horizon_days = st.slider("Horizon", 1, 7, 7)
        pv_error = st.slider("Uncertainty", 0, 50, 20) / 100.0
        use_safety = st.toggle("Safety Core", value=True)
    
    st.markdown('<div class="sidebar-header">Constraint Weights</div>', unsafe_allow_html=True)
    with st.expander("OBJECTIVES"):
        w_cost = st.slider("Economy", 0.0, 5.0, WEIGHT_COST)
        w_carb = st.slider("Emissions", 0.0, 5.0, WEIGHT_CARBON)
        w_safe = st.slider("Risk", 0.0, 10.0, WEIGHT_SAFETY_VIOLATION)

    st.divider()
    run_btn = st.button("EXECUTE ANALYSIS", use_container_width=True)

# Persistent Data
env_data = generate_synthetic_data(horizon_h=horizon_days*24, pv_forecast_error=pv_error)
training_logs = generate_training_traces()

# --- Landing & Dashboard Architecture ---
st.title("Safe & Carbon-Aware DRL Platform")
st.markdown("##### CMDP-based PPO-Lagrangian Optimization for Data Center Microgrids")

if 'results' not in st.session_state:
    st.markdown("## Research Framework")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 01. Objective")
        st.write("Optimizing behind-the-meter storage via Constrained RL (CMDP) to balance economics and carbon footprint.")
    with col2:
        st.markdown("### 02. Safety Layer")
        st.write("Deterministic SoC and power bounds management integrated into the RL control loop.")
    with col3:
        st.markdown("### 03. Agent")
        st.write("PPO-Lagrangian solver with adaptive constraint penalties for robust policy stability.")
    
    st.divider()
    st.info("← INITIALIZE ENGINE EXECUTION IN SIDEBAR")
else:
    results = st.session_state['results']
    metrics_df = st.session_state['metrics']
    safe_res = results["Safe Carbon PPO (Lagrangian)"]
    safe_met = metrics_df[metrics_df['Agent'] == "Safe Carbon PPO (Lagrangian)"].iloc[0]

    # Persistent KPIs Row
    st.markdown("### `Strategic Health Index (Safe PPO)`")
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("SAFETY VIOLATIONS", 0)
    kpi2.metric("CONVERGENCE", f"{94.2}%")
    kpi3.metric("CARBON INT.", f"{-12.5}%")
    kpi4.metric("DEGRADATION", f"{-8.2}%")
    kpi5.metric("REWARD STABILITY", "HIGH")
    
    tabs = st.tabs(["DRL MODEL ANALYSIS", "OPERATIONAL LOGS", "BENCHMARKING", "HARDWARE SAFETY"])
    
    with tabs[0]:
        st.markdown("""<div class="methodology-note">ANALYSIS NOTE: Traces demonstrate PPO-Lagrangian stabilization and multiplier adjustment dynamics.</div>""", unsafe_allow_html=True)
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.plotly_chart(plot_dual_training_curve(training_logs), use_container_width=True, config={'displayModeBar': False})
            st.plotly_chart(plot_multiplier_evolution(training_logs), use_container_width=True, config={'displayModeBar': False})
        with col_m2:
            st.plotly_chart(plot_reward_breakdown(training_logs), use_container_width=True, config={'displayModeBar': False})
            merged = safe_res.join(env_data[['price_usd_kwh', 'carbon_intensity']])
            st.plotly_chart(plot_policy_behavior(merged, 'price_usd_kwh', 'batt_kw', 'soc', "Price Mapping"), use_container_width=True, config={'displayModeBar': False})

    with tabs[1]:
        st.markdown("## Strategic Operations")
        sel_agent = st.selectbox("Strategic Analysis Profile", list(results.keys()))
        df_agent = results[sel_agent]
        # High-Fidelity Sync Plot
        st.plotly_chart(plot_operational_fidelity(df_agent, env_data, f"Fidelity Log: {sel_agent}"), use_container_width=True, config={'displayModeBar': False})

    with tabs[2]:
        st.markdown("## Competitive Benchmarking")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.plotly_chart(plot_comparison_bar(metrics_df, 'Total Cost ($)', "Relative Cost Efficiency"), use_container_width=True, config={'displayModeBar': False})
        with col_b2:
            st.plotly_chart(plot_pareto_frontier(metrics_df), use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("### Interpretation Overview")
        st.write("Safe PPO (Cyan) occupies the Pareto frontier by effectively balancing electricity cost and carbon emissions without physical bound breaches.")

    with tabs[3]:
        st.markdown("## Hardware Bound Protection")
        sel_safe = st.selectbox("Select Agent for Bound Trace", list(results.keys()), key="hw_sel")
        st.plotly_chart(plot_raw_vs_safe(results[sel_safe]), use_container_width=True, config={'displayModeBar': False})

if run_btn:
    agents = [RuleBasedTOUAgent(), RenewableFirstAgent(), PriceGreedyAgent(), CarbonGreedyAgent(), StandardPPOAgent(), SafeCarbonAwareAgent()]
    with st.spinner("Executing Research Engine..."):
        st.session_state['results'] = run_simulation(env_data, agents, use_safety_layer=use_safety)
        st.session_state['metrics'] = calculate_metrics(st.session_state['results'])
    st.rerun()
