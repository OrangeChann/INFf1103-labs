# INF1103 Lab 6 – Reflection Questions

## 1. What is the difference between a class and an object?
A class is a blueprint that defines what data (attributes) and behaviour (methods) something will have. An object is a single instance created from that blueprint, holding its own values. In my program, `Product` is the class; `Product("P001", "Laptop", 1200.00, 15)` and `Product("P002", "Mouse", 25.50, 40)` are two separate objects made from it, each with its own ID, name, price and stock.

## 2. Why is Product a suitable class for this system?
"Product" is one of the main nouns in the description of the system, and every product shares the same structure (ID, name, price, stock) and the same behaviour (update its stock, display itself). In Week 5 each product was a loose dictionary, and the code that changed it lived in separate functions. Making it a class keeps a product's data and the operations on that data together in one place.

## 3. What data belongs inside a Product object?
Only the information that describes one product:
- `__product_id` (String)
- `__name` (String)
- `__price` (float)
- `__stock` (int)

Things like the list of all products, the file path or the menu do not belong in a Product.

## 4. Why should the Product class manage its own stock rather than the main program directly changing it?
If the main program set the stock directly, the Product would have no control over what value it gets, and invalid states such as negative stock could slip in from anywhere in the code. With `update_stock(quantity)`, the Product checks the value first (it raises a `ValueError` for negative stock) before assigning it to `self.__stock`. The rule lives in one place, so every caller (the menu, the Inventory, the file loader) gets the same validation, and if the rule changes later only the Product needs to change.

## 5. What does encapsulation mean in your program?
Encapsulation means hiding an object's internal data and only allowing access through its public methods. In my program:
- `Product` stores its attributes as private (`__product_id`, `__name`, `__price`, `__stock`). Other code reads them through `get_...()` methods and changes stock only through `update_stock()`.
- `Inventory` keeps its list as private `__products`. Outside code uses `add_product()`, `search_product()`, `update_stock()` and `display_all()`, and `get_products()` returns a copy so the real list cannot be changed from outside.
- `InventoryFile` keeps its `__file_path` private.

Python does not strictly enforce this. Writing `product.__stock = 50` from outside just creates a new attribute and leaves the real stock unchanged, because of name mangling (the real attribute is `_Product__stock`). The double underscore still shows clearly which data is internal.

## 6. What is the responsibility of the Product class?
To represent and manage a single product: store its information, control changes to its own state (stock), and display its own details. It does not read user input, show the menu, load or save files, or manage other products.

## 7. What is the responsibility of the Inventory class?
To manage a collection of Product objects: store them, add new ones (rejecting duplicate IDs), search for one by ID, pass stock updates on to the right Product, and display all products. It does not deal with files or user input.

## 8. How does separating these responsibilities demonstrate the Single Responsibility Principle?
Each part of the program has one clear reason to change:
- `Product` changes only if what a product is or how it behaves changes.
- `Inventory` changes only if the way the collection is managed changes.
- `InventoryFile` changes only if the storage format or location changes (e.g. JSON to a database).
- `main.py` changes only if the menu or user interaction changes.

For example, I could switch from JSON to CSV by editing only `InventoryFile`, without touching `Product`, `Inventory` or the menu. In Week 5 all of these jobs were mixed together in one file of functions working on shared dictionaries.

## 9. What information does the main program need to know about a Product?
Only its public interface: how to create one (`Product(product_id, name, price, stock)`), the getter methods it uses when showing details (`get_name()`, `get_stock()`), and that `display_information()` prints the product. For stock changes it goes through `inventory.update_stock()`. It also needs to know that the constructor and `update_stock()` raise `ValueError` for invalid values, so it can show the user an error message.

## 10. What information about the internal implementation of Product does the main program not need to know?
- The names of the private attributes (`__stock`, `__price`, etc.) and the fact that Python name-mangles them.
- How the values are stored internally (e.g. that price is converted to `float` and stock to `int`).
- The exact validation logic inside `update_stock()` and `__init__`.
- How `display_information()` formats its output.

Because the main program does not depend on these details, they can change inside `Product` without breaking the rest of the program.
