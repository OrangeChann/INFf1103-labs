"""Lab 9, section 2.2: interchangeable order discounts (Strategy pattern).

Each way of discounting an order is its own class. Every strategy provides the
same apply() method, so Order can use any of them without knowing which one it
has. A new kind of discount is a new class, not an edit to Order (OCP).
"""
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Provided by the lab sheet: the shared method every strategy implements."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged. Order uses this when no strategy is given."""

    def apply(self, total: float) -> float:
        return total

    def __str__(self) -> str:
        return "No discount"


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        # Section 4: the strategy protects its own rule.
        if not 0 < percentage <= 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percentage: float = float(percentage)

    def apply(self, total: float) -> float:
        return total * (100 - self.__percentage) / 100

    def __str__(self) -> str:
        return f"{self.__percentage:g}% off"


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above a threshold,
    e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0:
            raise ValueError("Threshold cannot be negative.")
        if amount <= 0:
            raise ValueError("Discount amount must be greater than zero.")
        self.__threshold: float = float(threshold)
        self.__amount: float = float(amount)

    def apply(self, total: float) -> float:
        # This if is the bulk rule itself, not a choice between discount types.
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)
        return total

    def __str__(self) -> str:
        return f"{self.__amount:g} off orders of {self.__threshold:g} or more"
