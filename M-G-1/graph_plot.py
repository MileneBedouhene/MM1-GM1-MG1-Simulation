import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv("mg1_simulation_results.csv")

# Extract data for plotting
lambda_values = df['lambda']
avg_wait_times = df['avg_wait_time']
avg_queue_lengths = df['avg_queue_length']
avg_utilizations = df['avg_utilization']
avg_response_times = df['avg_response_time']

# Create subplots
plt.figure(figsize=(10, 8))

# 1. Average wait time
plt.subplot(2, 2, 1)
plt.plot(lambda_values, avg_wait_times, '-o', label='Wait Time')
plt.title("Temps d'attente moyen vs λ")
plt.ylabel("Temps d'attente moyen")
plt.grid(True)

# 2. Average queue length
plt.subplot(2, 2, 2)
plt.plot(lambda_values, avg_queue_lengths, '-o', color='green', label='Queue Length')
plt.title("Longueur moyenne de la file vs λ")
plt.ylabel("Longueur de file")
plt.grid(True)

# 3. Server utilization
plt.subplot(2, 2, 3)
plt.plot(lambda_values, avg_utilizations, '-o', color='orange', label='Utilization')
plt.title("Utilisation du serveur vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Utilisation")
plt.grid(True)

# 4. Average response time
plt.subplot(2, 2, 4)
plt.plot(lambda_values, avg_response_times, '-o', color='red', label='Response Time')
plt.title("Temps de réponse moyen vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Temps de réponse")
plt.grid(True)

plt.tight_layout()
plt.savefig('mg1_simulation_metrics_plot.png')
print("Simulation plot saved to mg1_simulation_metrics_plot.png")