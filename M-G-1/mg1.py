import random
import math
import heapq
import statistics

def exp_rv(lambda_value):
    """Generate an exponential random variate with rate lambda_value (1/lambda)."""
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
    
    # Select which exponential to use
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

# Function to calculate confidence intervals
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = statistics.mean(data)
    stddev = statistics.stdev(data)
    z = 1.96  # for 95% confidence
    margin = z * (stddev / math.sqrt(n))
    return mean, (mean - margin, mean + margin)

# Parameters
arrival_rate = 0.9  # lambda (mean arrival rate)
service_rate = 1.0  # mu (mean service rate)
NUM_CUSTOMERS = 1000000  # Number of customers to simulate

# Step 1: Generate arrival times (exponentially distributed)
arrival_times = generate_arrival_times(arrival_rate, NUM_CUSTOMERS)

# Step 2: Initialize events and variables
ARRIVAL = 1
DEPARTURE = 2

current_time = 0.0
queue = []
server_busy = False
event_list = []
last_event_time = 0.0
next_arrival_index = 0  # Index for the next arrival to process

# Statistics
num_customers_served = 0
area_queue = 0.0
area_busy = 0.0

# Individual observations
wait_times = []
response_times = []
queue_lengths = []
utilizations = []

# Schedule the first arrival event
heapq.heappush(event_list, (arrival_times[next_arrival_index], ARRIVAL))

# Step 3: Main simulation loop
while num_customers_served < NUM_CUSTOMERS:
    event_time, event_type = heapq.heappop(event_list)
    time_since_last = event_time - last_event_time
    area_queue += len(queue) * time_since_last
    area_busy += (1 if server_busy else 0) * time_since_last
    queue_lengths.append(len(queue))
    utilizations.append(1 if server_busy else 0)
    last_event_time = event_time
    current_time = event_time

    if event_type == ARRIVAL:
        # If the server is idle, start serving the customer
        if not server_busy:
            server_busy = True
            service_time = hyperx(1 / service_rate, 1 / (service_rate / 2))  # Hyperexponential service time
            response_times.append(service_time)
            wait_times.append(0.0)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            queue.append(current_time)

        # Schedule the next arrival
        next_arrival_index += 1
        if next_arrival_index < len(arrival_times):
            next_arrival = arrival_times[next_arrival_index]
            heapq.heappush(event_list, (next_arrival, ARRIVAL))

    elif event_type == DEPARTURE:
        num_customers_served += 1
        # If there is someone in the queue, start serving them
        if queue:
            arrival_time = queue.pop(0)
            wait_time = current_time - arrival_time
            service_time = hyperx(1 / service_rate, 1 / (service_rate / 2))
            wait_times.append(wait_time)
            response_times.append(wait_time + service_time)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            server_busy = False

# Final statistics
time_total = current_time
avg_wait, ci_wait = confidence_interval(wait_times)
avg_response, ci_response = confidence_interval(response_times)
avg_queue_length = area_queue / time_total
avg_utilization = area_busy / time_total

# Print the results
print(f"\nSimulation Results for λ={arrival_rate}, μ={service_rate}")
print(f"Number of customers served: {num_customers_served}")
print(f"Total simulation time: {time_total:.2f}")
print(f"Average wait time: {avg_wait:.4f} (95% CI: {ci_wait[0]:.4f}, {ci_wait[1]:.4f})")
print(f"Average queue length: {avg_queue_length:.4f}")  # Deterministic, no CI
print(f"Server utilization: {avg_utilization:.4f}")     # Deterministic, no CI
print(f"Average response time: {avg_response:.4f} (95% CI: {ci_response[0]:.4f}, {ci_response[1]:.4f})")
