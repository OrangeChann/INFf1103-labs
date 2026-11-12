"""Lab 9, section 2 (Strategy pattern) and section 7 checklist items 1-3."""
import contextlib
import inspect
import io
import unittest
from unittest.mock import patch

import main
from digital_product import DigitalProduct
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount)
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from student_discount import StudentDiscount
from supplier import Supplier


def make_order_totalling_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
    order = Order("O1", discount)
    order.add_order_line(PhysicalProduct("P100", "Keyboard", 50, 20, 1.2, supplier), 3)
    order.add_order_line(DigitalProduct("D100", "Software", 100, 50, 750, supplier), 1)
    return order


class TestStrategies(unittest.TestCase):
    def test_discount_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_every_strategy_is_a_discount_strategy(self):
        for strategy in (NoDiscount(), PercentageDiscount(10),
                         BulkDiscount(200, 20), StudentDiscount()):
            with self.subTest(strategy=type(strategy).__name__):
                self.assertIsInstance(strategy, DiscountStrategy)

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225.0)
        self.assertAlmostEqual(PercentageDiscount(100).apply(250), 0.0)

    def test_bulk_discount_at_above_and_below_threshold(self):
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250), 230)
        self.assertEqual(bulk.apply(200), 180)   # "200 or more"
        self.assertEqual(bulk.apply(199.99), 199.99)

    def test_bulk_discount_never_makes_total_negative(self):
        self.assertEqual(BulkDiscount(0, 20).apply(5), 0.0)

    def test_student_discount_takes_five_percent(self):
        self.assertAlmostEqual(StudentDiscount().apply(250), 237.5)

    def test_invalid_strategy_settings_are_rejected(self):
        for build in (lambda: PercentageDiscount(0), lambda: PercentageDiscount(-5),
                      lambda: PercentageDiscount(101), lambda: BulkDiscount(-1, 20),
                      lambda: BulkDiscount(200, 0)):
            with self.assertRaises(ValueError):
                build()


class TestOrderUsesStrategy(unittest.TestCase):
    """Section 7: totals go through a strategy, with no if/elif in Order."""

    def test_default_strategy_is_no_discount(self):
        order = make_order_totalling_250()
        self.assertIsInstance(order.discount, NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_bulk_then_percentage_predict_first(self):
        order = make_order_totalling_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225)
        self.assertEqual(order.calculate_subtotal(), 250)

    def test_order_delegates_to_strategy_apply(self):
        class RecordingDiscount(DiscountStrategy):
            def __init__(self):
                self.received = None

            def apply(self, total: float) -> float:
                self.received = total
                return 1.0

        recorder = RecordingDiscount()
        order = make_order_totalling_250(recorder)
        self.assertEqual(order.calculate_total(), 1.0)
        self.assertEqual(recorder.received, 250)

    def test_order_contains_no_discount_type_logic(self):
        source = inspect.getsource(Order)
        for word in ("elif", "Percentage", "Bulk", "Student", "isinstance"):
            with self.subTest(word=word):
                self.assertNotIn(word, source)

    def test_new_strategy_needs_no_change_to_order(self):
        # A strategy invented inside the test: Order has never heard of it.
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        self.assertEqual(make_order_totalling_250(HalfPrice()).calculate_total(), 125)

    def test_two_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        first = make_order_totalling_250(shared)
        second = make_order_totalling_250(shared)
        self.assertIs(first.discount, second.discount)
        self.assertAlmostEqual(first.calculate_total(), 225)

    def test_display_shows_subtotal_discount_and_total(self):
        order = make_order_totalling_250(BulkDiscount(200, 20))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            order.display_information()
        self.assertIn("Subtotal: $250.00", output.getvalue())
        self.assertIn("Discount: 20 off orders of 200 or more", output.getvalue())
        self.assertIn("Order total: $230.00", output.getvalue())


class TestDiscountMenu(unittest.TestCase):
    def run_menu(self, answers):
        supplier = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
        inventory = Inventory()
        inventory.add_product(PhysicalProduct("P100", "Keyboard", 50, 20, 1.2, supplier))
        orders: dict[str, Order] = {}
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), contextlib.redirect_stdout(output):
            main.manage_orders(inventory, orders)
        return orders, output.getvalue()

    def test_menu_sets_student_discount(self):
        orders, output = self.run_menu(
            ["1", "O1", "2", "O1", "P100", "4", "6", "O1", "4", "3", "O1", "7"])
        self.assertIsInstance(orders["O1"].discount, StudentDiscount)
        self.assertIn("Order total: $190.00", output)

    def test_menu_rejects_invalid_discount_and_keeps_old_one(self):
        orders, output = self.run_menu(["1", "O1", "6", "O1", "9", "7"])
        self.assertIsInstance(orders["O1"].discount, NoDiscount)
        self.assertIn("Unknown discount option.", output)

    def test_menu_rejects_invalid_percentage(self):
        orders, output = self.run_menu(["1", "O1", "6", "O1", "2", "150", "7"])
        self.assertIsInstance(orders["O1"].discount, NoDiscount)
        self.assertIn("Percentage must be greater than 0", output)


if __name__ == "__main__":
    unittest.main()
