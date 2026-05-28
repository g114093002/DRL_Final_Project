import streamlit as st
import pandas as pd
import numpy as np
from data.synthetic_data import generate_synthetic_data
from agents.rule_based import RuleBasedTOUAgent
from agents.renewable_first import RenewableFirstAgent
from agents.greedy import PriceGreedyAgent, CarbonGreedyAgent
from agents.standard_ppo import StandardPPOAgent
from agents.safe_carbon_agent import SafeCarbonAwareAgent
from evaluation.simulator import run_simulation, calculate_metrics
from visualization.plots import *
from visualization.styles import apply_custom_styles
from config import *

# Page Config
st.set_page_config(page_title="Safe Carbon Microgrid Demo", layout="wide", initial_sidebar_state="expanded")
apply_custom_styles()

st.title("🔋 Safe & Carbon-Aware Microgrid Energy Management")
st.markdown("### Deep Reinforcement Learning for Data Center Behind-the-Meter Optimization")

# Sidebar
with st.sidebar:
    st.header("Simulation Control")
    horizon_days = st.slider("Simulation Horizon (Days)", 1, 7, 7)
    pv_error = st.slider("PV Forecast Error (%)", 0, 50, 20) / 100.0
    use_safety = st.checkbox("Enable Safety Layer", value=True)
    
    st.header("Reward Weights")
    w_cost = st.slider("Cost Weight", 0.0, 10.0, WEIGHT_COST)
    w_carbon = st.slider("Carbon Weight", 0.0, 10.0, WEIGHT_CARBON)
    w_degrad = st.slider("Degradation Weight", 0.0, 10.0, WEIGHT_DEGRADATION)
    
    run_btn = st.button("🚀 Run Simulation", type="primary", use_container_width=True)

# Data generation (Cached)
@st.cache_data
def get_data(days, error, seed=42):
    return generate_synthetic_data(horizon_h=days*24, pv_forecast_error=error, seed=seed)

env_data = get_data(horizon_days, pv_error)

if run_btn:
    # Initialize agents
    agents = [
        RuleBasedTOUAgent(),
        RenewableFirstAgent(),
        PriceGreedyAgent(),
        CarbonGreedyAgent(),
        StandardPPOAgent(),
        SafeCarbonAwareAgent()
    ]
    
    with st.spinner("Running simulations..."):
        results = run_simulation(env_data, agents, use_safety_layer=use_safety)
        metrics_df = calculate_metrics(results)
    
    # Store in session state
    st.session_state['results'] = results
    st.session_state['metrics'] = metrics_df

