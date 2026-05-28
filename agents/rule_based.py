import numpy as np
from agents.base import BaseAgent

class RuleBasedTOUAgent(BaseAgent):
    def __init__(self):
        super().__init__("Rule-based TOU")

    def select_action(self, obs):
        price = obs[5] / 5.0
        batt_action = 0.0
        if price <= 0.15:
            batt_action = -0.5 # Charge
        elif price >= 0.35:
            batt_action = 0.8 # Discharge
            
        ev_action = 0.5
        return np.array([batt_action, ev_action])
