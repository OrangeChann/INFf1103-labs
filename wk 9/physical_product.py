from product import Product


class PhysicalProduct(Product):
    """A product that is stored and shipped."""

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
