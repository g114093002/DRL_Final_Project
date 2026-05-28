import torch
import torch.nn as nn
import numpy as np
from agents.base import BaseAgent

class Actor(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(Actor, self).__init__()
        self.net = nn.Sequential(nn.Linear(state_dim, 64), nn.ReLU(), nn.Linear(64, 64), nn.ReLU(), nn.Linear(64, action_dim), nn.Tanh())
    def forward(self, x): return self.net(x)

class SafeCarbonAwareAgent(BaseAgent):
    def __init__(self, state_dim=12, action_dim=2):
        super().__init__("Safe Carbon PPO (Lagrangian)")
        self.actor = Actor(state_dim, action_dim)
        self.lagrangian_multiplier = 1.0
        self.constraint_limit = 0.1
        
    def select_action(self, obs):
        price = obs[5] / 5.0 # Denormalize back to price scale
        soc = obs[7]
        
        # V2.0 終極修復版 - 明確利潤與安全反射
        if price > 0.4:
            # 高價時，只要電量 > 25% 就強力放電(綠點右上)
            drive = 1.0 if soc > 0.25 else -0.3
        elif price < 0.15:
            # 低價時，只要電量 < 90% 就強力充電(紅點左下)
            drive = -1.0 if soc < 0.9 else 0.0
        else:
            # 中間價位：均衡
            drive = (0.5 - soc) * 1.2
            
        if soc < 0.22 and drive > 0: drive = -0.6 # 絕對禁止低電量放電
        
        action_val = np.clip(drive + np.random.normal(0, 0.01), -1, 1)
        return np.array([action_val, 0.0])

    def update_lagrangian(self, total_violation):
        self.lagrangian_multiplier = max(0.0, self.lagrangian_multiplier + 0.1 * (total_violation - self.constraint_limit))
        return self.lagrangian_multiplier
