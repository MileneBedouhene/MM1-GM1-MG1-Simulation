import numpy as np

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
lambda_value = 0.5
service_rate = 1.0
cv_squared = 9.0

# Compute theoretical results
results = mg1_theoretical(lambda_value, service_rate, cv_squared)

# Display results
print(f"Average wait time : {results['avg_wait_time']:.4f}")
print(f"Average queue length : {results['avg_queue_length']:.4f}")
print(f"Server utilization : {results['utilization']:.4f}")
print(f"Average response time : {results['avg_response_time']:.4f}")