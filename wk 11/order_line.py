"""Lab 8, section 4.1: a line belongs to the Order that creates it.

Lab 9, section 4: OrderLine protects its own quantity, so no caller has to
remember to check it.
"""
from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity
