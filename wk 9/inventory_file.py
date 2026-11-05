import os
import json

from physical_product import PhysicalProduct
from digital_product import DigitalProduct


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
                product = self.__create_product(record)
            except (KeyError, TypeError, ValueError):
                print(f"Skipping invalid product record: {record}")
                continue
            inventory.add_product(product)
        print("Inventory loaded successfully.")

    def save(self, inventory):
        # Each product describes itself, so this works for every product type.
        records = [product.to_dict() for product in inventory.get_products()]
        with open(self.__file_path, "w") as f:
            json.dump(records, f, indent=4)

    def __create_product(self, record):
        # The saved type identifier decides which subclass to create.
        common = (record["id"], record["name"], record["price"], record["stock"])
        product_type = record["type"]
        if product_type == "physical":
            return PhysicalProduct(*common, record["weight"])
        if product_type == "digital":
            return DigitalProduct(*common, record["download_size"])
        raise ValueError(f"Unknown product type: {product_type}")
