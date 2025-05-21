import numpy as np
import matplotlib.pyplot as plt

def mg1_theoretical(lambda_value, mu=1.0, cv_squared=9.0):
    """
    Compute theoretical metrics for M/G/1 queue with hyperexponential service times.
    lambda_value: arrival rate
    mu: service rate
    cv_squared: squared coefficient of variation for service times
    """
    # Check system stability
    utilization = lambda_value / mu
    if utilization >= 1:
        raise ValueError(f"Unstable system: λ={lambda_value}, μ={mu}, ρ={utilization}")

    # Mean service time and second moment for hyperexponential service
    mean_service = 1 / mu
    var_service = cv_squared * mean_service**2
    second_moment_service = var_service + mean_service**2

    # Pollaczek-Khinchine formula for average wait time (Wq)
    avg_wait_time = (lambda_value * second_moment_service) / (2 * (1 - utilization))
    
    # Other metrics
    avg_response_time = avg_wait_time + mean_service  # W = Wq + E[S]
    avg_queue_length = lambda_value * avg_wait_time   # Lq = λ * Wq

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

# Compute theoretical results for all lambda values
results = [mg1_theoretical(lambda_val, service_rate, cv_squared) for lambda_val in lambda_values]

# Extract metrics for plotting
avg_wait_times = [r['avg_wait_time'] for r in results]
avg_queue_lengths = [r['avg_queue_length'] for r in results]
utilizations = [r['utilization'] for r in results]
avg_response_times = [r['avg_response_time'] for r in results]

# Create subplots
plt.figure(figsize=(10, 8))

# 1. Average wait time
plt.subplot(2, 2, 1)
plt.plot(lambda_values, avg_wait_times, '-o', label='Wait Time')
plt.title("Temps d'attente moyen vs λ")
plt.ylabel("Temps d'attente moyen")
plt.grid(True)

# 2. Average queue length
plt.subplot(2, 2, 2)
plt.plot(lambda_values, avg_queue_lengths, '-o', color='green', label='Queue Length')
plt.title("Longueur moyenne de la file vs λ")
plt.ylabel("Longueur de file")
plt.grid(True)

# 3. Server utilization
plt.subplot(2, 2, 3)
plt.plot(lambda_values, utilizations, '-o', color='orange', label='Utilization')
plt.title("Utilisation du serveur vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Utilisation")
plt.grid(True)

# 4. Average response time
plt.subplot(2, 2, 4)
plt.plot(lambda_values, avg_response_times, '-o', color='red', label='Response Time')
plt.title("Temps de réponse moyen vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Temps de réponse")
plt.grid(True)

plt.tight_layout()
plt.savefig('mg1_theoretical_metrics_plot.png')
print("Theoretical plot saved to mg1_theoretical_metrics_plot.png")

# Display results for each lambda
print("\nTheoretical Results for M/G/1 Queue (μ=1.0, cv²=9.0)")
for i, lambda_val in enumerate(lambda_values):
    print(f"\nλ={lambda_val:.2f}:")
    print(f"Average wait time : {results[i]['avg_wait_time']:.4f}")
    print(f"Average queue length : {results[i]['avg_queue_length']:.4f}")
    print(f"Server utilization : {results[i]['utilization']:.4f}")
    print(f"Average response time : {results[i]['avg_response_time']:.4f}")