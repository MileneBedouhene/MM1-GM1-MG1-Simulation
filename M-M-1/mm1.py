import random
import math
import heapq
import statistics

def exp_rv(beta):
    return -beta * math.log(random.random())

def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = statistics.mean(data)
    stddev = statistics.stdev(data)
    z = 1.96  # for 95% confidence
    margin = z * (stddev / math.sqrt(n))
    return mean, (mean - margin, mean + margin)

# Parameters
arrival_rate = 0.1  # lambda
service_rate = 1.0  # mu
beta = 1 / arrival_rate
NUM_CUSTOMERS = 1000000

# Events
ARRIVAL = 1
DEPARTURE = 2

# State variables
current_time = 0.0
queue = []
server_busy = False
event_list = []
last_event_time = 0.0

# Statistics
num_customers_served = 0
area_queue = 0.0
area_busy = 0.0

# Individual observations
wait_times = []
response_times = []
queue_lengths = []
utilizations = []

# Schedule the first arrival
heapq.heappush(event_list, (exp_rv(beta), ARRIVAL))

# Main simulation loop
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
        if not server_busy:
            server_busy = True
            service_time = exp_rv(1/service_rate)
            response_times.append(service_time)  # No wait time
            wait_times.append(0.0)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            queue.append(current_time)

        if num_customers_served + len(queue) + (1 if server_busy else 0) < NUM_CUSTOMERS:
            next_arrival = current_time + exp_rv(beta)
            heapq.heappush(event_list, (next_arrival, ARRIVAL))

    elif event_type == DEPARTURE:
        num_customers_served += 1
        if queue:
            arrival_time = queue.pop(0)
            wait_time = current_time - arrival_time
            service_time = exp_rv(1/service_rate)
            wait_times.append(wait_time)
            response_times.append(wait_time + service_time)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            server_busy = False

# Final update
time_total = current_time
avg_wait, ci_wait = confidence_interval(wait_times)
avg_response, ci_response = confidence_interval(response_times)
avg_queue_length = area_queue / time_total
avg_utilization = area_busy / time_total

# Print results
print(f"\nSimulation Results for λ={arrival_rate}, μ={service_rate}")
print(f"Number of customers served: {num_customers_served}")
print(f"Total simulation time: {time_total:.2f}")
print(f"Average wait time: {avg_wait:.4f} (95% CI: {ci_wait[0]:.4f}, {ci_wait[1]:.4f})")
print(f"Average queue length: {avg_queue_length:.4f}")  # Deterministic, no CI
print(f"Server utilization: {avg_utilization:.4f}")     # Deterministic, no CI
print(f"Average response time: {avg_response:.4f} (95% CI: {ci_response[0]:.4f}, {ci_response[1]:.4f})")


# pour le rapport 
# donner un edescription de la mm1 et des lois utiliser
# je dois comaparer les resultats theoriques avec les resultats simulee 
# faire les graphes des reultats theoriques

# https://chatgpt.com/share/681532db-9d0c-800c-8436-59f456d390cc