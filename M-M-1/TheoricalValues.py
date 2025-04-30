def mm1_queue(lambda_rate, mu_rate):
    if lambda_rate >= mu_rate:
        raise ValueError("System is unstable (λ must be less than μ).")

    utilization = lambda_rate / mu_rate                     # ρ
    avg_queue_length = utilization**2 / (1 - utilization)   # Lq
    avg_wait_time = lambda_rate / (mu_rate * (mu_rate - lambda_rate))  # R
    avg_response_time = 1 / (mu_rate - lambda_rate)         # W

    print(f"Average wait time: {avg_wait_time:.4f}")
    print(f"Average queue length: {avg_queue_length:.4f}")
    print(f"Server utilization: {utilization:.4f}")
    print(f"Average response time: {avg_response_time:.4f}")

# Example values
λ = 0.9  # Arrival rate
μ = 1  # Service rate

mm1_queue(λ, μ)
