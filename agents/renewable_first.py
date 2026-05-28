import numpy as np
from agents.base import BaseAgent

class RenewableFirstAgent(BaseAgent):
    def __init__(self):
        super().__init__("Renewable First")

    def select_action(self, obs):
        load = obs[2]
        pv = obs[3]
        diff = pv - load
        batt_action = np.clip(-diff, -1.0, 1.0)
        ev_action = 0.5
        return np.array([batt_action, ev_action])
