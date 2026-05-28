import numpy as np
import pandas as pd
from config import DC_LOAD_BASE_KW, DC_LOAD_VAR_KW, PV_CAPACITY_KW, DEFAULT_HORIZON_H

def generate_synthetic_data(horizon_h=DEFAULT_HORIZON_H, pv_forecast_error=0.1, seed=42):
    np.random.seed(seed)
    timestamps = pd.date_range(start='2024-01-01', periods=horizon_h, freq='h')
    hours = np.arange(horizon_h) % 24
    days = np.arange(horizon_h) // 24
    
    # 1. Data Center IT Load (600-900 kW, higher in day, lower at night)
    base_load = DC_LOAD_BASE_KW + DC_LOAD_VAR_KW * np.sin(2 * np.pi * (hours - 8) / 24) * 0.5
    noise = np.random.normal(0, 30, horizon_h)
    dc_load = base_load + noise + 50 * (np.arange(horizon_h) % 168 < 120) # Weekday boost
    dc_load = np.maximum(dc_load, 500)

    # 2. PV Generation (Bell-shaped curve)
    # Peak at 13:00
    pv_gen_base = PV_CAPACITY_KW * np.maximum(0, np.sin(np.pi * (hours - 6) / 12))
    pv_gen_base[ (hours < 6) | (hours > 18) ] = 0
    pv_noise = np.random.normal(0, 50, horizon_h)
    pv_gen = np.maximum(0, pv_gen_base + pv_noise)
    
    # PV Forecast (with error)
    pv_forecast = pv_gen * (1 + np.random.uniform(-pv_forecast_error, pv_forecast_error, horizon_h))
    pv_forecast = np.maximum(0, pv_forecast)

    # 3. Electricity Price (TOU)
    # 00-08: Off-peak (0.1), 08-16: Mid-peak (0.2), 16-21: Peak (0.4), 21-00: Mid-peak (0.2)
    prices = np.zeros(horizon_h)
    for i, h in enumerate(hours):
        if 0 <= h < 8:
            prices[i] = 0.10
        elif 8 <= h < 16 or 21 <= h < 24:
            prices[i] = 0.25
        else:
            prices[i] = 0.45
    # Add some daily variation
    prices *= (1 + 0.1 * np.sin(2 * np.pi * days / 7))

    # 4. Grid Carbon Intensity (kgCO2/kWh)
    # Typically lower when PV is high, higher at night
    carbon_intensity = 0.5 - 0.2 * np.cos(np.pi * (hours - 13) / 12) + np.random.normal(0, 0.02, horizon_h)
    carbon_intensity = np.clip(carbon_intensity, 0.1, 0.8)

    # 5. EV Demand
    # Randomized arrival, 8h stay, 40kWh needed
    ev_demand = np.zeros(horizon_h)
    ev_active = np.zeros(horizon_h)
    for i in range(0, horizon_h, 24):
        # Morning arrival at 08:00
        arrival_idx = i + 8
        if arrival_idx < horizon_h:
            ev_active[arrival_idx : min(arrival_idx + 8, horizon_h)] = 1
            # Actual power is determined by agent, here we just flag it
            
    df = pd.DataFrame({
        'timestamp': timestamps,
        'hour': hours,
        'dc_load_kw': dc_load,
        'pv_gen_kw': pv_gen,
        'pv_forecast_kw': pv_forecast,
        'price_usd_kwh': prices,
        'carbon_intensity': carbon_intensity,
        'ev_active': ev_active
    })
    
    return df
