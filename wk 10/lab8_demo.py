"""Lab 8, sections 2-7 and 9: labelled, repeatable relationship evidence.

Record predictions in lab8_notes.md BEFORE running: python -B lab8_demo.py
"""
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> None:
    """Section 6.2: this caller knows only the Product abstraction."""
    product.display_information()
    print(product.get_fulfilment_info())


def main() -> None:
    print("2.2 ASSOCIATION — prediction recorded before execution")
    supplier = Supplier("SUP1", "Music and Games", "sales@example.com")
    guitar = PhysicalProduct("P100", "Guitar", 300.0, 5, 3.5, supplier)
    game = DigitalProduct("D100", "Game", 60.0, 10, 2048.0, supplier)
    assert guitar is not supplier and game is not supplier
    assert guitar.supplier is game.supplier is supplier
    del supplier
    guitar.supplier.display_information()
    game.supplier.display_information()
    print("Both products retain the same supplier after del supplier: True")
    independent_supplier = Supplier("SUP2", "Independent Supplier", "other@example.com")
    independent_supplier.display_information()

    print("\n3.2 AGGREGATION — product existed before either inventory")
    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(guitar)
    assert inventory_a.remove_product("P100")
    assert inventory_a.find_product("P100") is None
    show_product_details(guitar)
    inventory_b.add_product(guitar)
    assert inventory_b.find_product("P100") is guitar
    print("Product still works after removal; Inventory B holds the same object: True")
    inventory_b.remove_product("P100")
    assert inventory_b.products == [] and guitar.get_name() == "Guitar"
    print("Emptying the inventory did not destroy the product: True")

    print("\n4.3 COMPOSITION — each order creates its own lines")
    first = Order("O1")
    second = Order("O2")
    first.add_order_line(guitar, 2)
    first.add_order_line(game, 3)
    second.add_order_line(guitar, 1)
    first.display_information()
    second.display_information()
    assert first.order_lines[0] is not second.order_lines[0]
    assert first.order_lines[0].product is second.order_lines[0].product is guitar
    print("For the shared guitar: 2 distinct OrderLines, 1 Product")
    print("Entire scenario: 3 OrderLines, 2 Products")
    first.remove_order_line(0)
    assert first.calculate_total() == 180.0
    print(f"O1 total after removing its guitar line: ${first.calculate_total():.2f}")
    second.cancel()
    assert second.order_lines == [] and guitar.get_stock() == 5
    print("Cancelling O2 removed its lines; the guitar remains usable: True")

    print("\n6.2 / 6.3 LSP — same Product caller and stock contract")
    products: list[Product] = [guitar, game]
    for product in products:
        show_product_details(product)
        product.update_stock(12)
        assert product.get_stock() == 12
        try:
            product.update_stock(-1)
        except ValueError:
            pass
        else:
            raise AssertionError("Product must reject negative stock")
        assert product.get_stock() == 12
    print("Both subtypes accept nonnegative stock and reject negative stock: True")

    print("\n7.2 POLYMORPHISM — one mixed Product collection, no subtype checks")
    inventory = Inventory()
    inventory.add_product(guitar)
    inventory.add_product(game)
    for product in inventory.products:
        product.display_information()
        print(product.get_fulfilment_info())
    print("\n9. REVIEW — all demonstration assertions passed")


if __name__ == "__main__":
    main()
