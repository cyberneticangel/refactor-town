from dataclasses import dataclass


@dataclass
class Item:
    name: str
    price: float
    qty: int

    @property
    def value(self):
        return self.price * self.qty


class Inventory:
    def __init__(self):
        self.items = {}  # name -> Item

    def add(self, name, price, qty):
        if name in self.items:
            raise ValueError("duplicate item: " + name)
        self.items[name] = Item(name, price, qty)

    def restock(self, name, amount):
        if name not in self.items:
            raise KeyError(name)
        self.items[name].qty += amount

    def total_value(self):
        return sum(item.value for item in self.items.values())

    def low_stock(self, threshold=5):
        return [item.name for item in self.items.values() if item.qty < threshold]

    def most_valuable(self):
        best = max(self.items.values(), key=lambda item: item.value, default=None)
        return best.name if best else None
