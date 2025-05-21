import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

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

# Generate lambda values from 0.1 to 0.9
lambdas = np.linspace(0.1, 0.9, 9)
results = [gm1_theoretical_hyperexp(lambda_val) for lambda_val in lambdas]

# Extract metrics for plotting
avg_wait_times = [r['avg_wait_time'] for r in results]
avg_queue_lengths = [r['avg_queue_length'] for r in results]
server_utilizations = [r['utilization'] for r in results]
avg_response_times = [r['avg_response_time'] for r in results]

# Create subplots
plt.figure(figsize=(10, 8))

# 1. Average wait time
plt.subplot(2, 2, 1)
plt.plot(lambdas, avg_wait_times, '-o', label='Wait Time')
plt.title("Temps d'attente moyen vs λ")
plt.ylabel("Temps d'attente moyen")
plt.grid(True)

# 2. Average queue length
plt.subplot(2, 2, 2)
plt.plot(lambdas, avg_queue_lengths, '-o', color='green', label='Queue Length')
plt.title("Longueur moyenne de la file vs λ")
plt.ylabel("Longueur de file")
plt.grid(True)

# 3. Server utilization
plt.subplot(2, 2, 3)
plt.plot(lambdas, server_utilizations, '-o', color='orange', label='Utilization')
plt.title("Utilisation du serveur vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Utilisation")
plt.grid(True)

# 4. Average response time
plt.subplot(2, 2, 4)
plt.plot(lambdas, avg_response_times, '-o', color='red', label='Response Time')
plt.title("Temps de réponse moyen vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Temps de réponse")
plt.grid(True)

plt.tight_layout()
plt.savefig('gm1_metrics_plot.png')