# Tab System
if 'results' in st.session_state:
    results = st.session_state['results']
    metrics_df = st.session_state['metrics']
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Overview", "📈 Time-Series", "⚔️ Comparison", "🛡️ Safety Layer", "🌱 Carbon Insights", "🔋 Battery Health", "📋 Raw Data"
    ])
    
    with tab1:
        st.subheader("Project Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        # Find best agents
        best_cost_agent = metrics_df.loc[metrics_df['Total Cost ($)'].idxmin(), 'Agent']
        best_carbon_agent = metrics_df.loc[metrics_df['Total Carbon (kg)'].idxmin(), 'Agent']
        safest_agent = metrics_df.loc[metrics_df['SoC Violations'].idxmin(), 'Agent']
        
        col1.metric("Lowest Cost", best_cost_agent)
        col2.metric("Lowest Carbon", best_carbon_agent)
        col3.metric("Safest Policy", safest_agent)
        col4.metric("Avg Renewable Use", f"{metrics_df['Renewable Utilization (%)'].mean():.1f}%")
        
        st.markdown("---")
        st.table(metrics_df.style.highlight_min(subset=['Total Cost ($)', 'Total Carbon (kg)', 'SoC Violations'], color='#006400')
                 .highlight_max(subset=['Carbon Savings (%)'], color='#006400'))
        
        st.info("The Safe Carbon PPO Agent balances multiple objectives using Lagrangian penalties and a deterministic safety layer.")

    with tab2:
        st.subheader("Operational Time-Series")
        selected_agent = st.selectbox("Select Agent to View", list(results.keys()))
        df_agent = results[selected_agent]
        
        # Combine necessary data for multi-line plot if needed, but here we just show agent-specific
        fig_p = graph_objects.Figure()
        fig_p.add_trace(graph_objects.Scatter(y=env_data['dc_load_kw'], name="IT Load (kW)", line=dict(color='gray', dash='dot')))
        fig_p.add_trace(graph_objects.Scatter(y=env_data['pv_gen_kw'], name="PV Gen (kW)", line=dict(color='yellow')))
        fig_p.add_trace(graph_objects.Scatter(y=df_agent['batt_kw'], name="Battery Power (kW)", line=dict(color='cyan')))
        fig_p.add_trace(graph_objects.Scatter(y=df_agent['grid_import'], name="Grid Import (kW)", line=dict(color='red')))
        fig_p.update_layout(title=f"Power Balance - {selected_agent}", template="plotly_dark")
        st.plotly_chart(fig_p, use_container_width=True)
        
        st.plotly_chart(plot_time_series(df_agent, 'soc', f"State of Charge (SoC) - {selected_agent}"), use_container_width=True)

    with tab3:
        st.subheader("Performance Metrics Comparison")
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(plot_comparison_bar(metrics_df, 'Total Cost ($)', "Total Electricity Cost"), use_container_width=True)
            st.plotly_chart(plot_comparison_bar(metrics_df, 'Total Carbon (kg)', "Total Carbon Footprint"), use_container_width=True)
        with c2:
            st.plotly_chart(plot_comparison_bar(metrics_df, 'Total Degradation', "Battery Degradation Score"), use_container_width=True)
            st.plotly_chart(plot_radar_chart(metrics_df), use_container_width=True)

    with tab4:
        st.subheader("Safety Layer Analysis")
        st.markdown("The safety layer intercepts and corrects agent actions that would violate physical or operational constraints.")
        
        selected_agent_s = st.selectbox("Select Agent", list(results.keys()), key="safety_sel")
        df_s = results[selected_agent_s]
        
        # Modified actions count
        interventions = df_s['safety_modified'].sum()
        st.metric("Safety Interventions", int(interventions), f"{interventions/len(df_s)*100:.1f}% of total steps")
        
        # Histogram of reasons
        reasons = [r for sublist in df_s['safety_reason'] for r in sublist]
        if reasons:
            reason_df = pd.Series(reasons).value_counts().reset_index()
            reason_df.columns = ['Reason', 'Count']
            st.plotly_chart(px.bar(reason_df, x='Reason', y='Count', title="Intervention Reasons", template="plotly_dark"))
        else:
            st.success("No safety interventions recorded.")

    with tab5:
        st.subheader("Carbon-Aware Analysis")
        st.plotly_chart(plot_carbon_vs_price(env_data), use_container_width=True)
        
        st.markdown("#### Carbon Intensity Heatmap")
        carbon_matrix = env_data['carbon_intensity'].values.reshape(-1, 24)
        fig_h = px.imshow(carbon_matrix, labels=dict(x="Hour", y="Day", color="Carbon"),
                         x=list(range(24)), title="Typical Weekly Carbon Pattern")
        fig_h.update_layout(template="plotly_dark")
        st.plotly_chart(fig_h, use_container_width=True)

    with tab6:
        st.subheader("Battery Health & Degradation")
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.plotly_chart(plot_comparison_bar(metrics_df, 'Total Degradation', "Cumulative BESS Stress"), use_container_width=True)
        with col_h2:
            # SoC distribution
            soc_data = pd.concat([results[a]['soc'].rename(a) for a in results], axis=1)
            st.plotly_chart(px.box(soc_data, title="SoC Distribution by Strategy", template="plotly_dark"), use_container_width=True)

    with tab7:
        st.subheader("Raw Simulation Data")
        st.dataframe(metrics_df)
        st.write("First 100 steps of selected agent:")
        st.dataframe(results[selected_agent].head(100))
        
        csv = metrics_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Metrics CSV", csv, "metrics.csv", "text/csv")
else:
    # Landing message
    st.info("👈 Click **Run Simulation** in the sidebar to start the demo.")
    st.markdown("""
    ### Methods Overview:
    * **Rule-based TOU**: Simple time-of-use pricing logic.
    * **Renewable First**: Prioritizes local PV self-consumption.
    * **Price Greedy**: Aggressive cost minimization ignoring carbon.
    * **Carbon Greedy**: Minimizes carbon footprint ignoring cost.
    * **Safe Carbon PPO**: Multi-objective reinforcement learning with safety constraints.
    """)
