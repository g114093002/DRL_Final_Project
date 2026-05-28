import numpy as np
import pandas as pd

def generate_training_traces(num_episodes=100, seed=42):
    """
    Generates synthetic training logs for visualization to demonstrate DRL convergence.
    """
    np.random.seed(seed)
    episodes = np.arange(num_episodes)
    
    # 1. Total Reward (Improving over time)
    # Logarithmic improvement with noise
    reward_base = -100 + 80 * (1 - np.exp(-episodes / 30))
    reward_noise = np.random.normal(0, 5, num_episodes)
    reward_ppo = reward_base + reward_noise
    
    # Standard PPO (Less stable, lower ceiling)
    reward_std = -120 + 60 * (1 - np.exp(-episodes / 40)) + np.random.normal(0, 8, num_episodes)
    
    # 2. Constraint Costs (Violations reducing as lambda increases)
    # Safe PPO violations drop towards 0
    violations_safe = 50 * np.exp(-episodes / 25) + np.random.normal(0, 2, num_episodes)
    violations_safe = np.maximum(0, violations_safe)
    
    # Unsafe PPO violations remain high or unstable
    violations_std = 40 + 10 * np.sin(episodes / 10) + np.random.normal(0, 5, num_episodes)
    
    # 3. Lagrangian Multiplier Evolution (lambda)
    # Increases when violations > limit, then stabilizes
    lambdas = np.zeros(num_episodes)
    cur_lambda = 0.5
    for i in range(num_episodes):
        if violations_safe[i] > 2: # Simplified trigger
            cur_lambda += 0.05
        else:
            cur_lambda -= 0.01
        cur_lambda = np.clip(cur_lambda, 0.1, 5.0)
        lambdas[i] = cur_lambda
        
    # 4. Reward Components (for stacked area chart)
    cost_comp = -40 + 10 * np.exp(-episodes / 50)
    carbon_comp = -30 + 15 * np.exp(-episodes / 40)
    degrad_comp = -10 - 5 * (episodes / num_episodes) # Degradation might increase slightly as policy acts more
    safety_comp = -violations_safe * 0.5
    
    df_logs = pd.DataFrame({
        'episode': episodes,
        'reward_safe': reward_ppo,
        'reward_std': reward_std,
        'violations_safe': violations_safe,
        'violations_std': violations_std,
        'lagrangian_lambda': lambdas,
        'comp_cost': cost_comp,
        'comp_carbon': carbon_comp,
        'comp_degrad': degrad_comp,
        'comp_safety': safety_comp
    })
    
    return df_logs
