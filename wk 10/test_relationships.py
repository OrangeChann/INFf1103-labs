"""Lab 8, section 9: relationship, type, LSP and integration evidence."""
import contextlib
import gc
import inspect
import io
import json
import os
import tempfile
import typing
import unittest
import weakref
from unittest.mock import patch

import main
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_file import InventoryFile
from lab8_demo import show_product_details
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier


class Lab8TestCase(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("SUP1", "Music and Games", "sales@example.com")
        self.guitar = PhysicalProduct("P100", "Guitar", 300, 5, 3.5, self.supplier)
        self.game = DigitalProduct("D100", "Game", 60, 10, 2048, self.supplier)

    def capture(self, function, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            function(*args)
        return output.getvalue()


class TestSection2Association(Lab8TestCase):
    def test_products_retain_supplier_after_variable_deleted(self):
        reference = weakref.ref(self.supplier)
        del self.supplier
        gc.collect()
        self.assertIs(self.guitar.supplier, self.game.supplier)
        self.assertIs(self.guitar.supplier, reference())
        self.assertIn("Music and Games", self.capture(self.guitar.display_information))
        self.assertIn("Music and Games", self.capture(self.game.display_information))

    def test_supplier_can_exist_without_products(self):
        reference = weakref.ref(self.guitar)
        del self.guitar, self.game
        gc.collect()
        self.assertIsNone(reference())
        self.assertIn("SUP1", self.capture(self.supplier.display_information))


class TestSection3Aggregation(Lab8TestCase):
    def test_transfer_preserves_identity_and_behaviour(self):
        first, second = Inventory(), Inventory()
        self.assertTrue(first.add_product(self.guitar))
        self.assertTrue(first.remove_product("p100"))
        self.assertIsNone(first.find_product("P100"))
        self.guitar.update_stock(7)
        self.assertTrue(second.add_product(self.guitar))
        self.assertIs(second.find_product("P100"), self.guitar)
        self.assertEqual(second.find_product("P100").get_stock(), 7)

    def test_emptying_and_deleting_inventory_do_not_own_products(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.game)
        inventory.remove_product("P100")
        inventory.remove_product("D100")
        self.assertEqual(inventory.products, [])
        del inventory
        self.assertEqual(self.game.get_name(), "Game")
        self.assertEqual(self.guitar.get_name(), "Guitar")

    def test_missing_removal_and_search(self):
        inventory = Inventory()
        self.assertFalse(inventory.remove_product("missing"))
        self.assertIsNone(inventory.find_product("missing"))

    def test_collection_snapshot_does_not_allow_external_membership_changes(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.products.clear()
        self.assertIs(inventory.find_product("P100"), self.guitar)

    def test_shared_aggregation_matches_uml_multiplicity(self):
        first, second = Inventory(), Inventory()
        first.add_product(self.guitar)
        second.add_product(self.guitar)
        self.assertIs(first.products[0], second.products[0])


class TestSection4Composition(Lab8TestCase):
    def test_distinct_lines_share_one_product(self):
        first, second = Order("O1"), Order("O2")
        first.add_order_line(self.guitar, 2)
        second.add_order_line(self.guitar, 1)
        self.assertIsNot(first.order_lines[0], second.order_lines[0])
        self.assertIs(first.order_lines[0].product, second.order_lines[0].product)

    def test_subtotals_and_total_are_delegated_to_lines(self):
        order = Order("O1")
        order.add_order_line(self.guitar, 2)
        order.add_order_line(self.game, 3)
        self.assertEqual(order.order_lines[0].quantity, 2)
        self.assertEqual(order.order_lines[0].calculate_subtotal(), 600.0)
        self.assertEqual(order.order_lines[1].calculate_subtotal(), 180.0)
        self.assertEqual(order.calculate_total(), 780.0)
        with patch.object(OrderLine, "calculate_subtotal", return_value=12.5):
            self.assertEqual(order.calculate_total(), 25.0)

    def test_remove_and_cancel_release_owned_lines_but_preserve_products(self):
        order = Order("O1")
        order.add_order_line(self.guitar, 2)
        order.add_order_line(self.game, 3)
        first_line = weakref.ref(order.order_lines[0])
        order.remove_order_line(0)
        gc.collect()
        self.assertIsNone(first_line())
        self.assertEqual(order.calculate_total(), 180.0)
        last_line = weakref.ref(order.order_lines[0])
        order.cancel()
        gc.collect()
        self.assertIsNone(last_line())
        self.assertTrue(order.cancelled)
        self.assertEqual(order.order_lines, [])
        self.assertEqual(order.calculate_total(), 0.0)
        self.assertEqual(self.guitar.get_name(), "Guitar")
        self.assertEqual(self.game.get_name(), "Game")
        with self.assertRaises(ValueError):
            order.add_order_line(self.game, 1)

    def test_deleting_order_releases_unreferenced_lines(self):
        order = Order("O1")
        order.add_order_line(self.guitar, 1)
        line_reference = weakref.ref(order.order_lines[0])
        del order
        gc.collect()
        self.assertIsNone(line_reference())
        self.assertEqual(self.guitar.get_stock(), 5)

    def test_lines_cannot_be_transferred_by_mutating_collection_snapshot(self):
        first, second = Order("O1"), Order("O2")
        first.add_order_line(self.game, 1)
        second.order_lines.append(first.order_lines[0])
        first.order_lines.clear()
        self.assertEqual(len(first.order_lines), 1)
        self.assertEqual(second.order_lines, [])

    def test_invalid_quantities_and_indexes_leave_order_unchanged(self):
        order = Order("O1")
        for quantity in (0, -1):
            with self.assertRaises(ValueError):
                order.add_order_line(self.game, quantity)
        self.assertEqual(order.order_lines, [])
        for index in (-1, 0):
            with self.assertRaises(IndexError):
                order.remove_order_line(index)


class TestSections5To7TypesLSPAndPolymorphism(Lab8TestCase):
    def test_all_application_method_parameters_and_results_have_hints(self):
        for cls in (Supplier, Product, PhysicalProduct, DigitalProduct,
                    SubscriptionProduct, Inventory, InventoryFile, Order, OrderLine):
            for name, member in vars(cls).items():
                if isinstance(member, property):
                    member = member.fget
                if not inspect.isfunction(member):
                    continue
                with self.subTest(cls=cls.__name__, method=name):
                    hints = typing.get_type_hints(member)
                    self.assertIn("return", hints)
                    for parameter in inspect.signature(member).parameters:
                        if parameter != "self":
                            self.assertIn(parameter, hints)

    def test_relationship_annotations_use_domain_types(self):
        self.assertIs(typing.get_type_hints(Product.__init__)["supplier"], Supplier)
        self.assertEqual(typing.get_type_hints(Inventory.products.fget)["return"], list[Product])
        self.assertEqual(typing.get_type_hints(Inventory.find_product)["return"], Product | None)
        self.assertEqual(typing.get_type_hints(Order.order_lines.fget)["return"], list[OrderLine])
        self.assertIs(typing.get_type_hints(OrderLine.calculate_subtotal)["return"], float)

    def test_common_caller_uses_specialised_output(self):
        physical = self.capture(show_product_details, self.guitar)
        digital = self.capture(show_product_details, self.game)
        self.assertIn("Weight: 3.50 kg", physical)
        self.assertIn("Guitar requires physical shipping.", physical)
        self.assertIn("Download Size: 2048.00 MB", digital)
        self.assertIn("Game is delivered digitally.", digital)

    def test_common_stock_contract_for_all_subclasses(self):
        subscription = SubscriptionProduct("S1", "Music", 10, 50, 6, self.supplier)
        inventory = Inventory()
        products: list[Product] = [self.guitar, self.game, subscription]
        for product in products:
            with self.subTest(product=product.get_name()):
                inventory.add_product(product)
                for quantity in (0, 1, 100):
                    self.assertTrue(inventory.update_stock(product.product_id, quantity))
                    self.assertEqual(product.get_stock(), quantity)
                with self.assertRaises(ValueError):
                    inventory.update_stock(product.product_id, -1)
                self.assertEqual(product.get_stock(), 100)

    def test_mixed_inventory_dispatches_both_operations(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.game)
        output = self.capture(inventory.display_all_products)
        for expected in ("Weight:", "Download Size:", "physical shipping", "delivered digitally"):
            self.assertIn(expected, output)


class TestIntegration(Lab8TestCase):
    def test_json_round_trip_restores_supplier_identity_and_details(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            inventory = Inventory()
            inventory.add_product(self.guitar)
            inventory.add_product(self.game)
            InventoryFile(path).save(inventory)
            restored = Inventory()
            self.capture(InventoryFile(path).load, restored)
            self.assertEqual(len(restored.products), 2)
            self.assertIs(restored.products[0].supplier, restored.products[1].supplier)
            self.assertEqual(restored.products[0].supplier.to_dict(), self.supplier.to_dict())

    def test_legacy_records_get_explicit_unknown_supplier(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            record = self.guitar.to_dict()
            del record["supplier"]
            with open(path, "w") as stream:
                json.dump([record], stream)
            inventory = Inventory()
            self.capture(InventoryFile(path).load, inventory)
            self.assertEqual(inventory.products[0].supplier.supplier_id, "LEGACY")

    def test_menu_reuses_existing_supplier_without_duplicate_details(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        with patch("builtins.input", return_value="sup1"):
            with contextlib.redirect_stdout(io.StringIO()):
                supplier = main.choose_supplier(inventory)
        self.assertIs(supplier, self.supplier)

    def test_order_menu_create_add_display_remove_cancel(self):
        inventory = Inventory()
        inventory.add_product(self.game)
        orders: dict[str, Order] = {}
        answers = ["1", "O1", "2", "O1", "D100", "2", "3", "O1",
                   "4", "O1", "1", "2", "O1", "D100", "1", "5", "O1", "6"]
        with patch("builtins.input", side_effect=answers):
            output = self.capture(main.manage_orders, inventory, orders)
        self.assertIn("Order total: $120.00", output)
        self.assertIn("Order line removed.", output)
        self.assertTrue(orders["O1"].cancelled)
        self.assertEqual(orders["O1"].order_lines, [])
        self.assertIs(inventory.find_product("D100"), self.game)


if __name__ == "__main__":
    unittest.main()
