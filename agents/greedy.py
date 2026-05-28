import numpy as np
from agents.base import BaseAgent

class PriceGreedyAgent(BaseAgent):
    def __init__(self):
        super().__init__("Price Greedy")

    def select_action(self, obs):
        price = obs[5] / 5.0
        # Aggressive price-based
        if price < 0.2:
            batt_action = -1.0
        elif price > 0.3:
            batt_action = 1.0
        else:
            batt_action = 0.0
        return np.array([batt_action, 1.0])

class CarbonGreedyAgent(BaseAgent):
    def __init__(self):
        super().__init__("Carbon Greedy")

    def select_action(self, obs):
        # obs[6]: carbon_intensity
        carbon = obs[6]
        # Low carbon: charge, High carbon: discharge
        if carbon < 0.3:
            batt_action = -1.0
        elif carbon > 0.5:
            batt_action = 1.0
        else:
            batt_action = 0.0
        return np.array([batt_action, 1.0])
