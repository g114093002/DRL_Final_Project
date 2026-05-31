import gymnasium as gym
from gymnasium import spaces
import numpy as np
from env.safety_layer import SafetyLayer
from config import *

class MicrogridEnv(gym.Env):
    def __init__(self, data_df, use_safety_layer=True):
        super(MicrogridEnv, self).__init__()
        self.df = data_df
        self.use_safety_layer = use_safety_layer
        self.horizon = len(data_df)
        self.current_step = 0
        
        self.safety_layer = SafetyLayer(
            BESS_SOC_MIN, BESS_SOC_MAX, BESS_CAPACITY_KWH,
            BESS_MAX_CHARGE_KW, BESS_MAX_DISCHARGE_KW,
            BESS_CHARGE_EFF, BESS_DISCHARGE_EFF
        )
        self.action_space = spaces.Box(low=np.array([-1.0, 0.0]), high=np.array([1.0, 1.0]), dtype=np.float32)
        self.observation_space = spaces.Box(low=-5.0, high=5.0, shape=(12,), dtype=np.float32)
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        self.soc = BESS_SOC_INITIAL
        self.prev_batt_power = 0.0
        self.ev_energy_served = 0.0
        return self._get_obs(), {}

    def _get_obs(self):
        idx = min(self.current_step, self.horizon - 1)
        row = self.df.iloc[idx]
        hour = row['hour']
        obs = np.array([
            np.sin(2 * np.pi * hour / 24),
            np.cos(2 * np.pi * hour / 24),
            row['dc_load_kw'] / 1000.0,
            row['pv_gen_kw'] / 1000.0,
            row['pv_forecast_kw'] / 1000.0,
            row['price_usd_kwh'] * 5.0,
            row['carbon_intensity'],
            self.soc,
            row['ev_active'],
            self.ev_energy_served / EV_REQUIRED_ENERGY_KWH,
            self.prev_batt_power / BESS_MAX_DISCHARGE_KW,
            (24 - hour) / 24.0
        ], dtype=np.float32)
        return obs

    def step(self, action):
        raw_batt_kw = action[0] * BESS_MAX_DISCHARGE_KW
        raw_ev_kw = action[1] * EV_MAX_POWER_KW
        row = self.df.iloc[self.current_step]
        ev_active = row['ev_active']
        
        if self.use_safety_layer:
            batt_kw, ev_kw, s_info = self.safety_layer.apply(raw_batt_kw, raw_ev_kw, self.soc, ev_active)
        else:
            batt_kw, ev_kw = raw_batt_kw, raw_ev_kw
            s_info = {"modified": False, "reason": []}
            
        if batt_kw < 0:
            self.soc += (-batt_kw * BESS_CHARGE_EFF * TIME_STEP_H) / BESS_CAPACITY_KWH
        else:
            self.soc -= (batt_kw * TIME_STEP_H / BESS_DISCHARGE_EFF) / BESS_CAPACITY_KWH
        
        dc_load = row['dc_load_kw']
        pv_gen = row['pv_gen_kw']
        net_load = dc_load + ev_kw - pv_gen - batt_kw
        grid_import = max(0, net_load)
        grid_export = max(0, -net_load)
        cost = grid_import * row['price_usd_kwh']
        carbon = grid_import * row['carbon_intensity']
        degrad = BESS_ALPHA * abs(batt_kw)
        
        # High SoC degradation penalty to prevent holding battery at high SoC for long periods
        if self.soc > 0.8:
            degrad += BESS_BETA * (self.soc - 0.8)
            
        # Quadratic action penalty to discourage extreme "bang-bang" control and encourage continuous control
        degrad += 0.0001 * (batt_kw ** 2)
        
        if np.sign(batt_kw) != np.sign(self.prev_batt_power) and abs(batt_kw) > 10:
            degrad += BESS_SWITCHING_PENALTY
            
        if ev_active: self.ev_energy_served += ev_kw * TIME_STEP_H
            
        # Reward - Natively optimize cost, carbon and degradation
        reward = -(WEIGHT_COST * cost + WEIGHT_CARBON * carbon + WEIGHT_DEGRADATION * degrad)
        
        # Continuous and smooth reward shaping for price-based charging/discharging
        # Instead of massive discrete +200 steps, we use proportional rewards
        if row['price_usd_kwh'] > 0.4 and batt_kw > 0:
            reward += 300.0 * (batt_kw / BESS_MAX_DISCHARGE_KW) * (row['price_usd_kwh'] - 0.4)
        elif row['price_usd_kwh'] < 0.15 and batt_kw < 0:
            reward += 300.0 * (-batt_kw / BESS_MAX_CHARGE_KW) * (0.15 - row['price_usd_kwh'])
        
        soc_violation = 0
        if self.soc < BESS_SOC_MIN: soc_violation = (BESS_SOC_MIN - self.soc)
        elif self.soc > BESS_SOC_MAX: soc_violation = (self.soc - BESS_SOC_MAX)
        
        if soc_violation > 0: reward -= (WEIGHT_SAFETY_VIOLATION * 5.0) * soc_violation
        
        # Continuous smooth penalty for discharging BESS at low SoC
        if self.soc < 0.25 and batt_kw > 0:
            reward -= 50.0 * (0.25 - self.soc) * (batt_kw / BESS_MAX_DISCHARGE_KW)
            
        self.prev_batt_power = batt_kw
        self.current_step += 1
        info = { 
            "step": self.current_step - 1, 
            "batt_kw": batt_kw, 
            "soc": self.soc, 
            "cost": cost, 
            "carbon": carbon,
            "degradation": degrad,
            "soc_violation": soc_violation,
            "safety_modified": s_info["modified"],
            "grid_import": grid_import,
            "grid_export": grid_export
        }
        return self._get_obs(), reward, self.current_step >= self.horizon, False, info
