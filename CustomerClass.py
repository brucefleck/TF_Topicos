class Customer:
    """
    Agente Cliente
    """
    def __init__(self, customer_id, shopping_list_size, shopping_speed, patience):
        self.id = customer_id
        self.shopping_list_size = shopping_list_size
        self.shopping_speed = shopping_speed
        self.patience = patience
        self.waiting_time = 0
        self.state = "shopping"  # shopping, queueing, being_served, leaving
        self.assigned_cashier = None

    def is_done_shopping(self):
        return self.shopping_list_size <= 0

    def step_shopping(self):
        if self.state == "shopping":
            self.shopping_list_size -= self.shopping_speed
            if self.shopping_list_size < 0:
                self.shopping_list_size = 0

    def step_waiting(self):
        if self.state == "queueing":
            self.waiting_time += 1

    def abandon(self):
        self.state = "leaving"