from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface-style ABC: a contract for anything that can be shipped.

    It holds no attributes or shipping details, so any kind of object can
    sign the contract, not only products.
    """

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Return the cost of shipping this object."""
