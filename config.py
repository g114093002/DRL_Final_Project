"""
Configuration parameters for the Microgrid Energy Management System.
"""

# Global Simulation Settings
TIME_STEP_H = 1
DEFAULT_HORIZON_H = 168  # 7 days

# Battery (BESS) Parameters
BESS_CAPACITY_KWH = 1000.0
BESS_SOC_MIN = 0.20
BESS_SOC_MAX = 0.90
BESS_SOC_INITIAL = 0.50
BESS_CHARGE_EFF = 0.95
BESS_DISCHARGE_EFF = 0.95
BESS_MAX_CHARGE_KW = 250.0
BESS_MAX_DISCHARGE_KW = 250.0

# Degradation Parameters
BESS_ALPHA = 0.005  # Energy-based degradation weight
BESS_BETA = 0.01    # SoC change-based degradation weight
BESS_SWITCHING_PENALTY = 0.01  # Penalty for changing charge/discharge state

# Data Center Load Parameters
DC_LOAD_BASE_KW = 700.0
DC_LOAD_VAR_KW = 200.0

# Solar PV Parameters
PV_CAPACITY_KW = 1200.0

# EV Parameters
EV_MAX_POWER_KW = 50.0
EV_REQUIRED_ENERGY_KWH = 40.0
EV_DEADLINE_H = 8

# Economic Units
CURRENCY = "USD"
UNIT_PRICE = f"{CURRENCY}/kWh"
UNIT_CARBON = "kgCO2/kWh"

# Reward Weights (Cost-Optimized Formulation)
WEIGHT_COST = 2.5
WEIGHT_CARBON = 0.5
WEIGHT_DEGRADATION = 0.5
WEIGHT_PEAK_PENALTY = 1.0
WEIGHT_EV_UNSERVED = 5.0
WEIGHT_SAFETY_VIOLATION = 10.0

# Constraints
GRID_IMPORT_LIMIT_KW = 1000.0
