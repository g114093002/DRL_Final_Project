import pandas as pd
import numpy as np
from env.microgrid_env import MicrogridEnv

def run_simulation(env_data, agents, use_safety_layer=True):
    results = {}
    
    for agent in agents:
        env = MicrogridEnv(env_data, use_safety_layer=use_safety_layer)
        obs, _ = env.reset()
        done = False
        
        history = []
        while not done:
            action = agent.select_action(obs)
            obs, reward, terminated, truncated, info = env.step(action)
            history.append(info)
            done = terminated or truncated
            
        results[agent.name] = pd.DataFrame(history)
        
    return results

def calculate_metrics(results):
    metrics_list = []
    for agent_name, df in results.items():
        m = {
            "Agent": agent_name,
            "Total Cost ($)": df['cost'].sum(),
            "Total Carbon (kg)": df['carbon'].sum(),
            "Total Degradation": df['degradation'].sum(),
            "SoC Violations": (df['soc_violation'] > 0).sum(),
            "Safety Interventions": df['safety_modified'].sum(),
            "Avg SoC": df['soc'].mean(),
            "Peak Grid Import (kW)": df['grid_import'].max(),
            "Renewable Utilization (%)": (1 - df['grid_export'].sum() / df['batt_kw'].abs().sum() * 0.1) * 100 # Dummy logic
        }
        # Normalize renewable utilization
        m["Renewable Utilization (%)"] = np.clip(m["Renewable Utilization (%)"], 0, 100)
        metrics_list.append(m)
    
    metrics_df = pd.DataFrame(metrics_list)
    # Calculate savings vs baseline (first agent)
    baseline_cost = metrics_df.iloc[0]["Total Cost ($)"]
    baseline_carbon = metrics_df.iloc[0]["Total Carbon (kg)"]
    
    metrics_df["Cost Savings (%)"] = (baseline_cost - metrics_df["Total Cost ($)"]) / baseline_cost * 100
    metrics_df["Carbon Savings (%)"] = (baseline_carbon - metrics_df["Total Carbon (kg)"]) / baseline_carbon * 100
    
    return metrics_df
