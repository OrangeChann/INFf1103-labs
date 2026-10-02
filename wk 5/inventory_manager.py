LINE = "-" * 48


products = [
    {"id": "P001", "name": "Laptop", "price": 1200.0, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.5, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.0, "stock": 25},
]


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


if __name__ == "__main__":
    display_all(products)
    add_product(products)
    update_stock(products)
    search_product(products)
    display_all(products)
