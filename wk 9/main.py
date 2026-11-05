import os

from product import Product
from inventory import Inventory, LINE
from inventory_file import InventoryFile

INVENTORY_FILE = os.environ.get(
    "INVENTORY_FILE",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json"),
)


def add_product(inventory):
    print("\nAdd New Product")
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
        product = Product(product_id, name, price, stock)
    except ValueError as error:
        print(f"\nInvalid price or quantity ({error}). Product not added.")
        return
    inventory.add_product(product)
    print("\nProduct added successfully!")


def update_stock(inventory):
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


def search_product(inventory):
    print("\nSearch Product")
    product = inventory.search_product(input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    product.display_information()
    print(LINE)


def print_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM (OOP)")
    print("=" * 40)
    print()

    inventory = Inventory()
    inventory_file = InventoryFile(INVENTORY_FILE)
    inventory_file.load(inventory)

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
        else:
            print("\nInvalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
