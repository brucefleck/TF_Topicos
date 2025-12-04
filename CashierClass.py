from collections import deque
from CustomerClass import Customer

class Cashier:
    """
    Agente Cajero
    """
    def __init__(self, cashier_id, service_rate):
        self.id = cashier_id
        self.service_rate = service_rate
        self.active = False  # El gestor decide si está activo
        self.queue = deque()
        self.current_customer = None
        self.busy_time = 0

    def queue_length(self):
        return len(self.queue)

    def add_customer_to_queue(self, customer: Customer):
        customer.state = "queueing"
        customer.assigned_cashier = self
        self.queue.append(customer)

    def step(self):
        """
        Procesa al cliente actual o toma uno nuevo de la cola.
        """
        if not self.active:
            # Si la caja está cerrada, no atiende
            return None

        # Si no hay cliente actual, tomar uno de la cola
        if self.current_customer is None and self.queue:
            self.current_customer = self.queue.popleft()
            self.current_customer.state = "being_served"

        # Procesar al cliente actual
        if self.current_customer is not None:
            self.busy_time += 1
            # Suponemos que cada producto "consume" 1 unidad de servicio
            # y que el cliente trae shopping_list_size productos al llegar a caja.
            self.current_customer.shopping_list_size -= self.service_rate
            if self.current_customer.shopping_list_size <= 0:
                finished_customer = self.current_customer
                finished_customer.state = "leaving"
                self.current_customer = None
                return finished_customer

        return None  # Ningún cliente terminó este tick