"""Tests for the Lab 7 checklist (section 7). Run with: python -m unittest -v"""
import contextlib
import io
import json
import os
import tempfile
import unittest
from unittest.mock import patch

import main
from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_file import InventoryFile
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct


def printed_by(function, *args):
    """Run a function and return everything it printed."""
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        function(*args)
    return output.getvalue()


def make_guitar():
    return PhysicalProduct("P100", "Guitar", 300, 5, 3.5)


def make_game():
    return DigitalProduct("D100", "Game", 60, 10, 2048)


class TestDisplayInformation(unittest.TestCase):
    def test_physical_shows_common_information_and_weight(self):
        output = printed_by(make_guitar().display_information)
        self.assertIn("ID: P100 | Name: Guitar | Price: $300.00 | Stock: 5", output)
        self.assertIn("Weight: 3.50 kg", output)

    def test_digital_shows_common_information_and_download_size(self):
        output = printed_by(make_game().display_information)
        self.assertIn("ID: D100 | Name: Game | Price: $60.00 | Stock: 10", output)
        self.assertIn("Download Size: 2048.00 MB", output)

    def test_subclasses_store_additional_attributes(self):
        self.assertEqual(make_guitar().get_weight(), 3.5)
        self.assertEqual(make_game().get_download_size(), 2048.0)

    def test_subclasses_inherit_stock_behaviour(self):
        guitar = make_guitar()
        guitar.update_stock(9)
        self.assertEqual(guitar.get_stock(), 9)

    def test_negative_additional_attributes_are_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalProduct("P1", "Bad", 1, 1, -1)
        with self.assertRaises(ValueError):
            DigitalProduct("D1", "Bad", 1, 1, -1)


class TestAbstractProduct(unittest.TestCase):
    def test_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError) as caught:
            Product("X1", "Generic", 10, 1)
        self.assertIn("get_fulfilment_info", str(caught.exception))

    def test_subclass_without_the_abstract_method_cannot_be_instantiated(self):
        class IncompleteProduct(Product):
            pass

        with self.assertRaises(TypeError):
            IncompleteProduct("X1", "Generic", 10, 1)

    def test_subclasses_implement_get_fulfilment_info(self):
        self.assertIn("physical shipping", make_guitar().get_fulfilment_info())
        self.assertIn("delivered digitally", make_game().get_fulfilment_info())


class TestCanBeShipped(unittest.TestCase):
    def test_shipping_cost_changes_with_weight(self):
        light = PhysicalProduct("P1", "Light", 1, 1, 1)
        heavy = PhysicalProduct("P2", "Heavy", 1, 1, 10)
        self.assertAlmostEqual(light.calculate_shipping_cost(), 7.00)
        self.assertAlmostEqual(heavy.calculate_shipping_cost(), 25.00)

    def test_physical_implements_the_interface(self):
        self.assertIsInstance(make_guitar(), CanBeShipped)

    def test_digital_does_not_implement_the_interface(self):
        game = make_game()
        self.assertNotIsInstance(game, CanBeShipped)
        self.assertFalse(hasattr(game, "calculate_shipping_cost"))

    def test_interface_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            CanBeShipped()

    def test_interface_is_separate_from_product(self):
        self.assertFalse(issubclass(CanBeShipped, Product))
        self.assertFalse(issubclass(Product, CanBeShipped))


