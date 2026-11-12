"""Lab 9: labelled evidence for each "Predict first" question.

Write your prediction in lab9_notes.md BEFORE running: python -B lab9_demo.py
"""
import inspect
import subprocess
import sys

import inventory_file
import main as menu
from discount_strategy import BulkDiscount, PercentageDiscount
from order import Order
from product import Product
from product_factory import ProductFactory
from student_discount import StudentDiscount
from supplier import Supplier


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def section_2() -> None:
    supplier = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
    keyboard = ProductFactory.create("physical", "P100", "Keyboard", 50.0, 20,
                                     supplier, weight=1.2)
    software = ProductFactory.create("digital", "D100", "Office Software", 100.0,
                                     50, supplier, download_size=750.0)

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


def section_3() -> None:
    supplier = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")

    print("3.2 FACTORY - the factory returns the right subclass as a Product")
    for product_type in ("physical", "digital", "subscription"):
        product: Product = ProductFactory.create(
            product_type, "X1", "Example", 10.0, 1, supplier)
        print(f"  create({product_type!r}) -> {type(product).__name__}: "
              f"{product.get_fulfilment_info()}")

    print("\n3.2 UNKNOWN TYPE - caught here so the demo can continue")
    try:
        ProductFactory.create("service", "S001", "Installation", 30.0, 5, supplier)
    except ValueError as error:
        print(f"  ValueError caught: {error}")

    print("\n3.2 UNKNOWN TYPE - NOT caught (run as a separate program)")
    code = "\n".join([
        "from product_factory import ProductFactory",
        "from supplier import Supplier",
        "s = Supplier('SUP1', 'Office Supplies Ltd', 'sales@example.com')",
        "ProductFactory.create('service', 'S001', 'Installation', 30.0, 5, s)",
        "print('This line never runs')",
    ])
    result = subprocess.run([sys.executable, "-B", "-c", code], text=True,
                            capture_output=True)
    for line in result.stderr.strip().splitlines():
        print(f"  | {line}")
    print(f"  stdout: {result.stdout.strip() or '(nothing - the print never ran)'}")
    print(f"  Exit code: {result.returncode}")

    print("\n3.3 WHO KNOWS ABOUT WHAT - concrete classes imported by each file")
    for module in (menu, inventory_file):
        source = inspect.getsource(module)
        known = [name for name in ("PhysicalProduct", "DigitalProduct",
                                   "SubscriptionProduct") if f"import {name}" in source]
        print(f"  {module.__name__}.py imports: {known or 'none - it uses ProductFactory'}")


def try_it(label: str, action) -> None:
    """Run one action and show whether validation accepted or rejected it."""
    try:
        action()
    except ValueError as error:
        print(f"  {label:<44} -> rejected: {error}")
    else:
        print(f"  {label:<44} -> accepted")


def section_4() -> None:
    supplier = Supplier("SUP1", "Office Supplies Ltd", "sales@example.com")
    create = ProductFactory.create

    print("4. VALIDATION - each rule is checked by the class that owns it")
    try_it("Product price 0", lambda: create("physical", "P1", "Lamp", 0, 5, supplier))
    try_it("Product price -5", lambda: create("physical", "P1", "Lamp", -5, 5, supplier))
    try_it("Product price 0.01", lambda: create("physical", "P1", "Lamp", 0.01, 5, supplier))
    try_it("Product stock -1", lambda: create("physical", "P1", "Lamp", 25, -1, supplier))
    try_it("Product stock 0", lambda: create("physical", "P1", "Lamp", 25, 0, supplier))
    lamp = create("physical", "P1", "Lamp", 25, 5, supplier)
    order = Order("O1")
    try_it("OrderLine quantity 0", lambda: order.add_order_line(lamp, 0))
    try_it("OrderLine quantity -2", lambda: order.add_order_line(lamp, -2))
    try_it("OrderLine quantity 1", lambda: order.add_order_line(lamp, 1))

    print("\n4. PREDICT FIRST - does DigitalProduct keep Product's stock rule?")
    app = create("digital", "D1", "Photo Editor", 49.90, 100, supplier)
    try_it("DigitalProduct created with stock -1",
           lambda: create("digital", "D2", "Editor", 49.90, -1, supplier))
    try_it("DigitalProduct update_stock(-1)", lambda: app.update_stock(-1))
    print(f"  Stock after rejected update: {app.get_stock()} (unchanged)")
    try_it("DigitalProduct update_stock(0)", lambda: app.update_stock(0))
    overrides = "update_stock" in type(app).__dict__
    print(f"  DigitalProduct overrides update_stock: {overrides} (rule is inherited)")


def main() -> None:
    heading("SECTION 2 - STRATEGY PATTERN")
    section_2()
    heading("SECTION 3 - FACTORY PATTERN")
    section_3()
    heading("SECTION 4 - VALIDATION")
    section_4()


if __name__ == "__main__":
    main()
