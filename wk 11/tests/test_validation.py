"""Lab 9, section 4 (validation) and section 7: invalid prices, stock
quantities and order quantities are rejected."""
import unittest

from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from supplier import Supplier

SUPPLIER = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
TYPES = ("physical", "digital", "subscription")


def make(product_type: str = "physical", price: float = 25.0, stock: int = 5):
    return ProductFactory.create(product_type, "X1", "Item", price, stock, SUPPLIER)


class TestPriceValidation(unittest.TestCase):
    def test_zero_and_negative_prices_rejected_for_every_type(self):
        for product_type in TYPES:
            for price in (0, -0.01, -5):
                with self.subTest(product_type=product_type, price=price):
                    with self.assertRaises(ValueError) as caught:
                        make(product_type, price=price)
                    self.assertEqual(str(caught.exception),
                                     "Price must be greater than zero.")

    def test_smallest_positive_price_accepted(self):
        self.assertEqual(make(price=0.01).get_price(), 0.01)


class TestStockValidation(unittest.TestCase):
    def test_negative_stock_rejected_on_creation_for_every_type(self):
        for product_type in TYPES:
            with self.subTest(product_type=product_type):
                with self.assertRaises(ValueError) as caught:
                    make(product_type, stock=-1)
                self.assertEqual(str(caught.exception),
                                 "Stock quantity cannot be negative.")

    def test_zero_stock_is_allowed(self):
        self.assertEqual(make(stock=0).get_stock(), 0)

    def test_negative_update_rejected_and_stock_unchanged_for_every_type(self):
        # Section 4 predict first: no subtype may skip or change this rule (LSP).
        for product_type in TYPES:
            with self.subTest(product_type=product_type):
                product = make(product_type, stock=7)
                with self.assertRaises(ValueError):
                    product.update_stock(-1)
                self.assertEqual(product.get_stock(), 7)
                product.update_stock(0)
                self.assertEqual(product.get_stock(), 0)

    def test_subclasses_inherit_rather_than_override_stock_rule(self):
        for product_type in TYPES:
            with self.subTest(product_type=product_type):
                self.assertNotIn("update_stock", type(make(product_type)).__dict__)


class TestOrderLineQuantity(unittest.TestCase):
    def test_zero_and_negative_quantities_rejected(self):
        for quantity in (0, -1, -10):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError) as caught:
                    OrderLine(make(), quantity)
                self.assertEqual(str(caught.exception),
                                 "Quantity must be greater than zero.")

    def test_order_rejects_bad_line_and_keeps_existing_lines(self):
        order = Order("O1")
        order.add_order_line(make(), 2)
        with self.assertRaises(ValueError):
            order.add_order_line(make(), 0)
        self.assertEqual(len(order.order_lines), 1)
        self.assertEqual(order.calculate_total(), 50.0)


if __name__ == "__main__":
    unittest.main()