class TestInventoryOperations(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.inventory.add_product(make_guitar())
        self.inventory.add_product(make_game())

    def test_duplicate_id_is_refused(self):
        self.assertFalse(self.inventory.add_product(make_guitar()))
        self.assertEqual(len(self.inventory.get_products()), 2)

    def test_search_finds_the_correct_type(self):
        self.assertIsInstance(self.inventory.search_product("p100"), PhysicalProduct)
        self.assertIsInstance(self.inventory.search_product("D100"), DigitalProduct)
        self.assertIsNone(self.inventory.search_product("missing"))

    def test_update_stock(self):
        self.assertTrue(self.inventory.update_stock("D100", 99))
        self.assertEqual(self.inventory.search_product("D100").get_stock(), 99)
        self.assertFalse(self.inventory.update_stock("missing", 1))

    def test_display_all_uses_each_subclass_display(self):
        output = printed_by(self.inventory.display_all)
        self.assertIn("Weight: 3.50 kg", output)
        self.assertIn("Download Size: 2048.00 MB", output)


class TestAddProductMenu(unittest.TestCase):
    def add_with_answers(self, *answers):
        inventory = Inventory()
        with patch("builtins.input", side_effect=answers):
            printed_by(main.add_product, inventory)
        return inventory

    def test_add_physical_asks_for_weight(self):
        inventory = self.add_with_answers("1", "P1", "Desk", "80", "2", "12.5")
        product = inventory.search_product("P1")
        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 12.5)

    def test_add_digital_asks_for_download_size(self):
        inventory = self.add_with_answers("2", "D1", "App", "5", "9", "120")
        product = inventory.search_product("D1")
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 120.0)

    def test_invalid_type_adds_nothing(self):
        inventory = self.add_with_answers("9")
        self.assertEqual(inventory.get_products(), [])

    def test_invalid_additional_value_adds_nothing(self):
        inventory = self.add_with_answers("1", "P1", "Desk", "80", "2", "heavy")
        self.assertEqual(inventory.get_products(), [])


class TestJsonPersistence(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.path = os.path.join(folder.name, "inventory.json")

    def load_inventory(self):
        # A new Inventory and InventoryFile is the same as restarting the program.
        inventory = Inventory()
        printed_by(InventoryFile(self.path).load, inventory)
        return inventory

    def save_sample_inventory(self):
        inventory = Inventory()
        inventory.add_product(make_guitar())
        inventory.add_product(make_game())
        inventory.add_product(SubscriptionProduct("S100", "Music", 10, 50, 6))
        InventoryFile(self.path).save(inventory)

    def test_saved_records_include_type_and_additional_attributes(self):
        self.save_sample_inventory()
        with open(self.path) as f:
            records = {record["id"]: record for record in json.load(f)}
        self.assertEqual(records["P100"]["type"], "physical")
        self.assertEqual(records["P100"]["weight"], 3.5)
        self.assertEqual(records["D100"]["type"], "digital")
        self.assertEqual(records["D100"]["download_size"], 2048.0)
        self.assertEqual(records["S100"]["type"], "subscription")
        self.assertEqual(records["S100"]["duration_months"], 6)

    def test_loading_restores_the_correct_subclasses_and_values(self):
        self.save_sample_inventory()
        inventory = self.load_inventory()

        guitar = inventory.search_product("P100")
        self.assertIs(type(guitar), PhysicalProduct)
        self.assertEqual(guitar.get_name(), "Guitar")
        self.assertEqual(guitar.get_price(), 300.0)
        self.assertEqual(guitar.get_stock(), 5)
        self.assertEqual(guitar.get_weight(), 3.5)

        game = inventory.search_product("D100")
        self.assertIs(type(game), DigitalProduct)
        self.assertEqual(game.get_download_size(), 2048.0)

        music = inventory.search_product("S100")
        self.assertIs(type(music), SubscriptionProduct)
        self.assertEqual(music.get_duration_months(), 6)

    def test_invalid_records_are_skipped(self):
        records = [
            {"id": "A", "name": "No type", "price": 1, "stock": 1},
            {"id": "B", "name": "Unknown", "price": 1, "stock": 1, "type": "magic"},
            {"id": "C", "name": "No weight", "price": 1, "stock": 1, "type": "physical"},
            {"id": "D", "name": "Good", "price": 1, "stock": 1, "type": "digital",
             "download_size": 1},
        ]
        with open(self.path, "w") as f:
            json.dump(records, f)
        products = self.load_inventory().get_products()
        self.assertEqual([p.get_product_id() for p in products], ["D"])


class TestSubscriptionProduct(unittest.TestCase):
    """Optional reflection task (section 8)."""

    def test_subscription_is_a_product_but_cannot_be_shipped(self):
        music = SubscriptionProduct("S100", "Music", 10, 50, 6)
        self.assertIsInstance(music, Product)
        self.assertNotIsInstance(music, CanBeShipped)
        self.assertIn("Duration: 6 months", printed_by(music.display_information))
        self.assertIn("activated", music.get_fulfilment_info())

    def test_zero_month_subscription_is_rejected(self):
        with self.assertRaises(ValueError):
            SubscriptionProduct("S1", "Bad", 1, 1, 0)


if __name__ == "__main__":
    unittest.main()
