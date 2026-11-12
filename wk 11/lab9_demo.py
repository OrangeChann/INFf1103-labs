"""Lab 9: labelled evidence for each "Predict first" question.

Write your prediction in lab9_notes.md BEFORE running: python -B lab9_demo.py
"""
import inspect

from digital_product import DigitalProduct
from discount_strategy import BulkDiscount, PercentageDiscount
from order import Order
from physical_product import PhysicalProduct
from student_discount import StudentDiscount
from supplier import Supplier


def section_2() -> None:
    supplier = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
    keyboard = PhysicalProduct("P100", "Keyboard", 50.0, 20, 1.2, supplier)
    software = DigitalProduct("D100", "Office Software", 100.0, 50, 750.0, supplier)

    print("2.1 OCP CHECK - does Order mention any discount type?")
    order_source = inspect.getsource(Order)
    for name in ("Percentage", "Bulk", "Student", "elif"):
        print(f"  '{name}' appears in Order: {name in order_source}")

    print("\n2.3 STRATEGY - lines adding up to 250")
    order = Order("O1", BulkDiscount(200, 20))
    order.add_order_line(keyboard, 3)   # 3 x 50  = 150
    order.add_order_line(software, 1)   # 1 x 100 = 100
    print(f"  Subtotal: {order.calculate_subtotal():.2f}")
    print(f"  BulkDiscount(200, 20)  -> calculate_total() = {order.calculate_total():.2f}")
    order.set_discount(PercentageDiscount(10))
    print(f"  set_discount(PercentageDiscount(10)) -> {order.calculate_total():.2f}")

    print("\n2.4 EXTEND WITHOUT MODIFYING - StudentDiscount on the same order")
    order.set_discount(StudentDiscount())
    print(f"  StudentDiscount() -> {order.calculate_total():.2f}")

    print("\n2.4 RELATIONSHIP - can two orders share one strategy object?")
    shared = PercentageDiscount(10)
    first, second = Order("O2", shared), Order("O3", shared)
    first.add_order_line(keyboard, 2)    # 100
    second.add_order_line(software, 3)   # 300
    print(f"  Same object used by both orders: {first.discount is second.discount}")
    print(f"  O2 total: {first.calculate_total():.2f} | O3 total: {second.calculate_total():.2f}")
    del first, second
    print(f"  Strategy still usable after both orders deleted: {shared.apply(50):.2f}")
    print(f"  Default strategy when none given: {Order('O4').discount}")


def main() -> None:
    print("=" * 60)
    print("SECTION 2 - STRATEGY PATTERN")
    print("=" * 60)
    section_2()


if __name__ == "__main__":
    main()
