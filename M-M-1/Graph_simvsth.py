import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, stdev
import math

# === Simulated Data (from the first script) ===
lambdas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

wait_data = [
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

queue_data = [
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

utilization_data = [
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

response_data = [
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

# Compute means and confidence intervals for simulated data
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

avg_wait_times_sim, wait_conf_intervals = compute_mean_and_conf(wait_data)
avg_queue_lengths_sim, _ = compute_mean_and_conf(queue_data)
server_utilizations_sim, _ = compute_mean_and_conf(utilization_data)
avg_response_times_sim, response_conf_intervals = compute_mean_and_conf(response_data)

# Compute error bars for simulated data
def get_error_bars(conf_intervals, means):
    return [(mean - low, high - mean) for mean, (low, high) in zip(means, conf_intervals)]

wait_errors_sim = list(zip(*get_error_bars(wait_conf_intervals, avg_wait_times_sim)))
response_errors_sim = list(zip(*get_error_bars(response_conf_intervals, avg_response_times_sim)))

# === Theoretical Data (from the second script) ===
def mm1_theoretical_metrics(lambda_rate, mu_rate):
    if lambda_rate >= mu_rate:
        raise ValueError("Unstable system: λ must be less than μ.")
    rho = lambda_rate / mu_rate
    Lq = rho**2 / (1 - rho)                # Average queue length
    Wq = rho / (mu_rate * (1 - rho))       # Average wait time
    W = 1 / (mu_rate - lambda_rate)        # Average response time
    return Lq, Wq, rho, W

# Parameters
mu = 1.0
lambdas = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

# Calculate theoretical metrics
avg_queue_lengths_th = []
avg_wait_times_th = []
avg_response_times_th = []
server_utilizations_th = []

for lam in lambdas:
    Lq, Wq, rho, W = mm1_theoretical_metrics(lam, mu)
    avg_queue_lengths_th.append(Lq)
    avg_wait_times_th.append(Wq)
    avg_response_times_th.append(W)
    server_utilizations_th.append(rho)

# Constant error bars for theoretical data
wait_errors_th = [0.01] * len(lambdas)
response_errors_th = [0.01] * len(lambdas)

# === Plotting Combined Graphs ===
plt.figure(figsize=(12, 10))

# 1. Wait Time
plt.subplot(2, 2, 1)
plt.errorbar(lambdas, avg_wait_times_sim, yerr=wait_errors_sim, fmt='-o', capsize=4, label='Simulated Wait Time', color='#1f77b4')
plt.errorbar(lambdas, avg_wait_times_th, yerr=wait_errors_th, fmt='--o', capsize=4, label='Theoretical Wait Time', color='#ff7f0e')
plt.title("Average Wait Time vs λ")
plt.ylabel("Average Wait Time")
plt.grid(True)
plt.legend()

# 2. Queue Length
plt.subplot(2, 2, 2)
plt.plot(lambdas, avg_queue_lengths_sim, '-o', color='#2ca02c', label='Simulated Queue Length')
plt.plot(lambdas, avg_queue_lengths_th, '--o', color='#ff7f0e', label='Theoretical Queue Length')
plt.title("Average Queue Length vs λ")
plt.ylabel("Average Queue Length")
plt.grid(True)
plt.legend()

# 3. Server Utilization
plt.subplot(2, 2, 3)
plt.plot(lambdas, server_utilizations_sim, '-o', color='#ff7f0e', label='Simulated Utilization')
plt.plot(lambdas, server_utilizations_th, '--o', color='#2ca02c', label='Theoretical Utilization')
plt.title("Server Utilization vs λ")
plt.xlabel("λ (Arrival Rate)")
plt.ylabel("Utilization")
plt.grid(True)
plt.legend()

# 4. Response Time
plt.subplot(2, 2, 4)
plt.errorbar(lambdas, avg_response_times_sim, yerr=response_errors_sim, fmt='-o', capsize=4, label='Simulated Response Time', color='#d62728')
plt.errorbar(lambdas, avg_response_times_th, yerr=response_errors_th, fmt='--o', capsize=4, label='Theoretical Response Time', color='#ff7f0e')
plt.title("Average Response Time vs λ")
plt.xlabel("λ (Arrival Rate)")
plt.ylabel("Average Response Time")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()