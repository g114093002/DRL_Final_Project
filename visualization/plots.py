import plotly.express as px
import plotly.graph_objects as graph_objects
import pandas as pd

def plot_time_series(results_df, metric='soc', title="Time Series Analysis"):
    # Use color='Agent' only if the column exists
    color_col = 'Agent' if 'Agent' in results_df.columns else None
    fig = px.line(results_df, x=results_df.index, y=metric, color=color_col, title=title)
    fig.update_layout(template="plotly_dark", height=400)
    return fig

def plot_comparison_bar(metrics_df, metric='Total Cost ($)', title="Strategy Comparison"):
    fig = px.bar(metrics_df, x='Agent', y=metric, color='Agent', title=title)
    fig.update_layout(template="plotly_dark", height=400)
    return fig

def plot_radar_chart(metrics_df):
    # Normalized radar chart
    categories = ['Total Cost ($)', 'Total Carbon (kg)', 'Total Degradation', 'SoC Violations', 'Peak Grid Import (kW)']
    
    # Scale values to [0, 1] (lower is better for these)
    df_norm = metrics_df.copy()
    for cat in categories:
        max_val = df_norm[cat].max()
        min_val = df_norm[cat].min()
        if max_val != min_val:
            df_norm[cat] = (df_norm[cat] - min_val) / (max_val - min_val)
        else:
            df_norm[cat] = 0.5

    fig = graph_objects.Figure()
    for index, row in df_norm.iterrows():
        fig.add_trace(graph_objects.Scatterpolar(
            r=[row[cat] for cat in categories],
            theta=categories,
            fill='toself',
            name=row['Agent']
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        showlegend=True,
        template="plotly_dark",
        title="Strategy Balance (Lower is Better)"
    )
    return fig

def plot_carbon_vs_price(env_data):
    fig = px.scatter(env_data, x='price_usd_kwh', y='carbon_intensity', 
                     color='hour', title="Price vs Carbon Intensity Scatter",
                     labels={'price_usd_kwh': 'Price ($/kWh)', 'carbon_intensity': 'Carbon (kgCO2/kWh)'})
    fig.update_layout(template="plotly_dark")
    return fig
