import matplotlib.pyplot as plt

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self._quantity = quantity

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = str(value)
        if len(value) <= 2:
            raise ValueError("Name must have at least 3 characters")
        elif len(value) > 25:
            raise ValueError("Name can't be more than 25 characters")
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        try:
            value = int(value)  # Safely convert to integer
        except ValueError:
            raise ValueError("Price must be a positive integer")
        if value < 0:
            raise ValueError("Price must be a positive integer")
        self._price = value

    def calculate_total_price(self):
        original_price = self.price * self._quantity
        print(f"Original Price: {original_price:,.2f}")  # Format with commas
        return original_price


class DiscountedPrice(Product):
    def __init__(self, name, price, quantity, discount):
        super().__init__(name, price, quantity)
        self.discount = discount

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        try:
            value = int(value)  # Safely convert to integer
        except ValueError:
            raise ValueError("Discount must be an integer")
        if value <= 0 or value >= 100:
            raise ValueError("Invalid Discount, Enter a valid discount")
        self._discount = value

    def calculate_total_price(self):
        old_price = super().calculate_total_price()
        new_price = old_price - (old_price * self._discount / 100)
        print(f"Total discounted price: {new_price:,.2f}")  # Format with commas
        return old_price, new_price

    def visualize_prices(self):
        total_before_discount, total_after_discount = self.calculate_total_price()
        categories = ['Original Price', 'Price After Discount']
        values = [total_before_discount, total_after_discount]

        plt.bar(categories, values, color=['blue', 'green'])
        plt.title(f'Price Before and After Discount for {self.name}')
        plt.xlabel('Price Categories')
        plt.ylabel('Amount ($)')
        plt.show()


try:
    product = DiscountedPrice(name="Butter", price="2000", quantity=12, discount="10")
    product.visualize_prices()
except ValueError as e:
    print(e)
