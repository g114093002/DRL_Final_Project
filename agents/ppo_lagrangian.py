from agents.safe_carbon_agent import SafeCarbonAwareAgent

# Simple wrapper to match requested naming
class PPOLagrangianAgent(SafeCarbonAwareAgent):
    def __init__(self, state_dim=12, action_dim=2):
        super().__init__(state_dim, action_dim)
        self.name = "PPO-Lagrangian (Carbon Aware)"
