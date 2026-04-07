import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# 1. PID CORE ENGINE (The Artificial Pancreas)
# ==========================================
def simulate_diabetes_control(G0, target, T, dt, meal_time, meal_carb):
    """
    Simulates glucose response using PID feedback control against a meal 'shock'.
    
    G0: Initial Glucose (mg/dL)
    target: Desired setpoint (mg/dL)
    meal_carb: The Magnitude of the glucose spike
    """
    n_steps = int(T / dt)
    t = np.linspace(0, T, n_steps)
    G = np.zeros(n_steps)
    Insulin_Delivered = np.zeros(n_steps)
    G[0] = G0
    
    # --- PID GAINS (Tuned for Stability) ---
    # Kp: Proportional (Current Error) - Reacts fast
    # Ki: Integral (Past Error Accumulated) - Eliminates bias
    # Kd: Derivative (Future Slope) - Dampens oscillations
    Kp, Ki, Kd = 0.08, 0.0008, 0.04
    integral, last_error = 0, 0
    
    for i in range(1, n_steps):
        # A. System Dynamics (Natural Decay & Mean Reversion)
        # This is essentially an Ornstein-Uhlenbeck (O-U) process.
        # It pushes glucose back toward a biological baseline.
        G[i] = G[i-1] + (0.012 * (target - G[i-1])) * dt
        
        # B. External Shock (The Meal)
        # Adds an exponential decay spike starting at the meal time.
        if t[i] > meal_time:
            spike = meal_carb * np.exp(-0.8 * (t[i] - meal_time))
            G[i] += spike * dt
            
        # C. The PID Controller (The Control Loop)
        error = G[i] - target  # High glucose is a positive error
        integral += error * dt # Accumulate past errors
        derivative = (error - last_error) / dt # Predict future slope
        
        # Insulin Control Signal (u)
        u = Kp * error + Ki * integral + Kd * derivative
        
        # Constrain insulin output (can't deliver negative insulin)
        u = max(0, u) 
        Insulin_Delivered[i] = u
        
        # D. Apply Control (Insulin lowers glucose)
        G[i] -= u * dt
        last_error = error
        
    return t, G, Insulin_Delivered

# ==========================================
# 2. RUN SIMULATION & CAPTURE LOGS
# ==========================================
# Initial 115, Target 90, Meal at Hour 2.5, Carbs=75
t_axis, G_path, Insulin_path = simulate_diabetes_control(G0=115, target=90, T=10, dt=0.05, meal_time=2.5, meal_carb=75)

# Calculate Clinical Metrics
pre_meal_idx = np.abs(t_axis - 2.0).argmin()
pre_meal_G = G_path[pre_meal_idx]
peak_G = np.max(G_path)
peak_time = t_axis[np.argmax(G_path)]
final_G = G_path[-1]

print(f"{'--- 💉 QUANTITATIVE MEDICINE: PID CONTROL LOG ---':^55}")
print(f"Set Target:        90.00 mg/dL")
print(f"Pre-Meal Level:   {pre_meal_G:.2f} mg/dL (at 2.0h)")
print(f"Meal Peak:        {peak_G:.2f} mg/dL (at {peak_time:.1f}h)")
print(f"Post-Meal Stable: {final_G:.2f} mg/dL (at 10.0h)")
print("-" * 55)

# ==========================================
# 3. CLINICAL VISUALIZER (The 'AIR 1' Plot)
# ==========================================
# Set up a professional, clean style for mobile/Pydroid
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.style.use('ggplot') # Fallback style

# Create two stacked subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# --- Subplot 1: Glucose Control ---
ax1.plot(t_axis, G_path, color='#e74c3c', linewidth=2.5, label='Blood Glucose')
ax1.axhline(90, color='#2c3e50', linestyle='--', linewidth=1.5, label='Target (90 mg/dL)')
ax1.axvline(2.5, color='#f39c12', linestyle=':', linewidth=2, label='Meal Time')

# Shaded 'Normal Range' (70-140 is typical)
ax1.fill_between(t_axis, 70, 140, color='#2ecc71', alpha=0.15, label='Target Range')

ax1.set_ylabel('Glucose (mg/dL)', fontsize=12, fontweight='bold')
ax1.set_title('PID Homeostasis: The Artificial Pancreas', fontsize=14, fontweight='bold')
ax1.set_ylim(60, 160)
ax1.legend(loc='upper right', frameon=True, facecolor='white')

# --- Subplot 2: Insulin Delivery (The Control Signal) ---
ax2.plot(t_axis, Insulin_path, color='#3498db', linewidth=2, label='Insulin Rate (u/t)')
ax2.set_ylabel('Insulin Rate', fontsize=12, fontweight='bold')
ax2.set_xlabel('Time (Hours)', fontsize=12, fontweight='bold')
ax2.set_title('Control Signal (Insulin Output)', fontsize=12)
ax2.set_ylim(0, np.max(Insulin_path)*1.2)
ax2.legend(loc='upper right', frameon=True, facecolor='white')

plt.tight_layout()
print("\n[INFO] Generating Clinical Visualization...")
plt.show() # In Pydroid, this opens a new window/tab
