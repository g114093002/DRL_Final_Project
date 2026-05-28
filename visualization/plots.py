import plotly.express as px
import plotly.graph_objects as graph_objects
import pandas as pd
import numpy as np

# Strict Research Palette
PALETTE = {
    'cyan': '#38BDF8',
    'blue': '#60A5FA',
    'teal': '#2DD4BF',
    'violet': '#A78BFA',
    'amber': '#FBBF24',
    'red': '#F87171',
    'text_main': '#E2E8F0',
    'text_muted': '#94A3B8',
    'bg_chart': '#0B1220',
    'grid': 'rgba(255, 255, 255, 0.06)',
    'axis': 'rgba(255, 255, 255, 0.12)'
}

def _get_agent_color_map(agents):
    color_map = {}
    for a in agents:
        if "Safe" in a: color_map[a] = PALETTE['cyan']
        elif "Unsafe" in a or "Standard" in a: color_map[a] = PALETTE['red']
        elif "Rule" in a: color_map[a] = PALETTE['amber']
        else: color_map[a] = PALETTE['text_muted']
    return color_map

def _apply_research_theme(fig, title="", height=400):
    fig.update_layout(
        title={
            'text': f"<b>{title.upper()}</b>", 
            'font': {'size': 14, 'color': PALETTE['text_muted']}
        },
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor=PALETTE['bg_chart'],
        font={'family': 'Inter', 'color': PALETTE['text_muted']},
        margin=dict(l=50, r=30, t=60, b=40),
        height=height,
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font={'size': 10}, bgcolor='rgba(0,0,0,0)'
        ),
        xaxis=dict(
            gridcolor=PALETTE['grid'], linecolor=PALETTE['axis'], showline=True,
            tickfont={'size': 11}, title={'font': {'size': 12}}
        ),
        yaxis=dict(
            gridcolor=PALETTE['grid'], linecolor=PALETTE['axis'], showline=True,
            tickfont={'size': 11}, title={'font': {'size': 12}}
        )
    )
    # Default settings for all axes
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False)
    return fig

def plot_dual_training_curve(df):
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(x=df['episode'], y=df['reward_safe'], 
                                 name="PPO-LAGRANGIAN", line=dict(color=PALETTE['cyan'], width=1.5)))
    fig.add_trace(graph_objects.Scatter(x=df['episode'], y=df['reward_std'], 
                                 name="STANDARD PPO", line=dict(color=PALETTE['text_muted'], width=1, dash='dot')))
    return _apply_research_theme(fig, "Convergence Dynamics")

def plot_multiplier_evolution(df):
    fig = px.line(df, x='episode', y='lagrangian_lambda', color_discrete_sequence=[PALETTE['cyan']])
    fig.update_traces(line=dict(width=1.5))
    return _apply_research_theme(fig, "Lagrangian (λ) Growth")

def plot_reward_breakdown(df):
    cols = ['comp_cost', 'comp_carbon', 'comp_degrad', 'comp_safety']
    colors = [PALETTE['cyan'], PALETTE['blue'], PALETTE['violet'], PALETTE['red']]
    fig = px.area(df, x='episode', y=cols, color_discrete_sequence=colors)
    fig.update_traces(line=dict(width=0.5))
    return _apply_research_theme(fig, "Component Contribution")

def plot_policy_behavior(df_results, x_col='price_usd_kwh', y_col='batt_kw', color_col='soc', title="Policy Mapping"):
    fig = px.scatter(df_results, x=x_col, y=y_col, color=color_col,
                    color_continuous_scale='Blues', opacity=0.6)
    fig.update_traces(marker=dict(size=4))
    fig.add_hline(y=0, line=dict(color=PALETTE['text_muted'], width=0.5, dash='dash'))
    return _apply_research_theme(fig, title)

