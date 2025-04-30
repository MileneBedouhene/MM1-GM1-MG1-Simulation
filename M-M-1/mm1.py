import random
import math
import heapq

def exp_rv(beta):
    return -beta * math.log(random.random())

# Parameters
arrival_rate = 0.1  # lambda
service_rate = 1.0  # mu
beta = 1/arrival_rate
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
total_wait_time = 0.0
area_queue = 0.0    # For average queue length
area_busy = 0.0     # For server utilization
total_response_time = 0.0

# Update area calculations
def update_areas(current_time):
    global last_event_time, area_queue, area_busy
    time_since_last = current_time - last_event_time
    area_queue += len(queue) * time_since_last
    area_busy += (1 if server_busy else 0) * time_since_last
    last_event_time = current_time

# Schedule the first arrival
heapq.heappush(event_list, (exp_rv(beta), ARRIVAL))

# Main simulation loop
while num_customers_served < NUM_CUSTOMERS:
    event_time, event_type = heapq.heappop(event_list)
    update_areas(event_time)
    current_time = event_time
    
    if event_type == ARRIVAL:
        if not server_busy:
            server_busy = True
            service_time = exp_rv(1/service_rate)
            total_response_time += service_time
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            queue.append(current_time)
            
        # Schedule next arrival if we haven't reached customer limit
        if num_customers_served + len(queue) + (1 if server_busy else 0) < NUM_CUSTOMERS:
            next_arrival = current_time + exp_rv(beta)
            heapq.heappush(event_list, (next_arrival, ARRIVAL))
            
    elif event_type == DEPARTURE:
        num_customers_served += 1
        if queue:
            arrival_time = queue.pop(0)
            wait_time = current_time - arrival_time
            total_wait_time += wait_time
            service_time = exp_rv(1/service_rate)
            total_response_time += wait_time + service_time
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            server_busy = False

# Final area update
update_areas(current_time)

# Calculate performance measures
avg_wait_time = total_wait_time / num_customers_served
avg_queue_length = area_queue / current_time
utilization = area_busy / current_time
avg_response_time = total_response_time / num_customers_served

# Print results
print(f"\nSimulation Results for λ={arrival_rate}, μ={service_rate}")
print(f"Number of customers served: {num_customers_served}")
print(f"Total simulation time: {current_time:.2f}")
print(f"Average wait time: {avg_wait_time:.4f}")
print(f"Average queue length: {avg_queue_length:.4f}")
print(f"Server utilization: {utilization:.4f}")
print(f"Average response time: {avg_response_time:.4f}")


#gm1 generer les arrives a l'avance et pour la mg1 j

#0,05 