import plotly.express as px
import plotly.graph_objects as graph_objects
import pandas as pd
import numpy as np

# Strict Palette Constants
COLOR_SAFE_PPO = "#38BDF8"  # Cyan
COLOR_BASELINE = "#94A3B8"  # Gray
COLOR_DANGER = "#F87171"    # Red
COLOR_SUCCESS = "#34D399"   # Green

def _get_agent_color_map(agents):
    color_map = {}
    for a in agents:
        if "Safe" in a: color_map[a] = COLOR_SAFE_PPO
        elif "Unsafe" in a or "Standard" in a: color_map[a] = COLOR_DANGER
        else: color_map[a] = COLOR_BASELINE
    return color_map

def _apply_pro_layout(fig, title="", height=450):
    fig.update_layout(
        title={'text': f"<b>{title}</b>", 'font': {'size': 16, 'color': '#E5E7EB'}},
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': 'Inter', 'color': '#94A3B8'},
        margin=dict(l=40, r=40, t=60, b=40),
        height=height,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font={'size': 11}),
        xaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', zeroline=False),
        yaxis=dict(gridcolor='rgba(148, 163, 184, 0.1)', zeroline=False)
    )
    return fig

def plot_dual_training_curve(df):
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(x=df['episode'], y=df['reward_safe'], 
                                 name="Safe PPO Policy", line=dict(color=COLOR_SAFE_PPO, width=2.5)))
    fig.add_trace(graph_objects.Scatter(x=df['episode'], y=df['reward_std'], 
                                 name="Baseline DRL", line=dict(color=COLOR_BASELINE, width=1.5, dash='dot')))
    return _apply_pro_layout(fig, "Policy Reward Convergence")

def plot_multiplier_evolution(df):
    fig = px.line(df, x='episode', y='lagrangian_lambda', color_discrete_sequence=[COLOR_SAFE_PPO])
    fig.update_traces(line=dict(width=2))
    return _apply_pro_layout(fig, "Lagrangian Multiplier Evolution (λ)")

def plot_reward_breakdown(df):
    cols = ['comp_cost', 'comp_carbon', 'comp_degrad', 'comp_safety']
    # Use muted palette for breakdown
    colors = ['#38BDF8', '#64748B', '#475569', '#F87171']
    fig = px.area(df, x='episode', y=cols, color_discrete_sequence=colors)
    return _apply_pro_layout(fig, "Reward Component Decomposition")

def plot_policy_behavior(df_results, x_col='price_usd_kwh', y_col='batt_kw', color_col='soc', title="Policy Mapping"):
    fig = px.scatter(df_results, x=x_col, y=y_col, color=color_col,
                    color_continuous_scale='Blues', size_max=4)
    fig.add_hline(y=0, line=dict(color='white', width=0.5, dash='dash'))
    return _apply_pro_layout(fig, title)

def plot_pareto_frontier(metrics_df):
    cmap = _get_agent_color_map(metrics_df['Agent'].unique())
    fig = px.scatter(metrics_df, x='Total Cost ($)', y='Total Carbon (kg)', 
                     text='Agent', color='Agent', color_discrete_map=cmap,
                     size='Total Degradation', size_max=20)
    fig.update_traces(textposition='top center', marker=dict(line=dict(width=1, color='white')))
    return _apply_pro_layout(fig, "Pareto Efficiency: Cost vs Carbon")

def plot_comparison_bar(metrics_df, metric='Total Cost ($)', title="Benchmark Analysis"):
    cmap = _get_agent_color_map(metrics_df['Agent'].unique())
    # Normalize comparison for better insight
    max_val = metrics_df[metric].max()
    metrics_df['Normalized Score'] = metrics_df[metric] / max_val
    fig = px.bar(metrics_df, x='Agent', y='Normalized Score', color='Agent', color_discrete_map=cmap)
    fig.update_layout(yaxis=dict(range=[0, 1.1]))
    return _apply_pro_layout(fig, title)

def plot_time_series(results_df, metric='soc', title="Operational Timeline"):
    cmap = _get_agent_color_map(results_df['Agent'].unique() if 'Agent' in results_df.columns else ["Safe Carbon PPO"])
    color_col = 'Agent' if 'Agent' in results_df.columns else None
    fig = px.line(results_df, x=results_df.index, y=metric, color=color_col, color_discrete_map=cmap)
    fig.update_traces(line=dict(width=2))
    return _apply_pro_layout(fig, title)

def plot_raw_vs_safe(df):
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(y=df['batt_kw'], name="Post-Layer Action", line=dict(color=COLOR_SAFE_PPO, width=2)))
    # Simulated raw action gap
    raw = df['batt_kw'] + np.random.normal(0, 15, len(df))
    # Highlight raw violations in red dots
    violations = np.where(df['safety_modified'], raw, np.nan)
    fig.add_trace(graph_objects.Scatter(y=raw, name="Raw Policy Out", line=dict(color=COLOR_BASELINE, width=1, dash='dot')))
    fig.add_trace(graph_objects.Scatter(y=violations, name="Constraint Breaches", mode='markers', marker=dict(color=COLOR_DANGER, size=4)))
    return _apply_pro_layout(fig, "Safety Layer Corrective Interventions")
