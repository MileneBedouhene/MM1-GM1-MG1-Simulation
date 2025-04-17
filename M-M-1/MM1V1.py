import random
import csv

# Constantes
MU = 1.0
TOTAL_CUSTOMERS = 1000000

class Client:
    def __init__(self, client_id, arrival_time, service_time):
        self.id = client_id
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_service_time = 0
        self.end_service_time = 0

    def compute_metrics(self, last_end_time):
        self.start_service_time = max(self.arrival_time, last_end_time)
        self.end_service_time = self.start_service_time + self.service_time
        waiting_time = self.start_service_time - self.arrival_time
        response_time = self.end_service_time - self.arrival_time
        return waiting_time, response_time

class MM1Simulation:
    def __init__(self, lam, mu, total_customers):
        self.lam = lam
        self.mu = mu
        self.total_customers = total_customers
        self.clients = []

    def generate_clients(self):
        arrival_time = 0
        for i in range(self.total_customers):
            inter_arrival = random.expovariate(self.lam)
            service_time = random.expovariate(self.mu)
            arrival_time += inter_arrival
            self.clients.append(Client(i, arrival_time, service_time))

    def run(self):
        self.generate_clients()
        last_end_time = 0
        total_waiting = 0
        total_response = 0

        for client in self.clients:
            waiting_time, response_time = client.compute_metrics(last_end_time)
            last_end_time = client.end_service_time

            total_waiting += waiting_time
            total_response += response_time

            server_state = "occupé" if client.arrival_time < client.start_service_time else "libre"
            print(f"Client {client.id}: "
                  f"Arrivée = {client.arrival_time:.2f}, "
                  f"Début Service = {client.start_service_time:.2f}, "
                  f"Fin Service = {client.end_service_time:.2f}, "
                  f"Attente = {waiting_time:.2f}, "
                  f"Réponse = {response_time:.2f}, "
                  f"Serveur = {server_state}")

        avg_waiting = total_waiting / self.total_customers
        avg_response = total_response / self.total_customers
        utilization = self.lam / self.mu

        return avg_waiting, avg_response, utilization

def save_results_to_csv(results, filename="results.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["lambda", "avg_waiting_time", "avg_response_time", "utilization"])
        writer.writerows(results)

if __name__ == "__main__":
    all_results = []

    for lam in [round(x * 0.1, 1) for x in range(1, 10)]:
        print(f"\n🚀 Simulation pour λ = {lam} avec {TOTAL_CUSTOMERS} requêtes")

        sim = MM1Simulation(lam, MU, TOTAL_CUSTOMERS)
        avg_waiting, avg_response, utilization = sim.run()

        all_results.append([lam, avg_waiting, avg_response, utilization])
        print(f"\n📊 Résultats pour λ = {lam} : "
              f"Attente moyenne = {avg_waiting:.4f}, "
              f"Réponse moyenne = {avg_response:.4f}, "
              f"Utilisation = {utilization:.2f}")

    save_results_to_csv(all_results)
    print("\n✅ Toutes les simulations sont terminées. Résultats sauvegardés dans 'results.csv'")
