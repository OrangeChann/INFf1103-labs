"""Lab 9, section 5 (exception handling) and section 7 checklist items 7-10."""
import ast
import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from input_helpers import get_non_negative_int, get_positive_float, get_positive_int
from inventory import Inventory
from inventory_file import InventoryFile
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier

APP_FOLDER = Path(__file__).resolve().parent.parent
SUPPLIER = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
LAB_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def run_with_input(function, answers, *args):
    """Call function with the given typed answers; return (result, printed lines)."""
    output = io.StringIO()
    with patch("builtins.input", side_effect=answers), contextlib.redirect_stdout(output):
        result = function(*args)
    return result, output.getvalue().splitlines()


class TestGetPositiveFloat(unittest.TestCase):
    def test_predict_first_abc_then_minus_5_then_12_50(self):
        value, printed = run_with_input(get_positive_float, ["abc", "-5", "12.50"], "Price: ")
        self.assertEqual(printed, ["Please enter a valid number, e.g. 12.50",
                                   "Please enter a number greater than zero."])
        self.assertEqual(value, 12.5)

    def test_zero_is_not_positive(self):
        value, printed = run_with_input(get_positive_float, ["0", "1"], "Price: ")
        self.assertEqual(printed, ["Please enter a number greater than zero."])
        self.assertEqual(value, 1.0)

    def test_nan_and_infinity_are_rejected(self):
        value, printed = run_with_input(get_positive_float, ["nan", "inf", "3"], "Price: ")
        self.assertEqual(len(printed), 2)
        self.assertEqual(value, 3.0)


class TestWholeNumberHelpers(unittest.TestCase):
    def test_stock_accepts_zero_after_bad_entries(self):
        value, printed = run_with_input(get_non_negative_int, ["ten", "2.5", "-1", "0"], "Stock: ")
        self.assertEqual(printed, ["Please enter a whole number, e.g. 5",
                                   "Please enter a whole number, e.g. 5",
                                   "Please enter a whole number of 0 or more."])
        self.assertEqual(value, 0)

    def test_quantity_must_be_at_least_one(self):
        value, printed = run_with_input(get_positive_int, ["0", "3"], "Quantity: ")
        self.assertEqual(printed, ["Please enter a whole number of 1 or more."])
        self.assertEqual(value, 3)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.folder.name, "products.csv")

    def tearDown(self):
        self.folder.cleanup()

    def load(self, text=None, inventory=None):
        if text is not None:
            with open(self.path, "w", newline="") as stream:
                stream.write(text)
        inventory = inventory if inventory is not None else Inventory()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(self.path, inventory, SUPPLIER)
        return inventory, output.getvalue().splitlines()

    def test_lab_file_loads_three_and_reports_two_bad_rows_in_order(self):
        inventory, printed = self.load(LAB_CSV)
        self.assertEqual([p.get_product_id() for p in inventory.products],
                         ["P001", "D001", "P003"])
        self.assertEqual(printed, [
            "Line 4 skipped (service,S001,Installation,30.00,5): Unknown product type: service",
            "Line 5 skipped (physical,P002,Office Chair,abc,3): "
            "could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])

    def test_shipped_products_csv_matches_lab_sheet(self):
        self.assertEqual((APP_FOLDER / "products.csv").read_text(), LAB_CSV)

    def test_missing_file_runs_except_and_finally_only(self):
        inventory, printed = self.load()   # no file written
        self.assertEqual(printed, [f"Products file not found: {self.path}",
                                   "Load attempt finished."])
        self.assertEqual(inventory.products, [])

    def test_products_are_created_through_factory(self):
        with patch("product_loader.ProductFactory.create",
                   wraps=ProductFactory.create) as create:
            self.load(LAB_CSV)
        self.assertEqual(create.call_count, 4)   # the "abc" row fails before create

    def test_rule_broken_inside_product_is_reported_and_skipped(self):
        inventory, printed = self.load("header\nphysical,P1,Free Lamp,0,5\n"
                                       "physical,P2,Lamp,10,-3\nphysical,P3,Lamp,10,3\n")
        self.assertIn("Price must be greater than zero.", printed[0])
        self.assertIn("Stock quantity cannot be negative.", printed[1])
        self.assertEqual([p.get_product_id() for p in inventory.products], ["P3"])

    def test_wrong_column_count_and_blank_lines(self):
        inventory, printed = self.load("header\nphysical,P1,Lamp\n\nphysical,P2,Lamp,10,3\n")
        self.assertIn("Line 2 skipped", printed[0])
        self.assertEqual(printed[1:], ["1 products loaded.", "Load attempt finished."])

    def test_duplicate_id_is_reported_and_not_counted(self):
        inventory = Inventory()
        inventory.add_product(ProductFactory.create("physical", "P001", "Laptop", 1200, 1,
                                                    SUPPLIER, weight=2))
        inventory, printed = self.load(LAB_CSV, inventory)
        self.assertIn("Line 2 skipped: product ID P001 already exists.", printed)
        self.assertIn("2 products loaded.", printed)
        self.assertEqual(inventory.find_product("P001").get_name(), "Laptop")


class TestMenuHandlesErrors(unittest.TestCase):
    def test_add_product_asks_again_for_bad_price_and_stock(self):
        answers = ["2", "D1", "App", "abc", "-5", "12.50", "-1", "four", "4",
                   "SUP1", "Supplier", "test@example.com", "120"]
        inventory = Inventory()
        _, printed = run_with_input(main.add_product, answers, inventory)
        product = inventory.find_product("D1")
        self.assertEqual(product.get_price(), 12.5)
        self.assertEqual(product.get_stock(), 4)
        self.assertIn("Product added successfully!", printed)

    def test_update_stock_asks_again(self):
        inventory = Inventory()
        inventory.add_product(ProductFactory.create("digital", "D1", "App", 5, 9, SUPPLIER))
        _, printed = run_with_input(main.update_stock, ["D1", "-4", "lots", "20"], inventory)
        self.assertEqual(inventory.find_product("D1").get_stock(), 20)
        self.assertIn("Stock updated successfully!", printed)

    def test_menu_option_9_loads_csv(self):
        inventory = Inventory()
        with patch("main.PRODUCTS_CSV", str(APP_FOLDER / "products.csv")):
            _, printed = run_with_input(main.load_products_from_csv,
                                        ["", "SUP9", "CSV Supplier", "csv@example.com"],
                                        inventory)
        self.assertIn("3 products loaded.", printed)
        self.assertEqual(inventory.find_product("P003").supplier.supplier_id, "SUP9")

    def test_failed_save_is_reported_not_crashed(self):
        with tempfile.TemporaryDirectory() as folder:
            # Saving "to" a folder raises an OSError (IsADirectory / Permission).
            _, printed = run_with_input(main.save_inventory, [],
                                        InventoryFile(folder), Inventory())
        self.assertTrue(printed[0].startswith("Could not save the inventory"))


class TestExceptsAreSpecific(unittest.TestCase):
    """Section 7: each except catches a specific exception."""

    def test_no_bare_or_catch_all_except_in_application_code(self):
        too_broad = {"Exception", "BaseException"}
        for path in APP_FOLDER.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler):
                    with self.subTest(file=path.name, line=node.lineno):
                        self.assertIsNotNone(node.type, "bare except:")
                        names = {n.id for n in ast.walk(node.type) if isinstance(n, ast.Name)}
                        self.assertFalse(names & too_broad)


if __name__ == "__main__":
    unittest.main()
