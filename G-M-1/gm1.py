import random
import math
import heapq
import statistics

def exp_rv(beta):
    return -beta * math.log(random.random())

def hyperx(x, s):
    """
    Generate a random variate from Morse's two-stage hyperexponential distribution
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
    Generate arrival times using Morse's hyperexponential distribution
    lambda_value: mean arrival rate
    """
    arrival_times = []
    current_time = 0.0
    mean = 1/lambda_value  # mean interarrival time
    std = 3 * mean        # standard deviation (adjust as needed, must be > mean)
    
    for _ in range(num_arrivals):
        inter_arrival_time = hyperx(mean, std)
        current_time += inter_arrival_time
        arrival_times.append(current_time)
    return arrival_times

# Fonction pour calculer l'intervalle de confiance
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = statistics.mean(data)
    stddev = statistics.stdev(data)
    z = 1.96  # pour un intervalle de confiance de 95%
    margin = z * (stddev / math.sqrt(n))
    return mean, (mean - margin, mean + margin)

# Paramètres
arrival_rate = 0.9  # lambda
service_rate = 1.0  # mu
beta = 1 / arrival_rate
NUM_CUSTOMERS = 1000000  # Nombre de clients simulés

# Générer les temps d'arrivée à l'avance
arrival_times = generate_arrival_times(arrival_rate, NUM_CUSTOMERS)

# Événements
ARRIVAL = 1
DEPARTURE = 2

# Variables d'état
current_time = 0.0
queue = []
server_busy = False
event_list = []
last_event_time = 0.0
next_arrival_index = 0  # Indice de l'arrivée suivante à traiter

# Statistiques
num_customers_served = 0
area_queue = 0.0
area_busy = 0.0

# Observations individuelles
wait_times = []
response_times = []
queue_lengths = []
utilizations = []

# Planifier la première arrivée
heapq.heappush(event_list, (arrival_times[next_arrival_index], ARRIVAL))

# Boucle principale de simulation
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
            service_time = exp_rv(1 / service_rate)
            response_times.append(service_time)  # Pas de temps d'attente
            wait_times.append(0.0)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            queue.append(current_time)

        # Planifier la prochaine arrivée
        if num_customers_served + len(queue) + (1 if server_busy else 0) < NUM_CUSTOMERS:
            next_arrival_index += 1
            if next_arrival_index < len(arrival_times):
                next_arrival = arrival_times[next_arrival_index]
                heapq.heappush(event_list, (next_arrival, ARRIVAL))

    elif event_type == DEPARTURE:
        num_customers_served += 1
        if queue:
            arrival_time = queue.pop(0)
            wait_time = current_time - arrival_time
            service_time = exp_rv(1 / service_rate)
            wait_times.append(wait_time)
            response_times.append(wait_time + service_time)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            server_busy = False

# Mise à jour finale
time_total = current_time
avg_wait, ci_wait = confidence_interval(wait_times)
avg_response, ci_response = confidence_interval(response_times)
avg_queue_length = area_queue / time_total
avg_utilization = area_busy / time_total

# Affichage des résultats
print(f"\nSimulation Results for λ={arrival_rate}, μ={service_rate}")
print(f"Number of customers served: {num_customers_served}")
print(f"Total simulation time: {time_total:.2f}")
print(f"Average wait time: {avg_wait:.4f} (95% CI: {ci_wait[0]:.4f}, {ci_wait[1]:.4f})")
print(f"Average queue length: {avg_queue_length:.4f}")  # Déterministe, pas de CI
print(f"Server utilization: {avg_utilization:.4f}")     # Déterministe, pas de CI
print(f"Average response time: {avg_response:.4f} (95% CI: {ci_response[0]:.4f}, {ci_response[1]:.4f})")


# faire une description de gm1 et des lois utilsisees
# faire une comaparaion avec les resultats theoriques et deduire que a chaque fois le lamba est petit les resulatst ne sont pas  similaires
# faire les graphes de la simulation et des reultats theoriques