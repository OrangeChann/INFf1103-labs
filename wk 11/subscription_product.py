from product import Product, ProductRecord
from supplier import Supplier


class SubscriptionProduct(Product):
    """Retained from Lab 7: also preserves the common Product contract."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 duration_months: int, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if duration_months < 1:
            raise ValueError("Subscription must last at least 1 month.")
        self.__duration_months: int = int(duration_months)

    def get_duration_months(self) -> int:
        return self.__duration_months

    def display_information(self) -> None:
        super().display_information()
        print(f"    Duration: {self.__duration_months} months")

    def get_fulfilment_info(self) -> str:
        return f"{self.get_name()} is activated on the customer's account."

    def to_dict(self) -> ProductRecord:
        data = super().to_dict()
        data["type"] = "subscription"
        data["duration_months"] = self.__duration_months
        return data
