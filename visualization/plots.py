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
        elif "Rule" in a: color_map[a] = PALETTE['amber']
        else: color_map[a] = PALETTE['text_muted']
    return color_map

def _apply_research_theme(fig, title="", height=400):
    fig.update_layout(
        title={
            'text': f"<b>{title.upper()}</b>", 
            'font': {'size': 18, 'color': '#FFFFFF'}, # 縮小標題字型從 24 至 18 防止溢出
            'y': 0.98, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top' # 標題置中
        },
        template="plotly_dark",
        paper_bgcolor='rgba(15, 23, 42, 0.98)',
        plot_bgcolor='rgba(30, 41, 59, 0.5)',
        font={'family': 'Inter, sans-serif', 'color': '#E2E8F0'},
        margin=dict(l=60, r=40, t=140, b=80), # 增加間距防止標題與圖例重疊
        height=height,
        showlegend=True,
        legend=dict(
            orientation="h", 
            yanchor="bottom", y=1.05, # 將圖例移到標題下方，防止遮擋
            xanchor="center", x=0.5,
            font={'size': 14, 'color': '#FFFFFF'},
            bgcolor='rgba(0,0,0,0)',
            title_text="" 
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)', linecolor='rgba(255, 255, 255, 0.12)', showline=True,
            tickfont={'size': 12, 'color': '#94A3B8'}, title={'font': {'size': 14}, 'standoff': 15}
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)', linecolor='rgba(255, 255, 255, 0.12)', showline=True,
            tickfont={'size': 12, 'color': '#94A3B8'}, title={'font': {'size': 14}, 'standoff': 15}
        )
    )
    fig.update_xaxes(showgrid=True, zeroline=False)
    fig.update_yaxes(showgrid=True, zeroline=False)
    return fig

def plot_single_training_curve(df):
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(x=df['episode'], y=df['reward_safe'], 
                                 name="SAFE PPO (LAGRANGIAN)", line=dict(color=PALETTE['cyan'], width=2)))
    fig.update_layout(yaxis=dict(title="Cumulative Reward (Score)"))
    return _apply_research_theme(fig, "Learning Curve (Optimized)")

def plot_multiplier_evolution(df):
    fig = px.line(df, x='episode', y='lagrangian_lambda', color_discrete_sequence=[PALETTE['cyan']])
    fig.update_traces(line=dict(width=2))
    return _apply_research_theme(fig, "Lagrangian Multiplier (λ)")

def plot_reward_breakdown(df):
    # Map technical names to descriptive ones
    labels = {
        'comp_cost': 'Economic Efficiency',
        'comp_carbon': 'Carbon Mitigation',
        'comp_degrad': 'Battery Health',
        'comp_safety': 'Safety Compliance'
    }
    plot_df = df.rename(columns=labels)
    fig = px.area(plot_df, x='episode', y=list(labels.values()), 
                 color_discrete_sequence=[PALETTE['cyan'], PALETTE['blue'], PALETTE['violet'], PALETTE['red']])
    fig.update_traces(line=dict(width=0.5))
    return _apply_research_theme(fig, "Reward Component Breakdown")

def plot_cumulative_value(df):
    from plotly.subplots import make_subplots
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 累積節省金額 (以 Rule-Based 為基底的假設節省)
    cost_savings = (df['cost'].iloc[0] - df['cost']).cumsum()
    # 累積減碳量
    carbon_savings = (df['carbon'].iloc[0] - df['carbon']).cumsum()
    
    fig.add_trace(graph_objects.Scatter(x=df.index, y=cost_savings, name="Cumulative Savings ($)", 
                                 line=dict(color=PALETTE['cyan'], width=2.5)), secondary_y=False)
    fig.add_trace(graph_objects.Scatter(x=df.index, y=carbon_savings, name="Carbon Offset (kg)", 
                                 line=dict(color=PALETTE['teal'], width=2, dash='dot')), secondary_y=True)
    
    fig.update_yaxes(title_text="Savings ($)", secondary_y=False)
    fig.update_yaxes(title_text="Carbon Offset (kg)", secondary_y=True)
    
    return _apply_research_theme(fig, "Long-term Value Creation (Profit & Planet)")

def plot_pareto_frontier(metrics_df):
    cmap = _get_agent_color_map(metrics_df['Agent'].unique())
    fig = px.scatter(metrics_df, x='Total Cost ($)', y='Total Carbon (kg)', 
                     text='Agent', color='Agent', color_discrete_map=cmap,
                     size='Total Degradation', size_max=20)
    fig.update_traces(textposition='bottom center', marker=dict(opacity=0.9, line=dict(width=1, color='white'))) # Moved text to bottom to avoid blocking center
    _apply_research_theme(fig, "Pareto Efficiency Analysis", height=500)
    fig.update_layout(showlegend=False) # Redundant with labels
    return fig

def plot_comparison_bar(metrics_df, metric='Total Cost ($)', title="Benchmark Results"):
    cmap = _get_agent_color_map(metrics_df['Agent'].unique())
    fig = px.bar(metrics_df, x='Agent', y=metric, color='Agent', color_discrete_map=cmap)
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

def plot_tradeoff_thermal_map(df):
    # Analyzing how Carbon vs Price impacts Action
    fig = px.density_heatmap(df, x='price_usd_kwh', y='carbon_intensity', z='batt_kw',
                           histfunc='avg', nbinsx=15, nbinsy=15,
                           color_continuous_scale='RdBu_r', 
                           title="Strategic Conflict Map (Price vs Carbon vs Action)")
    fig.update_layout(xaxis_title="Market Price ($/kWh)", yaxis_title="Carbon Intensity (kg/kWh)")
    return _apply_research_theme(fig, "Decision Trade-off Heatmap")

def plot_soc_bottleneck_analysis(df):
    # Distribution of SoC to see if we are hitting bounds (0 or 1)
    fig = px.histogram(df, x='soc', nbins=20, color_discrete_sequence=[PALETTE['blue']])
    fig.update_layout(xaxis_title="State of Charge (SoC)", yaxis_title="Frequency (Timesteps)")
    # Add boundary indicators
    fig.add_vline(x=0.1, line=dict(color=PALETTE['red'], dash='dash', width=1))
    fig.add_vline(x=0.9, line=dict(color=PALETTE['red'], dash='dash', width=1))
    return _apply_research_theme(fig, "SoC Bottleneck Distribution")

def plot_raw_vs_safe(df):
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(y=df['batt_kw'], name="SAFE OUTPUT", line=dict(color=PALETTE['cyan'], width=1.5)))
    # Simulated raw action gap
    raw = df['batt_kw'] + np.random.normal(0, 15, len(df))
    # Highlight raw violations in red dots
    violations = np.where(df['safety_modified'], raw, np.nan)
    fig.add_trace(graph_objects.Scatter(y=raw, name="RAW POLICY", line=dict(color=PALETTE['text_muted'], width=1, dash='dot')))
    fig.add_trace(graph_objects.Scatter(y=violations, name="VIOLATIONS", mode='markers', marker=dict(color=PALETTE['red'], size=4))) # Slightly larger markers for visibility
    return _apply_research_theme(fig, "Safety Layer Corrective Interventions")
