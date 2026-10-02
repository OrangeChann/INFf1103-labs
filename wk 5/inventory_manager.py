import os
import json

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")

LINE = "-" * 48


def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found. Starting with an empty inventory.")
        return []
    print("inventory.json found.")
    try:
        with open(INVENTORY_FILE, "r") as f:
            products = json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Could not read inventory.json. Starting with an empty inventory.")
        return []
    print("Inventory loaded successfully.")
    return products


def save_inventory(products):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(products, f, indent=4)


def find_product(products, product_id):
    for product in products:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def display_all(products):
    print("\nCurrent Inventory")
    print(LINE)
    if not products:
        print("Inventory is empty.")
    for p in products:
        print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")
    print(LINE)


def add_product(products):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if find_product(products, product_id):
        print("\nA product with that ID already exists.")
        return
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("\nInvalid price or quantity. Product not added.")
        return
    if price < 0 or stock < 0:
        print("\nPrice and stock cannot be negative. Product not added.")
        return
    products.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")


def update_stock(products):
    print("\nUpdate Stock")
    product = find_product(products, input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print("Name:", product["name"])
    print("Current Stock:", product["stock"])
    try:
        new_stock = int(input("\nNew Stock Quantity: "))
    except ValueError:
        print("\nInvalid quantity. Stock not updated.")
        return
    if new_stock < 0:
        print("\nStock cannot be negative. Stock not updated.")
        return
    product["stock"] = new_stock
    print("\nStock updated successfully!")


def search_product(products):
    print("\nSearch Product")
    product = find_product(products, input("Enter Product ID: ").strip())
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print(LINE)
    print("ID:", product["id"])
    print("Name:", product["name"])
    print(f"Price: ${product['price']:.2f}")
    print("Stock:", product["stock"])
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
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()
    products = load_inventory()

    while True:
        print_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            display_all(products)
        elif choice == "2":
            add_product(products)
        elif choice == "3":
            update_stock(products)
        elif choice == "4":
            search_product(products)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(products)
            print("Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(products)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
