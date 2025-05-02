def gm1_queue(lambda_rate, mu_rate, ca_squared):
    if lambda_rate >= mu_rate:
        raise ValueError("System is unstable (λ must be less than μ).")

    utilization = lambda_rate / mu_rate                     # ρ
    avg_wait_time = (utilization / (1 - utilization)) * ((ca_squared + 1) / (2 * mu_rate))  # Wq
    avg_response_time = avg_wait_time + (1 / mu_rate)       # W
    avg_queue_length = lambda_rate * avg_wait_time          # Lq

    print(f"Average wait time: {avg_wait_time:.4f}")
    print(f"Average queue length: {avg_queue_length:.4f}")
    print(f"Server utilization: {utilization:.4f}")
    print(f"Average response time: {avg_response_time:.4f}")

# Example values
λ = 0.9           # Arrival rate
μ = 1.0           # Service rate
C_a_squared = 9.0  # Coefficient of variation squared (e.g., hyperexponential with C_a = 3 → C_a² = 9)

gm1_queue(λ, μ, C_a_squared)
