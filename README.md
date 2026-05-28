# Safe and Carbon-Aware DRL for Data Center Microgrid

This project is a Streamlit-based Demo Dashboard demonstrating a **Safe and Carbon-Aware Deep Reinforcement Learning** agent for Data Center behind-the-meter microgrid energy management.

## Project Motivation
Data centers are massive energy consumers. Managing their energy via microgrids (PV + Batteries) can reduce costs and carbon footprints. However, batteries have life-cycles (degradation) and strict safety constraints (SoC limits). This project showcases how Safe DRL (PPO-Lagrangian) can balance these competing objectives.

## System Architecture
1. **Observation**: Load, PV, Price, Carbon, SoC, EV.
2. **Agent**: PPO-Lagrangian with Carbon-Aware reward.
3. **Safety Layer**: Deterministic constraint satisfaction.
4. **Environment**: Simulated microgrid with synthetic data.

## Features
- Interactive Streamlit Dashboard.
- Multiple control strategies (Baseline vs. Safe DRL).
- Multi-objective optimization (Cost, Carbon, Health, Safety).
- Sensitivity analysis (PV forecast error, weight tuning).

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

## Methods
- **PPO-Lagrangian**: Uses a Lagrangian multiplier to dynamically adjust penalties for constraint violations.
- **Safety Layer**: Ensures battery power and SoC stay within physical and operational limits regardless of agent output.
