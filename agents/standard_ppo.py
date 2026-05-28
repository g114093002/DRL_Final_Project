import numpy as np
from agents.base import BaseAgent
import torch
from agents.safe_carbon_agent import Actor

class StandardPPOAgent(BaseAgent):
    def __init__(self, state_dim=12, action_dim=2):
        super().__init__("Standard PPO (Unsafe)")
        self.actor = Actor(state_dim, action_dim)
        
    def select_action(self, obs):
        state_t = torch.FloatTensor(obs).unsqueeze(0)
        with torch.no_grad():
            action = self.actor(state_t).numpy()[0]
        # Standard PPO without safety bias
        return action
