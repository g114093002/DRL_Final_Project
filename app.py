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

# App Config
st.set_page_config(page_title="Safe Carbon Microgrid Research Platform", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()

# Sidebar
with st.sidebar:
    st.markdown("### `System Configuration`")
    with st.expander("Settings", expanded=True):
        horizon_days = st.slider("Horizon (Days)", 1, 7, 7)
        pv_error = st.slider("PV Forecast Error (%)", 0, 50, 20) / 100.0
        use_safety = st.toggle("Safety Layer", value=True)
    
    with st.expander("Reward Weights"):
        w_cost = st.slider("Cost", 0.0, 5.0, WEIGHT_COST)
        w_carb = st.slider("Carbon", 0.0, 5.0, WEIGHT_CARBON)
        w_safe = st.slider("Safety", 0.0, 10.0, WEIGHT_SAFETY_VIOLATION)

    st.divider()
    run_btn = st.button("RUN ANALYSIS", type="primary", use_container_width=True)

# Data
env_data = generate_synthetic_data(horizon_h=horizon_days*24, pv_forecast_error=pv_error)
training_logs = generate_training_traces()

# Main Narrative
st.title("Safe & Carbon-Aware DRL Platform")
st.markdown("### Constrained RL for Energy System Optimization")

if 'results' not in st.session_state:
    # --- Landing Page Narrative ---
    tabs_home = st.tabs(["Research Goal", "CMDP Architecture", "Key Contributions"])
    
    with tabs_home[0]:
        st.markdown("""
        <div class='research-step research-step-active'>
        <h2>01. Research Objective</h2>
        <p>This platform investigates the application of <b>Constrained Markov Decision Processes (CMDP)</b> to the energy management of behind-the-meter data center microgrids. 
        The primary goal is to derive stable, safety-constrained policies that minimize electricity costs and carbon intensity while maintaining battery health.</p>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://img.icons8.com/wired/128/38bdf8/brain.png", width=60)
        
    with tabs_home[1]:
        st.markdown("<h2>02. CMDP Architecture</h2>", unsafe_allow_html=True)
        st.components.v1.html("""
        <div style="background-color: transparent; padding: 10px;">
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({ startOnLoad: true, theme: 'dark' });
            </script>
            <div class="mermaid">
                graph LR
                    Obs(State) --> Agent(PPO-Lagrangian)
                    Agent --> Raw(Raw Action)
                    Raw --> Safety(Safety Layer)
                    Safety --> Env(Microgrid Env)
                    Env --> R(Reward)
                    Env --> C(Constraint)
                    C & R --> Agent
            </div>
        </div>
        """, height=250)
        
    with tabs_home[2]:
        st.markdown("""
        <div class='research-step'>
        <h2>03. Contributions</h2>
        <ul>
            <li><b>Deterministic Safety Layer</b> ensuring physical SoC constraints.</li>
            <li><b>Carbon-Aware Reward Formulation</b> utilizing dynamic intensity signals.</li>
            <li><b>PPO-Lagrangian Optimization</b> for multi-objective Pareto-efficiency.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("👈 Please initialize the simulation using the sidebar to view Model Analysis and Operational Results.")

else:
    # --- Main Dashboard Tabs ---
    tabs = st.tabs(["DRL Model Analysis", "Operational Metrics", "Strategy Benchmark", "Safety & Health"])
    results = st.session_state['results']
    metrics_df = st.session_state['metrics']
    
    with tabs[0]:
        st.markdown("## Policy Learning Evidence")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            st.plotly_chart(plot_dual_training_curve(training_logs), use_container_width=True)
            st.plotly_chart(plot_multiplier_evolution(training_logs), use_container_width=True)
        with col_a2:
            st.plotly_chart(plot_reward_breakdown(training_logs), use_container_width=True)
            # Policy Mapping
            safe_res = results["Safe Carbon PPO (Lagrangian)"]
            merged = safe_res.join(env_data[['price_usd_kwh', 'carbon_intensity']])
            st.plotly_chart(plot_policy_behavior(merged, 'price_usd_kwh', 'batt_kw', 'soc', "Learned Price Awareness"), use_container_width=True)

    with tabs[1]:
        st.markdown("## Operational Dynamics")
        sel_agent = st.selectbox("Strategic Analysis View", list(results.keys()))
        df_agent = results[sel_agent]
        
        st.plotly_chart(plot_time_series(df_agent, 'batt_kw', f"Battery Dispatch Timeline: {sel_agent}"), use_container_width=True)
        st.plotly_chart(plot_time_series(df_agent, 'soc', "State of Charge (SoC) Trajectory"), use_container_width=True)

    with tabs[2]:
        st.markdown("## Benchmark & Pareto Efficiency")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.plotly_chart(plot_comparison_bar(metrics_df, 'Total Cost ($)', "Normalized Cost Benchmark"), use_container_width=True)
        with col_b2:
            st.plotly_chart(plot_pareto_frontier(metrics_df), use_container_width=True)
        
        st.markdown("### Result Interpretation")
        st.write("The Safe PPO-Lagrangian agent identifies the Pareto frontier, balancing cost and carbon without the instability seen in greedy baselines.")

    with tabs[3]:
        st.markdown("## Safety & Hardware Protection")
        sel_safe = st.selectbox("Select Agent Profile", list(results.keys()), key="safe_tab_sel")
        st.plotly_chart(plot_raw_vs_safe(results[sel_safe]), use_container_width=True)
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Total Interventions", int(results[sel_safe]['safety_modified'].sum()))
        with col_s2:
            st.metric("Final Efficiency", f"{metrics_df[metrics_df['Agent'] == sel_safe]['Renewable Utilization (%)'].values[0]:.1f}%")

# Simulation Logic
if run_btn:
    agents = [RuleBasedTOUAgent(), RenewableFirstAgent(), PriceGreedyAgent(), CarbonGreedyAgent(), StandardPPOAgent(), SafeCarbonAwareAgent()]
    with st.spinner("Analyzing..."):
        st.session_state['results'] = run_simulation(env_data, agents, use_safety_layer=use_safety)
        st.session_state['metrics'] = calculate_metrics(st.session_state['results'])
    st.rerun()
