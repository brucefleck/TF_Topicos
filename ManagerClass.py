class Manager:
    """
    Agente Gestor (control global)
    """
    def __init__(self,
                 max_cashiers_open,
                 open_queue_threshold,
                 close_idle_threshold):
        self.max_cashiers_open = max_cashiers_open
        self.open_queue_threshold = open_queue_threshold
        self.close_idle_threshold = close_idle_threshold
        # Lleva un contador de inactividad para decidir cierres
        self.cashier_idle_counters = {}

    def initialize_cashiers(self, cashiers):
        for c in cashiers:
            self.cashier_idle_counters[c.id] = 0

    def step(self, cashiers, shelves, restockers, metrics):
        """
        Aplica reglas de gestión:
        - Abrir cajas si las colas están muy largas
        - Cerrar cajas si están muy inactivas
        - Asignar reposición si los estantes están bajos
        """
        # --- Gestión de colas / cajeros ---
        # Contar cuántos cajeros activos hay
        active_cashiers = [c for c in cashiers if c.active]
        inactive_cashiers = [c for c in cashiers if not c.active]

        # Regla simple: si hay alguna cola con longitud > open_queue_threshold,
        # intentar abrir otra caja (si hay disponible).
        longest_queue = max((c.queue_length() for c in cashiers), default=0)
        if longest_queue > self.open_queue_threshold and len(active_cashiers) < self.max_cashiers_open:
            # Activar el primer cajero inactivo
            if inactive_cashiers:
                inactive_cashiers[0].active = True

        # Regla simple para cierre: si un cajero activo no atiende a nadie en varios ticks, cerrarlo.
        for c in cashiers:
            if c.active:
                # si no tiene cola y no tiene cliente actual
                if c.queue_length() == 0 and c.current_customer is None:
                    self.cashier_idle_counters[c.id] += 1
                else:
                    self.cashier_idle_counters[c.id] = 0

                if self.cashier_idle_counters[c.id] >= self.close_idle_threshold and len(active_cashiers) > 1:
                    c.active = False
                    self.cashier_idle_counters[c.id] = 0

        # --- Gestión de reposición ---
        # Regla simple: si un estante necesita reposición, asignarlo al primer reponedor
        # (se puede mejorar luego).
        for shelf in shelves:
            if shelf.needs_restock():
                if restockers:
                    restockers[0].assign_shelf(shelf)