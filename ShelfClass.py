class Shelf:
    """
    Estante / Inventario
    """
    def __init__(self, product_id, capacity, threshold, initial_stock=None):
        self.product_id = product_id
        self.capacity = capacity
        self.threshold = threshold
        self.stock = initial_stock if initial_stock is not None else capacity
        self.stockouts = 0  # número de ticks con stock = 0

    def take_products(self, amount: int) -> int:
        """
        El cliente intenta tomar 'amount' productos.
        Devuelve cuántos pudo tomar realmente.
        """
        if self.stock <= 0:
            # No hay stock
            return 0
        taken = min(amount, self.stock)
        self.stock -= taken
        return taken

    def needs_restock(self):
        return self.stock <= self.threshold

    def step_stockout_counter(self):
        if self.stock <= 0:
            self.stockouts += 1