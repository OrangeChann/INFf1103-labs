"""Lab 9, section 3 (Factory pattern) and section 7 checklist items 4-5."""
import contextlib
import inspect
import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import inventory_file
import main
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_file import InventoryFile
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from subscription_product import SubscriptionProduct
from supplier import Supplier

SUPPLIER = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
CONCRETE = ("PhysicalProduct", "DigitalProduct", "SubscriptionProduct")


class TestProductFactory(unittest.TestCase):
    def test_creates_each_known_type(self):
        expected = {"physical": PhysicalProduct, "digital": DigitalProduct,
                    "subscription": SubscriptionProduct}
        for product_type, cls in expected.items():
            with self.subTest(product_type=product_type):
                product = ProductFactory.create(product_type, "X1", "Item", 10.0, 2, SUPPLIER)
                self.assertIsInstance(product, cls)
                self.assertIsInstance(product, Product)
                self.assertEqual(product.get_price(), 10.0)
                self.assertEqual(product.get_stock(), 2)
                self.assertIs(product.supplier, SUPPLIER)

    def test_passes_each_type_its_extra_detail(self):
        lamp = ProductFactory.create("physical", "P1", "Lamp", 25, 10, SUPPLIER, weight=1.5)
        app = ProductFactory.create("digital", "D1", "App", 49.9, 100, SUPPLIER,
                                    download_size=300)
        plan = ProductFactory.create("subscription", "S1", "Plan", 9.99, 50, SUPPLIER,
                                     duration_months=12)
        self.assertEqual(lamp.get_weight(), 1.5)
        self.assertEqual(app.get_download_size(), 300)
        self.assertEqual(plan.get_duration_months(), 12)

    def test_return_type_is_the_abstraction(self):
        hints = inspect.get_annotations(ProductFactory.create, eval_str=True)
        self.assertIs(hints["return"], Product)

    def test_unknown_type_raises_clear_value_error(self):
        with self.assertRaises(ValueError) as caught:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5, SUPPLIER)
        self.assertEqual(str(caught.exception), "Unknown product type: service")


class TestClientsUseFactory(unittest.TestCase):
    """Section 7: products are created through ProductFactory, not directly."""

    def test_menu_and_loader_do_not_import_concrete_classes(self):
        for module in (main, inventory_file):
            source = inspect.getsource(module)
            for name in CONCRETE:
                with self.subTest(module=module.__name__, name=name):
                    self.assertNotIn(name, source)

    def test_menu_add_product_goes_through_factory(self):
        answers = ["1", "P1", "Desk", "80", "2", "SUP1", "Supplier",
                   "test@example.com", "12.5"]
        inventory = Inventory()
        with patch("main.ProductFactory.create", wraps=ProductFactory.create) as create, \
                patch("builtins.input", side_effect=answers), \
                contextlib.redirect_stdout(io.StringIO()):
            main.add_product(inventory)
        create.assert_called_once()
        self.assertEqual(create.call_args.args[0], "physical")
        self.assertEqual(create.call_args.kwargs, {"weight": 12.5})
        self.assertIsInstance(inventory.find_product("P1"), PhysicalProduct)

    def test_json_loader_goes_through_factory(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            source = Inventory()
            source.add_product(ProductFactory.create("digital", "D1", "App", 5, 9,
                                                     SUPPLIER, download_size=120))
            InventoryFile(path).save(source)
            restored = Inventory()
            with patch("inventory_file.ProductFactory.create",
                       wraps=ProductFactory.create) as create, \
                    contextlib.redirect_stdout(io.StringIO()):
                InventoryFile(path).load(restored)
        create.assert_called_once()
        self.assertEqual(restored.find_product("D1").get_download_size(), 120)

    def test_json_loader_skips_unknown_type(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            record = {"id": "S001", "name": "Installation", "price": 30.0,
                      "stock": 5, "type": "service"}
            with open(path, "w") as stream:
                json.dump([record], stream)
            inventory = Inventory()
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                InventoryFile(path).load(inventory)
        self.assertEqual(inventory.products, [])
        self.assertIn("Skipping invalid product record", output.getvalue())


if __name__ == "__main__":
    unittest.main()
