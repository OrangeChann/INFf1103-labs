from product import Product


class DigitalProduct(Product):
    """A product delivered by download, so it does not implement CanBeShipped."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        if download_size < 0:
            raise ValueError("Download size cannot be negative.")
        self.__download_size = float(download_size)

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"    Download Size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self):
        return f"{self.get_name()} is delivered digitally."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
