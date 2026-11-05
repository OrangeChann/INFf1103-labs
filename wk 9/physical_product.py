from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped.

    Single class inheritance: Product is the only parent class (is-a).
    CanBeShipped is not a parent class but an interface being implemented
    (must-be-able-to). Python uses the same brackets to list both.
    """

    BASE_SHIPPING_COST = 5.00
    SHIPPING_COST_PER_KG = 2.00

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        if weight < 0:
            raise ValueError("Weight cannot be negative.")
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def display_information(self):
        super().display_information()
        print(f"    Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self):
        return f"{self.get_name()} requires physical shipping."

    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING_COST + self.SHIPPING_COST_PER_KG * self.__weight
