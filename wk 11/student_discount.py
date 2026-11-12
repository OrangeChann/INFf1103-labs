"""Lab 9, section 2.4: a fourth strategy, added without changing Order.

Kept in its own file to show the Open/Closed Principle: adding this discount
needed no edit to order.py or to the existing strategies.
"""
from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    """The business's 5% student discount (the section 2.1 example)."""

    RATE = 5

    def apply(self, total: float) -> float:
        return total * (100 - self.RATE) / 100

    def __str__(self) -> str:
        return f"Student discount ({self.RATE}% off)"
