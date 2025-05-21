import numpy as np
import matplotlib.pyplot as plt

def mm1_theoretical_metrics(lambda_rate, mu_rate):
    if lambda_rate >= mu_rate:
        raise ValueError("Unstable system: λ must be less than μ.")
    
    rho = lambda_rate / mu_rate
    Lq = rho**2 / (1 - rho)                # Taille moyenne de la file
    Wq = rho / (mu_rate * (1 - rho))       # Temps d'attente moyen
    W = 1 / (mu_rate - lambda_rate)        # Temps de réponse moyen
    return Lq, Wq, rho, W

# Paramètres
mu = 1.0
lambdas = np.arange(0.1, 1.0, 0.1)

# Initialiser les listes
avg_queue_lengths = []
avg_wait_times = []
avg_response_times = []
server_utilizations = []

# Pas d’erreurs ici, mais tu peux ajouter de fausses erreurs si tu veux tester `errorbar`
wait_errors = [0.01] * len(lambdas)
response_errors = [0.01] * len(lambdas)

# Calculer les métriques pour chaque λ
for lam in lambdas:
    Lq, Wq, rho, W = mm1_theoretical_metrics(lam, mu)
    avg_queue_lengths.append(Lq)
    avg_wait_times.append(Wq)
    avg_response_times.append(W)
    server_utilizations.append(rho)

# Tracer les sous-graphes
plt.figure(figsize=(12, 10))

# 1. Temps d’attente
plt.subplot(2, 2, 1)
plt.errorbar(lambdas, avg_wait_times, yerr=wait_errors, fmt='-o', capsize=4, label='Wait Time')
plt.title("Temps d'attente moyen vs λ")
plt.ylabel("Temps d'attente moyen")
plt.grid(True)

# 2. Taille de file moyenne
plt.subplot(2, 2, 2)
plt.plot(lambdas, avg_queue_lengths, '-o', color='green', label='Queue Length')
plt.title("Longueur moyenne de la file vs λ")
plt.ylabel("Longueur de file")
plt.grid(True)

# 3. Utilisation du serveur
plt.subplot(2, 2, 3)
plt.plot(lambdas, server_utilizations, '-o', color='orange', label='Utilization')
plt.title("Utilisation du serveur vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Utilisation")
plt.grid(True)

# 4. Temps de réponse moyen
plt.subplot(2, 2, 4)
plt.errorbar(lambdas, avg_response_times, yerr=response_errors, fmt='-o', capsize=4, color='red', label='Response Time')
plt.title("Temps de réponse moyen vs λ")
plt.xlabel("λ (Taux d'arrivée)")
plt.ylabel("Temps de réponse")
plt.grid(True)

plt.tight_layout()
plt.show()
