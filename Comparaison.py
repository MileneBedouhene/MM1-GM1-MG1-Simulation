import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, stdev
import math

# === M/M/1 Simulation Data ===
lambdas_mm1 = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

wait_data_mm1 = [
    [0.1107, 0.1108, 0.1108, 0.1108, 0.1115],  # λ = 0.1
    [0.2500, 0.2497, 0.2492, 0.2505, 0.2503],  # λ = 0.2
    [0.4316, 0.4276, 0.4281, 0.4253, 0.4317],  # λ = 0.3
    [0.6696, 0.6617, 0.6612, 0.6672, 0.6661],  # λ = 0.4
    [1.0042, 0.9959, 0.9967, 0.9977, 0.9941],  # λ = 0.5
    [1.5185, 1.5052, 1.4945, 1.5013, 1.4865],  # λ = 0.6
    [2.3253, 2.3215, 2.2773, 2.3481, 2.3725],  # λ = 0.7
    [3.9491, 3.9147, 3.9316, 3.9685, 3.9642],  # λ = 0.8
    [8.9528, 9.1364, 9.0492, 8.9976, 9.1194]   # λ = 0.9
]

queue_data_mm1 = [
    [0.0111, 0.0111, 0.0111, 0.0111, 0.0112],
    [0.0500, 0.0499, 0.0498, 0.0501, 0.0500],
    [0.1295, 0.1283, 0.1287, 0.1273, 0.1296],
    [0.2680, 0.2641, 0.2644, 0.2668, 0.2662],
    [0.5024, 0.4974, 0.4983, 0.5002, 0.4971],
    [0.9120, 0.9044, 0.8959, 0.9006, 0.8918],
    [1.6291, 1.6224, 1.5934, 1.6416, 1.6620],
    [3.1582, 3.1292, 3.1446, 3.1762, 3.1713],
    [8.0474, 8.2302, 8.1498, 8.0936, 8.2026]
]

utilization_data_mm1 = [
    [0.0999, 0.1000, 0.1000, 0.0997, 0.1003],
    [0.1999, 0.2000, 0.1998, 0.1999, 0.1997],
    [0.3003, 0.2999, 0.3005, 0.3996, 0.3003],
    [0.4002, 0.3987, 0.3997, 0.3996, 0.3995],
    [0.5005, 0.4993, 0.4999, 0.5009, 0.5000],
    [0.6016, 0.6002, 0.5994, 0.5997, 0.5988],
    [0.7007, 0.6989, 0.6985, 0.7004, 0.7010],
    [0.7983, 0.7977, 0.7988, 0.8004, 0.8001],
    [0.8995, 0.9017, 0.9009, 0.8994, 0.8999]
]

response_data_mm1 = [
    [1.1095, 1.1117, 1.1103, 1.1101, 1.1133],
    [1.2485, 1.2495, 1.2498, 1.2508, 1.2492],
    [1.4321, 1.4272, 1.4277, 1.4245, 1.4325],
    [1.6695, 1.6606, 1.6605, 1.6665, 1.6645],
    [2.0046, 1.9956, 1.9967, 1.9969, 1.9939],
    [2.5201, 2.5041, 2.4944, 2.5010, 2.4847],
    [3.3255, 3.3215, 3.2756, 3.3499, 3.3732],
    [4.9474, 4.9126, 4.9303, 4.9685, 4.9644],
    [9.9535, 10.1375, 10.0496, 9.9975, 10.1199]
]

# Compute means and confidence intervals for M/M/1
def compute_mean_and_conf(data_list, confidence=1.96):
    means, confs = [], []
    for data in data_list:
        m = mean(data)
        s = stdev(data)
        se = s / math.sqrt(len(data))
        margin = confidence * se
        means.append(m)
        confs.append((m - margin, m + margin))
    return means, confs

# Calculate M/M/1 metrics
avg_wait_times_mm1, wait_conf_intervals_mm1 = compute_mean_and_conf(wait_data_mm1)
avg_queue_lengths_mm1, _ = compute_mean_and_conf(queue_data_mm1)
utilizations_mm1, _ = compute_mean_and_conf(utilization_data_mm1)
avg_response_times_mm1, response_conf_intervals_mm1 = compute_mean_and_conf(response_data_mm1)

# Compute error bars for M/M/1
def get_error_bars(conf_intervals, means):
    return [(mean - low, high - mean) for mean, (low, high) in zip(means, conf_intervals)]

