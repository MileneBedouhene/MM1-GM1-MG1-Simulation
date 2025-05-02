import math

def mg1_hyperexponential_theoretical(lambda_rate, mu_rate):
    """
    Calculate theoretical performance for M/G/1 queue with hyperexponential service times
    matching the parameters used in the simulation.
    
    Parameters:
    lambda_rate: Arrival rate (λ)
    mu_rate: Service rate (μ)
    """
    if lambda_rate >= mu_rate:
        raise ValueError("System is unstable (λ must be less than μ).")
    
    # Parameters matching your simulation's hyperx function
    x = 1/mu_rate  # mean service time
    s = 2/mu_rate  # standard deviation (as in your simulation: 1/(service_rate/2))
    
    # Calculate variance and squared coefficient of variation (SCV)
    variance = s**2
    scv = variance / (x**2)  # Squared Coefficient of Variation
    
    # Utilization (ρ)
    rho = lambda_rate / mu_rate
    
    # Pollaczek-Khinchin formulas
    Lq = (rho**2 * (1 + scv)) / (2 * (1 - rho))  # Avg queue length
    Wq = Lq / lambda_rate                         # Avg wait time in queue
    W = Wq + (1/mu_rate)                          # Avg response time
    L = lambda_rate * W                           # Avg customers in system
    
    # Print results in same format as simulation
    print(f"\nTheoretical Results for M/G/1 (Hyperexponential) λ={lambda_rate}, μ={mu_rate}")
    print("---------------------------------------------------")
    print(f"Average wait time: {Wq:.4f}")
    print(f"Average queue length: {Lq:.4f}")
    print(f"Server utilization: {rho:.4f}")
    print(f"Average response time: {W:.4f}")
    print(f"\nService time parameters:")
    print(f"Mean service time: {x:.4f}")
    print(f"Service time std dev: {s:.4f}")
    print(f"Squared CoV (SCV): {scv:.4f}")

# Example usage with same parameters as simulation
λ = 0.9  # Arrival rate
μ = 1.0  # Service rate

mg1_hyperexponential_theoretical(λ, μ)