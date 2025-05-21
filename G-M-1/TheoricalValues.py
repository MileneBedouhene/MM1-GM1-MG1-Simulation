import numpy as np
from scipy.optimize import fsolve

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

# Example usage
lambda_val = 0.5
mu = 1.0

# Compute metrics
results = gm1_theoretical_hyperexp(lambda_val, mu)

# Display results
print(f"Average wait time : {results['avg_wait_time']:.4f}")
print(f"Average queue length : {results['avg_queue_length']:.4f}")
print(f"Server utilization : {results['utilization']:.4f}")
print(f"Average response time : {results['avg_response_time']:.4f}")