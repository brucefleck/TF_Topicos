import random
from CustomerClass import Customer
from CashierClass import Cashier
from ShelfClass import Shelf
from RestockerClass import Restocker
from ManagerClass import Manager

class SupermarketSimulation:
    """
    Clase principal de la simulación
    """
    def __init__(self,
                 max_ticks=200,
                 arrival_prob=0.5,
                 max_new_customers_per_tick=3,
                 num_cashiers=3,
                 num_restockers=1):
        # Parámetros de simulación
        self.max_ticks = max_ticks
        self.arrival_prob = arrival_prob
        self.max_new_customers_per_tick = max_new_customers_per_tick

        # Inventario / Estantes (aquí 1 estante genérico, pero se puede extender)
        self.shelves = [
            Shelf(product_id=1, capacity=200, threshold=40, initial_stock=200)
        ]

        # Cajeros
        self.cashiers = [
            Cashier(cashier_id=i, service_rate=5) for i in range(num_cashiers)
        ]

        # Reponedores
        self.restockers = [
            Restocker(restocker_id=i, restock_speed=10)
            for i in range(num_restockers)
        ]

        # Gestor
        self.manager = Manager(
            max_cashiers_open=num_cashiers,    # se puede limitar si quieres
            open_queue_threshold=5,            # si una cola pasa de 5 clientes, abrir caja
            close_idle_threshold=10            # si 10 ticks sin actividad, cerrar caja
        )
        self.manager.initialize_cashiers(self.cashiers)
        # Activamos inicialmente 1 caja
        if self.cashiers:
            self.cashiers[0].active = True

        # Clientes
        self.customers = []
        self.next_customer_id = 0

        # Métricas
        self.time = 0
        self.metrics = {
            "tick": [],
            "num_customers_in_system": [],
            "avg_waiting_time": [],
            "max_queue_length": [],
            "abandoned_customers": 0,
            "served_customers": 0,
            "total_waiting_time_served": 0,
        }

        self.abandoned_customers = 0
        self.served_customers = 0
        self.total_waiting_time_served = 0

    # ---------- Lógica de simulación por pasos ----------

    def spawn_customers(self):
        """
        Genera nuevos clientes según arrival_prob
        """
        num_new = 0
        for _ in range(self.max_new_customers_per_tick):
            if random.random() < self.arrival_prob:
                num_new += 1

        for _ in range(num_new):
            shopping_list_size = random.randint(5, 40)
            shopping_speed = random.randint(1, 3)
            patience = random.randint(5, 30)
            c = Customer(
                customer_id=self.next_customer_id,
                shopping_list_size=shopping_list_size,
                shopping_speed=shopping_speed,
                patience=patience
            )
            self.next_customer_id += 1
            self.customers.append(c)

    def customers_shopping_step(self):
        """
        Los clientes que están comprando avanzan en sus compras.
        Cuando terminan, se asume que toman sus productos del estante.
        """
        shelf = self.shelves[0]  # por ahora un solo estante

        for c in self.customers:
            if c.state == "shopping":
                # avanzar compras
                c.step_shopping()

                if c.is_done_shopping():
                    # tomar productos del estante
                    # asumimos que el cliente compró X productos en total
                    taken = shelf.take_products(amount=random.randint(1, 5))
                    # luego pasará a la cola
                    c.state = "ready_for_checkout"


    def assign_customers_to_queues(self):
        """
        Clientes que ya terminaron de comprar eligen una caja.
        """
        for c in self.customers:
            if c.state == "ready_for_checkout":
                # Elegir la caja con menor cola entre las activas;
                # si no hay activas, elegir cualquiera (o esperar)
                active_cashiers = [k for k in self.cashiers if k.active]
                if not active_cashiers:
                    # No hay cajeros activos, el cliente se puede quedar esperando
                    # o simplemente elegir el primero.
                    cashier = self.cashiers[0]
                else:
                    cashier = min(active_cashiers, key=lambda k: k.queue_length())
                cashier.add_customer_to_queue(c)

    def update_waiting_and_abandon(self):
        """
        Actualiza tiempos de espera de clientes en cola y revisa abandonos.
        """
        for c in self.customers:
            if c.state == "queueing":
                c.step_waiting()
                if c.waiting_time > c.patience:
                    c.abandon()
                    self.abandoned_customers += 1

    def cashiers_step(self):
        """
        Cada cajero procesa al cliente actual.
        """
        for cashier in self.cashiers:
            finished_customer = cashier.step()
            if finished_customer is not None:
                # Cliente servido completamente
                self.served_customers += 1
                self.total_waiting_time_served += finished_customer.waiting_time

    def shelves_step(self):
        """
        Actualiza métricas de stockout de los estantes.
        """
        for shelf in self.shelves:
            shelf.step_stockout_counter()

    def restockers_step(self):
        """
        Los reponedores reponen estantes asignados.
        """
        for r in self.restockers:
            r.step()

    def manager_step(self):
        """
        El gestor toma decisiones globales.
        """
        self.manager.step(
            cashiers=self.cashiers,
            shelves=self.shelves,
            restockers=self.restockers,
            metrics=self.metrics
        )

    def remove_finished_customers(self):
        """
        Quita de la lista de clientes aquellos que ya se fueron (servicio o abandono).
        """
        self.customers = [
            c for c in self.customers if c.state not in ("leaving",)
        ]

    def collect_metrics(self):
        """
        Guarda métricas por tick.
        """
        self.metrics["tick"].append(self.time)
        self.metrics["num_customers_in_system"].append(len(self.customers))

        # Tiempo de espera promedio de los clientes SERVIDOS hasta el momento
        if self.served_customers > 0:
            avg_wait = self.total_waiting_time_served / self.served_customers
        else:
            avg_wait = 0
        self.metrics["avg_waiting_time"].append(avg_wait)

        # Máxima longitud de cola entre cajeros
        max_queue = max((c.queue_length() for c in self.cashiers), default=0)
        self.metrics["max_queue_length"].append(max_queue)

        # Métricas acumuladas
        self.metrics["abandoned_customers"] = self.abandoned_customers
        self.metrics["served_customers"] = self.served_customers
        self.metrics["total_waiting_time_served"] = self.total_waiting_time_served

    def step(self):
        """
        Un paso (tick) completo de simulación.
        """
        # 1. Llegan nuevos clientes
        self.spawn_customers()

        # 2. Clientes compran
        self.customers_shopping_step()

        # 3. Clientes que terminaron de comprar van a las colas
        self.assign_customers_to_queues()

        # 4. Clientes en cola esperan y, si se impacientan, abandonan
        self.update_waiting_and_abandon()

        # 5. Cajeros atienden
        self.cashiers_step()

        # 6. Estantes actualizan métricas de stockout
        self.shelves_step()

        # 7. Reponedores reponen productos
        self.restockers_step()

        # 8. Gestor toma decisiones globales
        self.manager_step()

        # 9. Quitar clientes que ya se fueron
        self.remove_finished_customers()

        # 10. Guardar métricas
        self.collect_metrics()

        # Avanzar tiempo
        self.time += 1

    def run(self):
        """
        Ejecuta la simulación completa.
        """
        for _ in range(self.max_ticks):
            self.step()
        return self.metrics


