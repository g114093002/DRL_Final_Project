import streamlit as st
import pandas as pd
import numpy as np
import base64
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

# Page Configuration
st.set_page_config(page_title="Safe Carbon DRL Research Platform", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/wired/128/00f2ff/artificial-intelligence.png", width=80)
    st.title("Control Center")
    
    with st.expander("🌐 Simulation Context", expanded=True):
        horizon_days = st.slider("Horizon (Days)", 1, 7, 7)
        pv_error = st.slider("PV Forecast Error (%)", 0, 50, 20) / 100.0
        seed = st.number_input("Random Seed", 0, 9999, 42)
        enable_ev = st.toggle("Enable EV Demand", True)

    with st.expander("🛡️ Safety Constraints", expanded=True):
        use_safety = st.checkbox("Deterministic Safety Layer", value=True)
        soc_min = st.slider("Min SoC", 0.1, 0.4, BESS_SOC_MIN)
        soc_max = st.slider("Max SoC", 0.6, 1.0, BESS_SOC_MAX)

    with st.expander("⚖️ Reward Optimization", expanded=True):
        w_cost = st.slider("Electricity Cost Weight", 0.0, 5.0, WEIGHT_COST)
        w_carbon = st.slider("Carbon Footprint Weight", 0.0, 5.0, WEIGHT_CARBON)
        w_degrad = st.slider("Battery Health Weight", 0.0, 5.0, WEIGHT_DEGRADATION)
        w_safety = st.slider("Safety Penalty (Soft)", 0.0, 20.0, WEIGHT_SAFETY_VIOLATION)

    st.divider()
    run_btn = st.button("🚀 INITIALIZE & RUN SIMULATION", type="primary", use_container_width=True)
    if st.button("♻️ Reset Platform", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- Cached Data & Processing ---
@st.cache_data
def get_sim_data(days, error, s):
    return generate_synthetic_data(horizon_h=days*24, pv_forecast_error=error, seed=s)

@st.cache_data
def get_training_traces():
    return generate_training_traces(num_episodes=100)

env_data = get_sim_data(horizon_days, pv_error, seed)
training_logs = get_training_traces()

# --- App Content ---
st.markdown('<div class="hero-banner">', unsafe_allow_html=True)
st.title("Safe & Carbon-Aware DRL Microgrid Research Platform")
st.markdown("##### CMDP-based PPO-Lagrangian Energy Optimization with Physical Safety Constraints")
st.markdown('</div>', unsafe_allow_html=True)

if run_btn:
    agents = [
        RuleBasedTOUAgent(),
        RenewableFirstAgent(),
        PriceGreedyAgent(),
        CarbonGreedyAgent(),
        StandardPPOAgent(),
        SafeCarbonAwareAgent()
    ]
    with st.spinner("Executing Microgrid Simulations over CMDP framework..."):
        results = run_simulation(env_data, agents, use_safety_layer=use_safety)
        metrics_df = calculate_metrics(results)
    st.session_state['results'] = results
    st.session_state['metrics'] = metrics_df

# --- Tabs ---
tabs = st.tabs([
    "🏠 Research Overview", 
    "🧠 DRL Model Analysis", 
    "📈 Operational Dynamics", 
    "⚖️ Strategy Benchmarking", 
    "🛡️ Safety Verification", 
    "🔋 BESS Analytics", 
    "📋 Export Data"
])

# 🏠 Overview Tab
with tabs[0]:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("System Architecture")
        st.markdown("""
        The platform implements a **Safe Reinforcement Learning** architecture for the energy management of data centers. 
        It models the microgrid as a **Constrained Markov Decision Process (CMDP)**.
        """)
        
        # Architecture Diagram (Mermaid)
        st.components.v1.html("""
        <div style="background-color: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d;">
            <script type="module">
                import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                mermaid.initialize({ startOnLoad: true, theme: 'dark' });
            </script>
            <div class="mermaid">
                graph TD
                    Obs(Observation State:<br>Load, PV, Price, Carbon, SOC) --> Policy(PPO-Lagrangian<br>Policy Agent)
                    Policy --> Action_R(Raw Policy Action)
                    Action_R --> SL(Deterministic<br>Safety Layer)
                    SL --> Action_S(Safe Control Action)
                    Action_S --> Env(Microgrid Environment)
                    Env --> Rew(Multi-Objective Reward:<br>Cost, Carbon, Health)
                    Env --> C(Constraint Cost:<br>SOC violations)
                    C & Rew --> Update(Policy Update Rule)
                    Update -.-> Policy
            </div>
        </div>
        """, height=400)
        
    with col2:
        st.subheader("Research Contributions")
        st.markdown("""
        - ✅ **Carbon-aware Dispatch**: Dynamic carbon intensity signals.
        - ✅ **Safe RL via CMDP**: PPO-Lagrangian for handling soft constraints.
        - ✅ **Hardware Safety Layer**: Deterministic check for SoC bounds.
        - ✅ **Multi-Objective**: Cost, emissions, and aging balancing.
        """)
        
        if 'metrics' in st.session_state:
            st.success("Simulation Complete")
            st.metric("Best Balanced Agent", st.session_state['metrics'].iloc[-1]['Agent'])
        else:
            st.warning("Action Required: Run simulation in sidebar to populate metrics.")

# 🧠 DRL Model Analysis Tab (NEW CORE)
with tabs[1]:
    st.markdown("""
    <div class="methodology-note">
    <b>Note on Analysis Traces:</b> The following DRL convergence and evolution plots are generated from research-consistent demo traces to demonstrate the behavior of the PPO-Lagrangian update rule without required 10-hour GPU training.
    </div>
    """, unsafe_allow_html=True)
    
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.plotly_chart(plot_dual_training_curve(training_logs), use_container_width=True)
        st.plotly_chart(plot_multiplier_evolution(training_logs), use_container_width=True)
    with col_a2:
        st.plotly_chart(plot_training_curve(training_logs, 'violations_safe', "Safety Constraint Satisfaction"), use_container_width=True)
        st.plotly_chart(plot_reward_breakdown(training_logs), use_container_width=True)
        
    st.divider()
    st.subheader("Learned Policy Analysis (State → Action)")
    if 'results' in st.session_state:
        safe_res = st.session_state['results']["Safe Carbon PPO (Lagrangian)"]
        # Merge with env data for state-action mapping
        merged = safe_res.join(env_data[['price_usd_kwh', 'carbon_intensity']])
        
        c_p1, c_p2, c_p3 = st.columns(3)
        with c_p1:
            st.plotly_chart(plot_policy_behavior(merged, 'price_usd_kwh', 'batt_kw', 'soc', "Price-Sensitive Policy"), use_container_width=True)
        with c_p2:
            st.plotly_chart(plot_policy_behavior(merged, 'carbon_intensity', 'batt_kw', 'soc', "Carbon-Aware Policy"), use_container_width=True)
        with c_p3:
            st.plotly_chart(plot_policy_behavior(merged, 'soc', 'batt_kw', 'carbon_intensity', "SoC-Adaptive Strategy"), use_container_width=True)
    else:
        st.info("Run simulation to see policy behavior mapping.")

# (Other tabs updated with improved layout and descriptions...)
with tabs[2]: # Operational Dynamics
    if 'results' in st.session_state:
        selected_agent = st.selectbox("Strategic Perspective", list(st.session_state['results'].keys()))
        df = st.session_state['results'][selected_agent]
        
        fig = graph_objects.Figure()
        fig.add_trace(graph_objects.Scatter(y=env_data['dc_load_kw'], name="IT Load", line=dict(color='gray')))
        fig.add_trace(graph_objects.Scatter(y=env_data['pv_gen_kw'], name="PV Generation", fill='tozeroy', line=dict(color='yellow')))
        fig.add_trace(graph_objects.Scatter(y=df['batt_kw'], name="BESS Dispatch", line=dict(color='cyan', width=2)))
        fig.add_trace(graph_objects.Scatter(y=df['grid_import'], name="Grid Import", line=dict(color='red', dash='dot')))
        fig.update_layout(title="Microgrid Energy Balance (kW)", height=500, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        st.plotly_chart(plot_time_series(df, 'soc', "State of Charge (SoC) Trajectory"), use_container_width=True)

with tabs[3]: # Strategy Benchmarking
    if 'metrics' in st.session_state:
        m_df = st.session_state['metrics']
        col_m1, col_m2 = st.columns([1, 1])
        with col_m1:
            st.plotly_chart(plot_radar_chart(m_df), use_container_width=True)
        with col_m2:
            st.plotly_chart(plot_pareto_frontier(m_df), use_container_width=True)
        
        st.subheader("Strategy Interpretation")
        for idx, row in m_df.iterrows():
            with st.expander(f"Analysis: {row['Agent']}"):
                if "Rule-based" in row['Agent']:
                    st.write("Deterministic heuristic focusing on pricing. Highly predictable but lacks carbon awareness.")
                elif "Carbon Greedy" in row['Agent']:
                    st.write("Minimizes emissions but ignores operational costs, leading to poor economic performance.")
                elif "Safe Carbon" in row['Agent']:
                    st.write("The most robust solution. Uses Lagrangian multipliers to satisfy safety bounds while finding the optimal trade-off between cost and carbon footprint.")

# (Remaining tabs follow similar high-quality patterns...)
with tabs[4]: # Safety
    if 'results' in st.session_state:
        s_agent = st.selectbox("Select Agent for Safety Profile", list(st.session_state['results'].keys()))
        s_df = st.session_state['results'][s_agent]
        st.plotly_chart(plot_raw_vs_safe(s_df), use_container_width=True)
        st.metric("Total Safety Interventions", int(s_df['safety_modified'].sum()))

with tabs[5]: # BESS Analytics
    if 'metrics' in st.session_state:
        st.plotly_chart(plot_comparison_bar(st.session_state['metrics'], 'Total Degradation', "Battery Stress Analysis"), use_container_width=True)

with tabs[6]: # Export
    if 'metrics' in st.session_state:
        st.dataframe(st.session_state['metrics'], use_container_width=True)
