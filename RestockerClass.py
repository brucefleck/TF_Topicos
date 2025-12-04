from ShelfClass import Shelf

class Restocker:
    """
    Agente Reponedor
    """
    def __init__(self, restocker_id, restock_speed):
        self.id = restocker_id
        self.restock_speed = restock_speed
        self.assigned_shelves = []  # lista de estantes a reponer (objetos Shelf)

    def assign_shelf(self, shelf: Shelf):
        if shelf not in self.assigned_shelves:
            self.assigned_shelves.append(shelf)

    def step(self):
        """
        Recorre sus estantes asignados y repone de a poco.
        """
        for shelf in self.assigned_shelves:
            if shelf.stock < shelf.capacity:
                shelf.stock += self.restock_speed
                if shelf.stock > shelf.capacity:
                    shelf.stock = shelf.capacity
            # Si ya está lleno, se podría quitar de la lista más adelante