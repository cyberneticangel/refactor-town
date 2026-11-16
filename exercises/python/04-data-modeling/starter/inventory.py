class Inventory:
    def __init__(self):
        self.names = []
        self.prices = []
        self.qtys = []

    def add(self, name, price, qty):
        for i in range(len(self.names)):
            if self.names[i] == name:
                raise ValueError("duplicate item: " + name)
        self.names.append(name)
        self.prices.append(price)
        self.qtys.append(qty)

    def restock(self, name, amount):
        if name not in self.names:
            raise KeyError(name)
        i = self.names.index(name)
        self.qtys[i] = self.qtys[i] + amount

    def total_value(self):
        total = 0
        for i in range(len(self.names)):
            total = total + self.prices[i] * self.qtys[i]
        return total

    def low_stock(self, threshold=5):
        result = []
        for i in range(len(self.names)):
            if self.qtys[i] < threshold:
                result.append(self.names[i])
        return result

    def most_valuable(self):
        if len(self.names) == 0:
            return None
        best = 0
        for i in range(len(self.names)):
            if self.prices[i] * self.qtys[i] > self.prices[best] * self.qtys[best]:
                best = i
        return self.names[best]
