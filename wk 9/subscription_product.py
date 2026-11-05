from product import Product


class SubscriptionProduct(Product):
    """Optional reflection task (section 8): a product with a billing period."""

    def __init__(self, product_id, name, price, stock, duration_months):
        super().__init__(product_id, name, price, stock)
        if duration_months < 1:
            raise ValueError("Subscription must last at least 1 month.")
        self.__duration_months = int(duration_months)

    def get_duration_months(self):
        return self.__duration_months

    def display_information(self):
        super().display_information()
        print(f"    Duration: {self.__duration_months} months")

    def get_fulfilment_info(self):
        return f"{self.get_name()} is activated on the customer's account."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "subscription"
        data["duration_months"] = self.__duration_months
        return data