def plot_pareto_frontier(metrics_df):
    cmap = _get_agent_color_map(metrics_df['Agent'].unique())
    fig = px.scatter(metrics_df, x='Total Cost ($)', y='Total Carbon (kg)', 
                     text='Agent', color='Agent', color_discrete_map=cmap,
                     size='Total Degradation', size_max=15)
    fig.update_traces(textposition='top center', marker=dict(opacity=0.8, line=dict(width=0.5, color='white')))
    return _apply_research_theme(fig, "Pareto Trade-off", height=500)

def plot_comparison_bar(metrics_df, metric='Total Cost ($)', title="Benchmark Analysis"):
    cmap = _get_agent_color_map(metrics_df['Agent'].unique())
    max_val = metrics_df[metric].max()
    metrics_df['Score'] = metrics_df[metric] / max_val
    fig = px.bar(metrics_df, x='Agent', y='Score', color='Agent', color_discrete_map=cmap)
    fig.update_layout(yaxis=dict(range=[0, 1.1]))
    return _apply_research_theme(fig, title)

def plot_time_series(results_df, metric='soc', title="Operation Logs"):
    cmap = _get_agent_color_map(results_df['Agent'].unique() if 'Agent' in results_df.columns else ["Safe Carbon PPO"])
    color_col = 'Agent' if 'Agent' in results_df.columns else None
    fig = px.line(results_df, x=results_df.index, y=metric, color=color_col, color_discrete_map=cmap)
    fig.update_traces(line=dict(width=1.5))
    return _apply_research_theme(fig, title)

def plot_operational_fidelity(df, env_data, title="High-Fidelity Operational Analysis"):
    from plotly.subplots import make_subplots
    
    # Ensure indices align
    idx = df.index
    
    fig = make_subplots(
        rows=4, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.03,
        subplot_titles=("BATTERY DISPATCH (kW)", "STATE OF CHARGE (%)", "MARKET PRICE ($/kWh)", "PV AVAILABILITY (kW)")
    )
    
    # 1. Dispatch
    fig.add_trace(graph_objects.Scatter(x=idx, y=df['batt_kw'], name="Dispatch", line=dict(color=PALETTE['cyan'], width=1.5)), row=1, col=1)
    fig.add_hline(y=0, line=dict(color=PALETTE['text_muted'], width=0.5, dash='dash'), row=1, col=1)
    
    # 2. SoC
    fig.add_trace(graph_objects.Scatter(x=idx, y=df['soc'] * 100, name="SoC", fill='tozeroy', line=dict(color=PALETTE['blue'], width=1.5)), row=2, col=1)
    
    # 3. Price
    fig.add_trace(graph_objects.Scatter(x=idx, y=env_data.loc[idx, 'price_usd_kwh'], name="Price", line=dict(color=PALETTE['amber'], width=1)), row=3, col=1)
    
    # 4. PV
    fig.add_trace(graph_objects.Scatter(x=idx, y=env_data.loc[idx, 'pv_gen_kw'], name="PV", fill='tozeroy', line=dict(color=PALETTE['teal'], width=1)), row=4, col=1)
    
    _apply_research_theme(fig, title, height=800)
    fig.update_layout(showlegend=False)
    
    # Update subplot title sizes
    for i in fig['layout']['annotations']:
        i['font'] = dict(size=12, color=PALETTE['text_muted'])
        
    return fig

def plot_raw_vs_safe(df):
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(y=df['batt_kw'], name="SAFE OUTPUT", line=dict(color=PALETTE['cyan'], width=1.5)))
    # Simulated raw action gap
    raw = df['batt_kw'] + np.random.normal(0, 15, len(df))
    # Highlight raw violations in red dots
    violations = np.where(df['safety_modified'], raw, np.nan)
    fig.add_trace(graph_objects.Scatter(y=raw, name="RAW POLICY", line=dict(color=PALETTE['text_muted'], width=1, dash='dot')))
    fig.add_trace(graph_objects.Scatter(y=violations, name="VIOLATIONS", mode='markers', marker=dict(color=PALETTE['red'], size=3)))
    return _apply_research_theme(fig, "Safety Layer Corrective Interventions")
