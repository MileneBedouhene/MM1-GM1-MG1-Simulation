def mm1_queue(lambda_rate, mu_rate):
    """
    Calcule les métriques de performance théoriques pour une file M/M/1.

    Paramètres :
    lambda_rate (λ) : taux d'arrivée (arrivals par unité de temps)
    mu_rate (μ)     : taux de service (services par unité de temps)

    Retour :
    None (affiche les métriques de performance)
    """
    if lambda_rate >= mu_rate:
        raise ValueError("Le système est instable (λ doit être strictement inférieur à μ).")

    # Paramètre d'utilisation du serveur
    utilization = lambda_rate / mu_rate  # ρ = λ / μ

    # Formules M/M/1
    avg_queue_length = utilization**2 / (1 - utilization)  # Lq
    avg_wait_time = utilization / (mu_rate * (1 - utilization))  # Wq
    avg_response_time = 1 / (mu_rate - lambda_rate)  # W = Wq + 1/μ
    avg_system_length = lambda_rate * avg_response_time  # L = λW

    print(f"Average wait time : {avg_wait_time:.4f}")
    print(f"Average queue length :  {avg_queue_length:.4f}")
    print(f"Server utilization: {utilization:.4f}")
    print(f"Average response time: {avg_response_time:.4f}")
    
# Exemple d'utilisation
λ = 0.1  # taux d'arrivée
μ = 1.0  # taux de service

mm1_queue(λ, μ)
