import os

from can_be_shipped import CanBeShipped
from product_factory import ProductFactory
from inventory import Inventory, LINE
from inventory_file import InventoryFile
from product import Product
from supplier import Supplier
from order import Order
from discount_strategy import (DiscountStrategy, NoDiscount,
                               PercentageDiscount, BulkDiscount)
from student_discount import StudentDiscount

INVENTORY_FILE = os.environ.get(
    "INVENTORY_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json"),
)


# Lab 9, section 3: the menu only maps a choice to a product type name and the
# one extra detail to ask for. Which class to build is the factory's decision.
# menu choice: (factory type, extra detail keyword, prompt, converter)
PRODUCT_MENU: dict[str, tuple[str, str, str, type]] = {
    "1": ("physical", "weight", "Weight (kg): ", float),
    "2": ("digital", "download_size", "Download Size (MB): ", float),
    "3": ("subscription", "duration_months", "Duration (months): ", int),
}


def create_product(menu_choice: str, product_id: str, name: str, price: float,
                   stock: int, supplier: Supplier) -> Product:
    """Ask for the extra detail this type needs, then let the factory build it."""
    product_type, detail, prompt, convert = PRODUCT_MENU[menu_choice]
    value = convert(input(prompt))
    return ProductFactory.create(product_type, product_id, name, price, stock,
                                 supplier, **{detail: value})


def choose_supplier(inventory: Inventory) -> Supplier:
    """Section 2: create a supplier separately, or reuse an existing supplier."""
    supplier_id = input("Supplier ID: ").strip()
    if not supplier_id:
        raise ValueError("Supplier ID cannot be empty.")
    for product in inventory.products:
        if product.supplier.supplier_id.casefold() == supplier_id.casefold():
            product.supplier.display_information()
            return product.supplier
    name = input("Supplier Name: ").strip()
    email = input("Supplier Contact Email: ").strip()
    if not name or not email:
        raise ValueError("Supplier name and email cannot be empty.")
    return Supplier(supplier_id, name, email)


def add_product(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    print("3. Subscription Product")
    product_type = input("Product Type: ").strip()
    if product_type not in PRODUCT_MENU:
        print("\nInvalid product type. Product not added.")
        return
    product_id = input("Product ID: ").strip()
    if not product_id:
        print("\nProduct ID cannot be empty. Product not added.")
        return
    if inventory.search_product(product_id):
        print("\nA product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
        supplier = choose_supplier(inventory)
        product = create_product(product_type, product_id, name, price, stock, supplier)
    except ValueError as error:
        print(f"\nInvalid value entered ({error}). Product not added.")
        return
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print("Name:", product.get_name())
    print("Current Stock:", product.get_stock())
    try:
        new_stock = int(input("\nNew Stock Quantity: "))
        inventory.update_stock(product_id, new_stock)
    except ValueError as error:
        print(f"\nInvalid quantity ({error}). Stock not updated.")
        return
    print("\nStock updated successfully!")


def search_product(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(f"    Fulfilment: {product.get_fulfilment_info()}")
    # Only products that signed the CanBeShipped contract have a shipping cost.
    if isinstance(product, CanBeShipped):
        print(f"    Shipping Cost: ${product.calculate_shipping_cost():.2f}")
    print(LINE)


def remove_product(inventory: Inventory) -> None:
    """Section 3.2: remove membership without destroying products used by orders."""
    product_id = input("Product ID to remove: ").strip()
    if inventory.remove_product(product_id):
        print("Product removed from inventory.")
    else:
        print("Product not found.")


def choose_discount() -> DiscountStrategy:
    """Lab 9, section 2: the menu creates the strategy the user picks.

    Order never sees this choice; it only calls apply() on what it is given.
    """
    print("1. No Discount")
    print("2. Percentage Discount")
    print("3. Bulk Discount (20 off orders of 200 or more)")
    print("4. Student Discount (5% off)")
    choice = input("Discount option: ").strip()
    if choice == "1":
        return NoDiscount()
    if choice == "2":
        return PercentageDiscount(float(input("Percentage off: ")))
    if choice == "3":
        return BulkDiscount(200, 20)
    if choice == "4":
        return StudentDiscount()
    raise ValueError("Unknown discount option.")


def manage_orders(inventory: Inventory, orders: dict[str, Order]) -> None:
    """Section 4: orders own their lines; this menu only supplies products/quantities."""
    while True:
        print("\nORDERS (current session)")
        print("1. Create Order\n2. Add Order Line\n3. Display Order")
        print("4. Remove Order Line\n5. Cancel Order\n6. Set Discount\n7. Back")
        choice = input("Order option: ").strip()
        if choice == "7":
            return
        if choice not in ("1", "2", "3", "4", "5", "6"):
            print("Invalid order option.")
            continue
        order_id = input("Order ID: ").strip()
        if choice == "1":
            if not order_id or order_id in orders:
                print("Order ID must be nonempty and unique.")
            else:
                orders[order_id] = Order(order_id)
                print("Order created.")
            continue
        order = orders.get(order_id)
        if order is None:
            print("Order not found.")
            continue
        try:
            if choice == "2":
                product = inventory.find_product(input("Product ID: ").strip())
                if product is None:
                    print("Product not found.")
                    continue
                order.add_order_line(product, int(input("Quantity: ")))
                print("Order line added.")
            elif choice == "3":
                order.display_information()
            elif choice == "4":
                order.remove_order_line(int(input("Line number (starting at 1): ")) - 1)
                print("Order line removed.")
            elif choice == "5":
                order.cancel()
                print("Order cancelled; its lines were removed.")
            elif choice == "6":
                order.set_discount(choose_discount())
                print(f"Discount set: {order.discount}")
        except (ValueError, IndexError) as error:
            print(f"Invalid order operation: {error}")


def print_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("7. Remove Product")
    print("8. Manage Orders")
    print("----------------------------")


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM (OOP)")
    print("=" * 40)
    print()

    inventory = Inventory()
    inventory_file = InventoryFile(INVENTORY_FILE)
    inventory_file.load(inventory)
    orders: dict[str, Order] = {}

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            inventory_file.save(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            inventory_file.save(inventory)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        elif choice == "7":
            remove_product(inventory)
        elif choice == "8":
            manage_orders(inventory, orders)
        else:
            print("\nInvalid option. Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()
