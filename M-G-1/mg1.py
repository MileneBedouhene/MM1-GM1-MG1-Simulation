import random
import math
import heapq
import statistics
import pandas as pd

def exp_rv(lambda_value):
    """Generate an exponential random variate with rate lambda_value."""
    return -math.log(random.random()) / lambda_value

def hyperx(x, s):
    """
    Generate a random variate from a two-stage hyperexponential distribution.
    x: mean
    s: standard deviation (must be greater than x)
    Returns: random variate from the distribution
    """
    if s <= x:
        raise ValueError("hyperx Error: s must be greater than x")
    
    cv = s / x  # coefficient of variation
    z = cv * cv
    p = 0.5 * (1.0 - math.sqrt((z - 1.0) / (z + 1.0)))
    
    if random.random() > p:
        z = x / (1.0 - p)
    else:
        z = x / p
        
    return -0.5 * z * math.log(random.random())

def generate_arrival_times(lambda_value, num_arrivals):
    """
    Generate arrival times using an exponential distribution.
    lambda_value: mean arrival rate
    """
    arrival_times = []
    current_time = 0.0
    for _ in range(num_arrivals):
        inter_arrival_time = exp_rv(lambda_value)
        current_time += inter_arrival_time
        arrival_times.append(current_time)
    return arrival_times

def confidence_interval(data, confidence=0.95):
    """
    Calculate the mean and 95% confidence interval for the data.
    """
    n = len(data)
    mean = statistics.mean(data)
    if n > 1:
        stddev = statistics.stdev(data)
        z = 1.96  # for 95% confidence interval
        margin = z * (stddev / math.sqrt(n))
    else:
        margin = 0.0
    return mean, margin

def run_simulation(lambda_value, service_rate=1.0, num_customers=1000000):
    """
    Run a single M/G/1 queue simulation with exponential arrivals and hyperexponential service times.
    """
    # Check system stability
    utilization = lambda_value / service_rate
    if utilization >= 1:
        raise ValueError(f"Unstable system: λ={lambda_value}, μ={service_rate}, ρ={utilization}")

    # Generate arrival times
    arrival_times = generate_arrival_times(lambda_value, num_customers)

    # Events
    ARRIVAL = 1
    DEPARTURE = 2

    # State variables
    current_time = 0.0
    queue = []
    server_busy = False
    event_list = []
    last_event_time = 0.0
    next_arrival_index = 0
    num_customers_served = 0
    area_queue = 0.0
    area_busy = 0.0
    wait_times = []
    response_times = []
    queue_lengths = []
    utilizations = []

    # Schedule first arrival
    heapq.heappush(event_list, (arrival_times[next_arrival_index], ARRIVAL))

    # Main simulation loop
    while num_customers_served < num_customers and event_list:
        event_time, event_type = heapq.heappop(event_list)
        time_since_last = event_time - last_event_time
        area_queue += len(queue) * time_since_last
        area_busy += (1 if server_busy else 0) * time_since_last
        queue_lengths.append(len(queue))
        utilizations.append(1 if server_busy else 0)
        last_event_time = event_time
        current_time = event_time

        if event_type == ARRIVAL:
            if not server_busy:
                server_busy = True
                service_time = hyperx(1 / service_rate, 3 / service_rate)  # cv^2 = 9
                response_times.append(service_time)
                wait_times.append(0.0)
                heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
            else:
                queue.append(current_time)

            # Schedule next arrival
            if num_customers_served + len(queue) + (1 if server_busy else 0) < num_customers:
                next_arrival_index += 1
                if next_arrival_index < len(arrival_times):
                    next_arrival = arrival_times[next_arrival_index]
                    heapq.heappush(event_list, (next_arrival, ARRIVAL))

        elif event_type == DEPARTURE:
            num_customers_served += 1
            if queue:
                arrival_time = queue.pop(0)
                wait_time = current_time - arrival_time
                service_time = hyperx(1 / service_rate, 3 / service_rate)  # cv^2 = 9
                wait_times.append(wait_time)
                response_times.append(wait_time + service_time)
                heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
            else:
                server_busy = False

    # Compute final metrics
    time_total = current_time
    avg_wait, wait_margin = confidence_interval(wait_times)
    avg_response, response_margin = confidence_interval(response_times)
    avg_queue_length = area_queue / time_total
    avg_utilization = area_busy / time_total

    return {
        "avg_wait": avg_wait,
        "wait_margin": wait_margin,
        "avg_response": avg_response,
        "response_margin": response_margin,
        "avg_queue_length": avg_queue_length,
        "avg_utilization": avg_utilization
    }

# Parameters
lambda_value = 0.9
service_rate = 1.0
num_runs = 5
num_customers = 1000000

# Run simulations and collect results
results = []
for _ in range(num_runs):
    results.append(run_simulation(lambda_value, service_rate, num_customers))

# Compute averages for the metrics
avg_wait = statistics.mean([r['avg_wait'] for r in results])
avg_response = statistics.mean([r['avg_response'] for r in results])
avg_queue_length = statistics.mean([r['avg_queue_length'] for r in results])
avg_utilization = statistics.mean([r['avg_utilization'] for r in results])

# Prepare data for CSV
output_data = {
    "lambda": [lambda_value],
    "avg_wait_time": [avg_wait],
    "avg_queue_length": [avg_queue_length],
    "avg_utilization": [avg_utilization],
    "avg_response_time": [avg_response]
}

# Save to CSV
df = pd.DataFrame(output_data)
df.to_csv("mg1_simulation_results.csv", index=False)
print("Simulation results saved to mg1_simulation_results.csv")

# Display results
print(f"\nSimulation Results for (λ={lambda_value}, μ={service_rate})")
print(f"Average wait time: {avg_wait:.4f}")
print(f"Average queue length: {avg_queue_length:.4f}")
print(f"Server utilization: {avg_utilization:.4f}")
print(f"Average response time: {avg_response:.4f}")