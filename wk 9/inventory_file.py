import os
import json

from product import Product


class InventoryFile:
    """Loads and saves an Inventory to a JSON file.

    Responsibility (SRP): file handling only. It converts between the
    JSON records on disk and Product objects in memory.
    """

    def __init__(self, file_path):
        self.__file_path = file_path

    def load(self, inventory):
        if not os.path.exists(self.__file_path):
            print("inventory.json not found. Starting with an empty inventory.")
            return
        print("inventory.json found.")
        try:
            with open(self.__file_path, "r") as f:
                records = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Could not read inventory.json. Starting with an empty inventory.")
            return

        for record in records:
            try:
                product = Product(record["id"], record["name"], record["price"], record["stock"])
            except (KeyError, TypeError, ValueError):
                print(f"Skipping invalid product record: {record}")
                continue
            inventory.add_product(product)
        print("Inventory loaded successfully.")

    def save(self, inventory):
        records = [
            {
                "id": product.get_product_id(),
                "name": product.get_name(),
                "price": product.get_price(),
                "stock": product.get_stock(),
            }
            for product in inventory.get_products()
        ]
        with open(self.__file_path, "w") as f:
            json.dump(records, f, indent=4)
