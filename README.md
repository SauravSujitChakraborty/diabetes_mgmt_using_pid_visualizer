# diabetes_mgmt_using_pid_visualizer 

NOTE :- This project was made by me on Jul'25 and I preserved it, while finally publishing it on Apr 7,'26

Automatic Homeostasis Using Control Theory Applied In Diabetes Management 

Modeling an Artificial Pancreas Via Closed-Loop Feedback & Stochastic Shocks

1.Introduction

==> ​This project implements a PID (Proportional-Integral-Derivative) control system to simulate an Artificial Pancreas.

==> The engine manages blood glucose levels by responding to 'Carbohydrate Shocks' (meals) through automated insulin delivery.

==> This system is a biological analog to Delta-Hedging in quantitative finance, where a portfolio must be continuously rebalanced to maintain a neutral risk position.

​2. Mathematical Framework

​A. The System Dynamics (Mean Reversion)

==> ​The baseline glucose behavior is modeled as a Mean-Reverting Process (similar to the Ornstein-Uhlenbeck Process). It assumes that without external interference, biological systems naturally drift back toward a setpoint.

 $$ dG_t = \theta (\mu - G_t)dt + dS_t $$

where,

$$
\begin{aligned}
G_t \quad &: \text{Glucose level at time } t \\
\theta \quad &: \text{The rate of mean reversion (decay constant)} \\
\mu \quad &: \text{The target setpoint (90 mg/dL)} \\
dS_t \quad &: \text{The exogenous shock (The Meal Spike)}
\end{aligned}
$$

B. The Control Signal (PID Equation)

==> The controller calculates the Error $e(t) = G_t - \mu$ The insulin output $u(t)$ is determined by the sum of three distinct mathematical terms:

$$ u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt} $$

i) Proportional Term $(K_p)$: Reacts to the current error. If glucose is high, $u(t)$ increases immediately.

ii) ​Integral Term $(K_i)$: Accumulates past error. This ensures that even small, persistent deviations are eliminated, preventing 'Steady-State Offset'.

ii) ​Derivative Term $(K_d)$: Predicts future error by calculating the slope. This 'dampens' the system, preventing the insulin from over-correcting and causing a hypoglycemic crash.

3. The 'Quantitative' Relation : Delta-Hedging Analogy
   
==> In Quantitative Finance, a Delta-Neutral strategy requires maintaining a position where the sensitivity to price changes is zero.

i)Process Variable: In Medicine, it is Glucose; in Finance, it is the Option Delta.

ii)Target: In Medicine, it is 90 mg/dL; in Finance, it is Zero Delta.

iii)Actuator: In Medicine, it is Insulin Injection; in Finance, it is Buying/Selling the Underlying Asset.

==> This project demonstrates that the mathematics of biological homeostasis and financial risk management are functionally identical: both are Feedback Control Loops designed to minimize variance against stochastic noise.

4. Simulation Results & Visualization
   
==> The simulation tracks two primary metrics:

i)The State Path: The trajectory of Blood Glucose across a 10-hour window.

ii)The Control Effort: The rate of insulin delivery required to dampen the post-meal excursion.

==> The visualization confirms that the system is Critically Damped—it returns to the target setpoint as fast as possible without oscillating or overshooting.

5. Mathematical Tools
   
==> Discrete-time PID approximation using the Euler Method for differential equations.

6. Packages Required

==> This simulation utilizes the standard scientific Python stack to model biological feedback loops and dynamic systems.

==> NumPy (numpy): Used for the core simulation engine to handle array-based time steps and calculate the Ornstein-Uhlenbeck (O-U) process for glucose decay.

==> Matplotlib (matplotlib): Essential for generating the 'Artificial Pancreas' dashboard, visualizing the relationship between the glucose 'shock' and the insulin 'control signal'.

==> Pandas (pandas): While not strictly required for the simulation math, it is recommended for logging the clinical metrics (Peak G, Time-to-Target) into structured DataFrames for batch analysis.

7. Installation

==> Cloning the repository :

```bash
git clone [https://github.com/SauravSujitChakraborty/diabetes_mgmt_using_pid_visualizer.git](https://github.com/SauravSujitChakraborty/diabetes_mgmt_using_pid_visualizer.git)

==> Installing the dependencies :

```bash
pip install numpy matplotlib pandas

