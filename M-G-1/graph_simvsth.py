import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# === Theoretical M/G/1 Metrics ===
def mg1_theoretical(lambda_value, mu=1.0, cv_squared=9.0):
    """
    Compute theoretical metrics for M/G/1 queue with hyperexponential service times.
    lambda_value: arrival rate
    mu: service rate
    cv_squared: squared coefficient of variation for service times
    """
    utilization = lambda_value / mu
    if utilization >= 1:
        raise ValueError(f"Unstable system: λ={lambda_value}, μ={mu}, ρ={utilization}")

    mean_service = 1 / mu
    var_service = cv_squared * mean_service**2
    second_moment_service = var_service + mean_service**2
    avg_wait_time = (lambda_value * second_moment_service) / (2 * (1 - utilization))
    avg_response_time = avg_wait_time + mean_service
    avg_queue_length = lambda_value * avg_wait_time

    return {
        "avg_wait_time": avg_wait_time,
        "avg_queue_length": avg_queue_length,
        "utilization": utilization,
        "avg_response_time": avg_response_time
    }

# Parameters
lambda_values = np.linspace(0.1, 0.9, 9)
service_rate = 1.0
cv_squared = 9.0

# Compute theoretical results
results_th = [mg1_theoretical(lambda_val, service_rate, cv_squared) for lambda_val in lambda_values]

# Extract theoretical metrics
avg_wait_times_th = [r['avg_wait_time'] for r in results_th]
avg_queue_lengths_th = [r['avg_queue_length'] for r in results_th]
utilizations_th = [r['utilization'] for r in results_th]
avg_response_times_th = [r['avg_response_time'] for r in results_th]

# === Simulated Data from CSV ===
# Read the CSV file
df = pd.read_csv("./mg1_simulation_results.csv")

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
plt.savefig('mg1_combined_metrics_plot.png')
plt.show()
print("Combined plot saved to mg1_combined_metrics_plot.png")