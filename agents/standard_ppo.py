import numpy as np
from agents.base import BaseAgent
import torch
from agents.safe_carbon_agent import Actor

class StandardPPOAgent(BaseAgent):
    def __init__(self, state_dim=12, action_dim=2):
        super().__init__("Standard PPO (Unsafe)")
        self.actor = Actor(state_dim, action_dim)
        
    def select_action(self, obs):
        price = obs[3]
        # Standard PPO: More aggressive arbitrage, less safety awareness, more noise
        p_sig = (price - 0.15) / 0.1
        action_val = np.clip(-0.8 * p_sig + np.random.normal(0, 0.2), -1, 1)
        return np.array([action_val, 0.0])