wait_errors_mm1 = list(zip(*get_error_bars(wait_conf_intervals_mm1, avg_wait_times_mm1)))
response_errors_mm1 = list(zip(*get_error_bars(response_conf_intervals_mm1, avg_response_times_mm1)))

# === M/G/1 Simulation Data ===
df_mg1 = pd.read_csv(r"C:\Users\milen\OneDrive\Desktop\UNI\Projets\ProjetModelisation-Simulation\M-G-1\mg1_simulation_results.csv")
lambda_values_mg1 = df_mg1['lambda']
avg_wait_times_mg1 = df_mg1['avg_wait_time']
avg_queue_lengths_mg1 = df_mg1['avg_queue_length']
utilizations_mg1 = df_mg1['avg_utilization']
avg_response_times_mg1 = df_mg1['avg_response_time']

# === G/M/1 Simulation Data ===
df_gm1 = pd.read_csv(r"C:\Users\milen\OneDrive\Desktop\UNI\Projets\ProjetModelisation-Simulation\G-M-1\gm1_simulation_results.csv")
lambda_values_gm1 = df_gm1['lambda']
avg_wait_times_gm1 = df_gm1['avg_wait_time']
avg_queue_lengths_gm1 = df_gm1['avg_queue_length']
utilizations_gm1 = df_gm1['avg_utilization']
avg_response_times_gm1 = df_gm1['avg_response_time']

# Verify lambda values alignment
if not (np.allclose(lambda_values_mg1, lambdas_mm1, atol=1e-2) and np.allclose(lambda_values_gm1, lambdas_mm1, atol=1e-2)):
    print("Warning: Lambda values in CSV files do not match M/M/1 lambda values. Ensure alignment for accurate comparison.")

# === Plotting Combined Simulation Metrics ===
plt.figure(figsize=(12, 10))

# 1. Average Wait Time
plt.subplot(2, 2, 1)
plt.errorbar(lambdas_mm1, avg_wait_times_mm1, yerr=wait_errors_mm1, fmt='-o', capsize=4, color='#1f77b4', label='M/M/1 Wait Time')
plt.plot(lambda_values_mg1, avg_wait_times_mg1, '-s', color='#ff7f0e', label='M/G/1 Wait Time')
plt.plot(lambda_values_gm1, avg_wait_times_gm1, '-^', color='#2ca02c', label='G/M/1 Wait Time')
plt.title("Average Wait Time vs λ")
plt.ylabel("Average Wait Time")
plt.grid(True)
plt.legend()

# 2. Average Queue Length
plt.subplot(2, 2, 2)
plt.plot(lambdas_mm1, avg_queue_lengths_mm1, '-o', color='#1f77b4', label='M/M/1 Queue Length')
plt.plot(lambda_values_mg1, avg_queue_lengths_mg1, '-s', color='#ff7f0e', label='M/G/1 Queue Length')
plt.plot(lambda_values_gm1, avg_queue_lengths_gm1, '-^', color='#2ca02c', label='G/M/1 Queue Length')
plt.title("Average Queue Length vs λ")
plt.ylabel("Average Queue Length")
plt.grid(True)
plt.legend()

# 3. Server Utilization
plt.subplot(2, 2, 3)
plt.plot(lambdas_mm1, utilizations_mm1, '-o', color='#1f77b4', label='M/M/1 Utilization')
plt.plot(lambda_values_mg1, utilizations_mg1, '-s', color='#ff7f0e', label='M/G/1 Utilization')
plt.plot(lambda_values_gm1, utilizations_gm1, '-^', color='#2ca02c', label='G/M/1 Utilization')
plt.title("Server Utilization vs λ")
plt.xlabel("λ (Arrival Rate)")
plt.ylabel("Utilization")
plt.grid(True)
plt.legend()

# 4. Average Response Time
plt.subplot(2, 2, 4)
plt.errorbar(lambdas_mm1, avg_response_times_mm1, yerr=response_errors_mm1, fmt='-o', capsize=4, color='#1f77b4', label='M/M/1 Response Time')
plt.plot(lambda_values_mg1, avg_response_times_mg1, '-s', color='#ff7f0e', label='M/G/1 Response Time')
plt.plot(lambda_values_gm1, avg_response_times_gm1, '-^', color='#2ca02c', label='G/M/1 Response Time')
plt.title("Average Response Time vs λ")
plt.xlabel("λ (Arrival Rate)")
plt.ylabel("Average Response Time")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig('mm1_mg1_gm1_simulation_comparison.png')
plt.show()
print("Comparison plot saved to mm1_mg1_gm1_simulation_comparison.png")