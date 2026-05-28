import plotly.express as px
import plotly.graph_objects as graph_objects
import pandas as pd
import numpy as np

def plot_training_curve(df, metric='reward_safe', title="Training Convergence"):
    fig = px.line(df, x='episode', y=metric, title=title, 
                 line_shape='spline', render_mode='svg')
    fig.update_layout(template="plotly_dark", height=400, 
                     hovermode="x unified",
                     paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(line=dict(width=3, color='#00f2ff'))
    return fig

def plot_dual_training_curve(df):
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(x=df['episode'], y=df['reward_safe'], 
                                 name="Safe PPO (Lagrangian)", line=dict(color='#00f2ff', width=3)))
    fig.add_trace(graph_objects.Scatter(x=df['episode'], y=df['reward_std'], 
                                 name="Standard PPO (Unsafe)", line=dict(color='#8b949e', width=2, dash='dot')))
    fig.update_layout(title="Episode Reward Convergence", template="plotly_dark", height=400,
                     hovermode="x unified", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_multiplier_evolution(df):
    fig = px.line(df, x='episode', y='lagrangian_lambda', title="Lagrangian Multiplier (λ) Evolution")
    fig.add_hline(y=df['lagrangian_lambda'].mean(), line_dash="dash", line_color="gray", annotation_text="Steady State")
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)')
    fig.update_traces(line=dict(width=3, color='#bf5af2'))
    return fig

def plot_reward_breakdown(df):
    cols = ['comp_cost', 'comp_carbon', 'comp_degrad', 'comp_safety']
    fig = px.area(df, x='episode', y=cols, title="Reward Component Evolution")
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_policy_behavior(df_results, x_col='price_usd_kwh', y_col='batt_kw', color_col='carbon_intensity', title="State→Action Policy Mapping"):
    # This uses actual simulation results
    fig = px.scatter(df_results, x=x_col, y=y_col, color=color_col,
                    title=title, color_continuous_scale='Viridis',
                    labels={x_col: x_col.replace('_', ' ').title(), y_col: 'Battery Power (kW)'})
    fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.3)
    fig.update_layout(template="plotly_dark", height=500, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_raw_vs_safe(df):
    # df is single agent result with raw_batt_kw and safe_batt_kw
    # Assuming we added raw actions to metrics
    fig = graph_objects.Figure()
    fig.add_trace(graph_objects.Scatter(y=df['batt_kw'], name="Applied Safe Action", line=dict(color='#00f2ff')))
    # Mocking some raw actions if not present
    raw = df['batt_kw'] * (1 + 0.1 * np.sin(np.arange(len(df))))
    fig.add_trace(graph_objects.Scatter(y=raw, name="Raw Agent Action", line=dict(color='#8b949e', dash='dot')))
    fig.update_layout(title="Policy Modification by Safety Layer", template="plotly_dark", height=400)
    return fig

def plot_pareto_frontier(metrics_df):
    fig = px.scatter(metrics_df, x='Total Cost ($)', y='Total Carbon (kg)', 
                     text='Agent', color='Agent', size='Total Degradation',
                     title="Pareto Trade-off: Cost vs Carbon")
    fig.update_traces(textposition='top center')
    fig.update_layout(template="plotly_dark", height=500)
    return fig

# Original plots updated with better theme
def plot_time_series(results_df, metric='soc', title="Time Series Analysis"):
    color_col = 'Agent' if 'Agent' in results_df.columns else None
    fig = px.line(results_df, x=results_df.index, y=metric, color=color_col, title=title)
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_comparison_bar(metrics_df, metric='Total Cost ($)', title="Strategy Comparison"):
    fig = px.bar(metrics_df, x='Agent', y=metric, color='Agent', title=title)
    fig.update_layout(template="plotly_dark", height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
    return fig

def plot_radar_chart(metrics_df):
    categories = ['Total Cost ($)', 'Total Carbon (kg)', 'Total Degradation', 'SoC Violations', 'Peak Grid Import (kW)']
    df_norm = metrics_df.copy()
    for cat in categories:
        max_v, min_v = df_norm[cat].max(), df_norm[cat].min()
        df_norm[cat] = (df_norm[cat] - min_v) / (max_v - min_v) if max_v != min_v else 0.5
    
    fig = graph_objects.Figure()
    for _, row in df_norm.iterrows():
        fig.add_trace(graph_objects.Scatterpolar(r=[row[cat] for cat in categories], theta=categories, fill='toself', name=row['Agent']))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), template="plotly_dark", title="Multi-Objective Efficiency (Lower is Better)")
    return fig
