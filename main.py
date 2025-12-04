from SuperSimClass import SupermarketSimulation
import matplotlib.pyplot as plt

if __name__ == "__main__":
    sim_A = SupermarketSimulation(
        max_ticks=250,
        arrival_prob=0.3,
        max_new_customers_per_tick=3,
        num_cashiers=2,
        num_restockers=1
    )

    sim_B = SupermarketSimulation(
        max_ticks=250,
        arrival_prob=0.7,
        max_new_customers_per_tick=9,
        num_cashiers=2,
        num_restockers=1
    )

    sim_C = SupermarketSimulation(
        max_ticks=250,
        arrival_prob=0.5,
        max_new_customers_per_tick=10,
        num_cashiers=4,
        num_restockers=3
    )

    results_A = sim_A.run()
    print("=== SIMULACION A ===")
    print("Clientes atendidos:", results_A["served_customers"])
    print("Clientes que abandonaron:", results_A["abandoned_customers"])
    print("Tiempo de espera promedio (acumulado):",
          results_A["total_waiting_time_served"] / results_A["served_customers"]
          if results_A["served_customers"] > 0 else 0)
    print("Longitud máxima de cola observada:",
          max(results_A["max_queue_length"]) if results_A["max_queue_length"] else 0)

    results_B = sim_B.run()
    print("=== SIMULACION B ===")
    print("Clientes atendidos:", results_B["served_customers"])
    print("Clientes que abandonaron:", results_B["abandoned_customers"])
    print("Tiempo de espera promedio (acumulado):",
          results_B["total_waiting_time_served"] / results_B["served_customers"]
          if results_B["served_customers"] > 0 else 0)
    print("Longitud máxima de cola observada:",
          max(results_B["max_queue_length"]) if results_B["max_queue_length"] else 0)

    results_C = sim_C.run()
    print("=== SIMULACION C ===")
    print("Clientes atendidos:", results_C["served_customers"])
    print("Clientes que abandonaron:", results_C["abandoned_customers"])
    print("Tiempo de espera promedio (acumulado):",
          results_C["total_waiting_time_served"] / results_C["served_customers"]
          if results_C["served_customers"] > 0 else 0)
    print("Longitud máxima de cola observada:",
          max(results_C["max_queue_length"]) if results_C["max_queue_length"] else 0)

    ticks_A = results_A["tick"]
    avg_wait_A = results_A["avg_waiting_time"]

    ticks_B = results_B["tick"]
    avg_wait_B = results_B["avg_waiting_time"]

    ticks_C = results_C["tick"]
    avg_wait_C = results_C["avg_waiting_time"]

    plt.figure()
    plt.plot(ticks_A, avg_wait_A, label="Escenario A")
    plt.plot(ticks_B, avg_wait_B, label="Escenario B")
    plt.plot(ticks_C, avg_wait_C, label="Escenario C")
    plt.xlabel("Tick")
    plt.ylabel("Tiempo de espera promedio")
    plt.title("Comparación de tiempo de espera promedio entre escenarios")
    plt.grid(True)
    plt.legend()
    plt.show()

    max_queue_A = results_A["max_queue_length"]
    max_queue_B = results_B["max_queue_length"]
    max_queue_C = results_C["max_queue_length"]

    plt.figure()
    plt.plot(ticks_A, max_queue_A)
    plt.plot(ticks_B, max_queue_B)
    plt.plot(ticks_C, max_queue_C)
    plt.xlabel("Tick")
    plt.ylabel("Longitud máxima de cola")
    plt.title("Evolución de la longitud máxima de cola")
    plt.grid(True)
    plt.show()

    served_A = results_A["served_customers"]
    abandoned_A = results_A["abandoned_customers"]
    served_B = results_B["served_customers"]
    abandoned_B = results_B["abandoned_customers"]
    served_C = results_C["served_customers"]
    abandoned_C = results_C["abandoned_customers"]
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    
    axs[0].bar(["Atendidos", "Abandonan"], [served_A, abandoned_A])
    axs[0].set_ylabel("Número de clientes")
    axs[0].set_title("Escenario A")
    
    axs[1].bar(["Atendidos", "Abandonan"], [served_B, abandoned_B])
    axs[1].set_ylabel("Número de clientes")
    axs[1].set_title("Escenario B")
    
    axs[2].bar(["Atendidos", "Abandonan"], [served_C, abandoned_C])
    axs[2].set_ylabel("Número de clientes")
    axs[2].set_title("Escenario C")
    
    plt.tight_layout()
    plt.show()

