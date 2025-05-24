import numpy as np
import pandas as pd
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# === Theoretical G/M/1 Metrics ===
def gm1_theoretical_hyperexp(lambda_val, mu=1.0, p=0.05278640450004202):
    """Compute theoretical metrics for G/M/1 queue with hyperexponential interarrivals."""
    # Compute lambda1, lambda2 for hyperexponential distribution
    x = 1 / lambda_val  # Mean interarrival time
    z = 9.0  # cv^2 = 9
    p = 0.5 * (1 - np.sqrt((z - 1) / (z + 1)))
    z1 = x / p
    z2 = x / (1 - p)
    lambda1 = 2 / z1
    lambda2 = 2 / z2

    # Laplace-Stieltjes transform
    def laplace_transform(s):
        return (p * lambda1 / (lambda1 + s)) + ((1 - p) * lambda2 / (lambda2 + s))

    # Equation for sigma
    def sigma_equation(sigma):
        s = mu * (1 - sigma)
        return sigma - laplace_transform(s)

    # Solve for sigma
    initial_guess = min(0.5, lambda_val)
    sigma, = fsolve(sigma_equation, initial_guess)

    # Check system stability
    utilization = lambda_val / mu
    if sigma >= 1 or utilization >= 1:
        raise ValueError(f"Unstable system for λ={lambda_val}, σ={sigma}")

    # Compute metrics
    avg_wait_time = sigma / (mu * (1 - sigma))  # Wq
    avg_response_time = avg_wait_time + 1 / mu  # W = Wq + 1/μ
    avg_queue_length = lambda_val * avg_wait_time  # Lq = λ * Wq

    return {
        "utilization": utilization,
        "avg_wait_time": avg_wait_time,
        "avg_response_time": avg_response_time,
        "avg_queue_length": avg_queue_length
    }

# Generate lambda values for theoretical calculations
lambda_values = np.linspace(0.1, 0.9, 9)

# Compute theoretical results
results_th = [gm1_theoretical_hyperexp(lambda_val) for lambda_val in lambda_values]

# Extract theoretical metrics
avg_wait_times_th = [r['avg_wait_time'] for r in results_th]
avg_queue_lengths_th = [r['avg_queue_length'] for r in results_th]
utilizations_th = [r['utilization'] for r in results_th]
avg_response_times_th = [r['avg_response_time'] for r in results_th]

# === Simulated Data from CSV ===
# Read the CSV file
df = pd.read_csv("gm1_simulation_results.csv")

# Extract simulated data
lambda_values_sim = df['lambda']
avg_wait_times_sim = df['avg_wait_time']
avg_queue_lengths_sim = df['avg_queue_length']
utilizations_sim = df['avg_utilization']
avg_response_times_sim = df['avg_response_time']

# Verify lambda values match
if not np.allclose(lambda_values_sim, lambda_values, atol=1e-2):
    print("Warning: Lambda values in CSV do not match theoretical lambda values. Ensure alignment for accurate comparison.")

# === Plotting Combined Graphs ===
plt.figure(figsize=(12, 10))

# 1. Average Wait Time
plt.subplot(2, 2, 1)
plt.plot(lambda_values_sim, avg_wait_times_sim, '-o', color='#1f77b4', label='Simulated Wait Time')
plt.plot(lambda_values, avg_wait_times_th, '--o', color='#ff7f0e', label='Theoretical Wait Time')
plt.title("Average Wait Time vs λ")
plt.ylabel("Average Wait Time")
plt.grid(True)
plt.legend()

# 2. Average Queue Length
plt.subplot(2, 2, 2)
plt.plot(lambda_values_sim, avg_queue_lengths_sim, '-o', color='#2ca02c', label='Simulated Queue Length')
plt.plot(lambda_values, avg_queue_lengths_th, '--o', color='#ff7f0e', label='Theoretical Queue Length')
plt.title("Average Queue Length vs λ")
plt.ylabel("Average Queue Length")
plt.grid(True)
plt.legend()

# 3. Server Utilization
plt.subplot(2, 2, 3)
plt.plot(lambda_values_sim, utilizations_sim, '-o', color='#ff7f0e', label='Simulated Utilization')
plt.plot(lambda_values, utilizations_th, '--o', color='#2ca02c', label='Theoretical Utilization')
plt.title("Server Utilization vs λ")
plt.xlabel("λ (Arrival Rate)")
plt.ylabel("Utilization")
plt.grid(True)
plt.legend()

# 4. Average Response Time
plt.subplot(2, 2, 4)
plt.plot(lambda_values_sim, avg_response_times_sim, '-o', color='#d62728', label='Simulated Response Time')
plt.plot(lambda_values, avg_response_times_th, '--o', color='#ff7f0e', label='Theoretical Response Time')
plt.title("Average Response Time vs λ")
plt.xlabel("λ (Arrival Rate)")
plt.ylabel("Average Response Time")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('gm1_combined_metrics_plot.png')
plt.show()
print("Combined plot saved to gm1_combined_metrics_plot.png")