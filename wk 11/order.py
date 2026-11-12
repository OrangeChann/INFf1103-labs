"""Lab 8, sections 4.2-4.3: Order creates and manages its composed lines.

Lab 9, section 2.3: Order is given a DiscountStrategy and only calls its
apply() method. It contains no if/elif logic about discount types.
"""
from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__cancelled: bool = False
        # Association: the strategy is created outside and only used here.
        # None (not NoDiscount() in the signature) avoids a shared default.
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    @property
    def order_lines(self) -> list[OrderLine]:
        # Callers may inspect lines; changing this copy cannot transfer lines.
        return list(self.__order_lines)

    @property
    def cancelled(self) -> bool:
        return self.__cancelled

    @property
    def discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        """Section 2.3: swap the strategy on an existing order."""
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        if self.__cancelled:
            raise ValueError("Cannot add lines to a cancelled order.")
        # The only construction site for OrderLine in the application.
        self.__order_lines.append(OrderLine(product, quantity))

    def remove_order_line(self, index: int) -> None:
        """Remove a line using its zero-based position within this order."""
        if not 0 <= index < len(self.__order_lines):
            raise IndexError("Order line index is out of range.")
        del self.__order_lines[index]

    def calculate_subtotal(self) -> float:
        """Sum of the line subtotals, before any discount."""
        return sum((line.calculate_subtotal() for line in self.__order_lines), 0.0)

    def calculate_total(self) -> float:
        """Section 2.3: add up the lines, then let the strategy apply its discount."""
        total = self.calculate_subtotal()
        return self.__discount.apply(total)

    def cancel(self) -> None:
        self.__order_lines.clear()
        self.__cancelled = True

    def display_information(self) -> None:
        print(f"Order: {self.order_id} | Cancelled: {self.cancelled}")
        for number, line in enumerate(self.__order_lines, start=1):
            print(f"{number}. {line.product.get_name()} x {line.quantity} "
                  f"= ${line.calculate_subtotal():.2f}")
        print(f"Subtotal: ${self.calculate_subtotal():.2f}")
        print(f"Discount: {self.__discount}")
        print(f"Order total: ${self.calculate_total():.2f}")
