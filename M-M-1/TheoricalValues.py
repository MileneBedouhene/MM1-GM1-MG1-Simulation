def mg1_queue(lambda_rate, mu_rate, service_std_dev):
    """
    Calculate theoretical performance metrics for M/G/1 queue.
    
    Parameters:
    lambda_rate (λ): Arrival rate
    mu_rate (μ): Service rate
    service_std_dev: Standard deviation of service time distribution
    
    Returns:
    None (prints performance metrics)
    """
    if lambda_rate >= mu_rate:
        raise ValueError("System is unstable (λ must be less than μ).")
    
    # Calculate key parameters
    utilization = lambda_rate / mu_rate                     # ρ = λ/μ
    service_variance = service_std_dev**2                  # σ²
    
    # Pollaczek-Khinchin formulas
    avg_queue_length = (lambda_rate**2 * service_variance + utilization**2) / (2 * (1 - utilization))  # Lq
    avg_wait_time = avg_queue_length / lambda_rate          # Wq = Lq/λ
    avg_response_time = avg_wait_time + (1 / mu_rate)      # W = Wq + 1/μ
    avg_system_length = lambda_rate * avg_response_time    # L = λW
    
    print(f"Average wait time in queue: {avg_wait_time:.4f}")
    print(f"Average queue length: {avg_queue_length:.4f}")
    print(f"Server utilization: {utilization:.4f}")
    print(f"Average response time: {avg_response_time:.4f}")
    print(f"Average customers in system: {avg_system_length:.4f}")
    print(f"Service time variance: {service_variance:.4f}")

# Example values matching your simulation
λ = 0.9      # Arrival rate
μ = 1.0      # Service rate
σ = 2.0      # Standard deviation of service time (hyperexponential case)

mg1_queue(λ, μ, σ)