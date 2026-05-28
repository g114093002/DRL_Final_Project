import numpy as np

class BaseAgent:
    def __init__(self, name):
        self.name = name

    def select_action(self, obs):
        raise NotImplementedError
