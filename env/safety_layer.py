import numpy as np

class SafetyLayer:
    def __init__(self, soc_min, soc_max, capacity_kwh, max_charge_kw, max_discharge_kw, charge_eff, discharge_eff, time_step=1):
        self.soc_min = soc_min
        self.soc_max = soc_max
        self.capacity = capacity_kwh
        self.max_charge = max_charge_kw
        self.max_discharge = max_discharge_kw
        self.charge_eff = charge_eff
        self.discharge_eff = discharge_eff
        self.dt = time_step

    def apply(self, battery_power_kw, ev_power_kw, current_soc, ev_active):
        """
        battery_power_kw: >0 discharge, <0 charge
        Returns safe_battery_power, safe_ev_power, info
        """
        info = {
            "raw_battery_power": battery_power_kw,
            "raw_ev_power": ev_power_kw,
            "modified": False,
            "reason": []
        }

        # 1. Clip Battery Power by Physical Limits
        safe_batt = np.clip(battery_power_kw, -self.max_charge, self.max_discharge)
        if safe_batt != battery_power_kw:
            info["modified"] = True
            info["reason"].append("battery_limit_clip")

        # 2. Check Next SoC
        # If charging (safe_batt < 0): SoC_next = SoC + (-safe_batt * eff * dt) / capacity
        # If discharging (safe_batt > 0): SoC_next = SoC - (safe_batt * dt / eff) / capacity
        
        if safe_batt < 0: # Charge
            max_charge_by_soc = (self.soc_max - current_soc) * self.capacity / (self.charge_eff * self.dt)
            if abs(safe_batt) > max_charge_by_soc:
                safe_batt = -max_charge_by_soc
                info["modified"] = True
                info["reason"].append("soc_max_limit")
        elif safe_batt > 0: # Discharge
            max_discharge_by_soc = (current_soc - self.soc_min) * self.capacity * self.discharge_eff / self.dt
            if safe_batt > max_discharge_by_soc:
                safe_batt = max_discharge_by_soc
                info["modified"] = True
                info["reason"].append("soc_min_limit")
                
        # 3. EV Charging
        safe_ev = ev_power_kw if ev_active else 0.0
        if safe_ev < 0: safe_ev = 0
        # Optional: clip EV power by grid limit or other things, but here just check active
        if safe_ev != ev_power_kw:
             info["modified"] = True
             info["reason"].append("ev_inactive_or_negative")

        return safe_batt, safe_ev, info
