from product import Product, ProductRecord
from supplier import Supplier


class DigitalProduct(Product):
    """A product delivered by download, so it does not implement CanBeShipped."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 download_size: float, supplier: Supplier) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return f"{self.get_name()} is delivered digitally."

    def to_dict(self) -> ProductRecord:
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
