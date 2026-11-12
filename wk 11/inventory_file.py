import os
import json

from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from subscription_product import SubscriptionProduct
from inventory import Inventory
from product import Product, ProductRecord
from supplier import Supplier


class InventoryFile:
    """Loads and saves an Inventory to a JSON file.

    Responsibility (SRP): file handling only. It converts between the
    JSON records on disk and Product objects in memory.
    """

    def __init__(self, file_path: str) -> None:
        self.__file_path: str = file_path

    def load(self, inventory: Inventory) -> None:
        if not os.path.exists(self.__file_path):
            print("inventory.json not found. Starting with an empty inventory.")
            return
        print("inventory.json found.")
        try:
            with open(self.__file_path, "r") as f:
                records: list[ProductRecord] = json.load(f)
        except (json.JSONDecodeError, OSError):
            print("Could not read inventory.json. Starting with an empty inventory.")
            return

        # Section 2: products with the same supplier ID share one object.
        suppliers: dict[str, Supplier] = {
            product.supplier.supplier_id: product.supplier
            for product in inventory.products
        }
        for record in records:
            try:
                product = self.__create_product(record, suppliers)
            except (KeyError, TypeError, ValueError):
                print(f"Skipping invalid product record: {record}")
                continue
            inventory.add_product(product)
        print("Inventory loaded successfully.")

    def save(self, inventory: Inventory) -> None:
        # Each product describes itself, so this works for every product type.
        records = [product.to_dict() for product in inventory.get_products()]
        with open(self.__file_path, "w") as f:
            json.dump(records, f, indent=4)

    def __create_product(self, record: ProductRecord,
                         suppliers: dict[str, Supplier]) -> Product:
        # The saved type identifier decides which subclass to create.
        # Raw JSON is validated here; the domain uses concrete object types.
        common = (record["id"], record["name"], record["price"], record["stock"])
        supplier_data = record.get("supplier", {
            "supplier_id": "LEGACY", "name": "Legacy supplier (not recorded)",
            "contact_email": "not-recorded",
        })
        supplier_id = supplier_data["supplier_id"]
        supplier = suppliers.get(supplier_id)
        if supplier is None:
            supplier = Supplier(supplier_id, supplier_data["name"],
                                supplier_data["contact_email"])
            suppliers[supplier_id] = supplier
        elif supplier.to_dict() != supplier_data:
            raise ValueError("Conflicting details for the same supplier ID.")
        product_type = record["type"]
        if product_type == "physical":
            return PhysicalProduct(*common, record["weight"], supplier)
        if product_type == "digital":
            return DigitalProduct(*common, record["download_size"], supplier)
        if product_type == "subscription":
            return SubscriptionProduct(*common, record["duration_months"], supplier)
        raise ValueError(f"Unknown product type: {product_type}")
