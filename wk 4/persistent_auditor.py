import os
import ast

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.txt")

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            total_line = f.readline().strip()
            history_line = f.readline().strip()

        total_units = int(total_line.split("=")[-1].strip())

        try:
            history = ast.literal_eval(history_line) if history_line else []
        except (ValueError, SyntaxError):
            history = []

        return total_units, history
    except FileNotFoundError:
        with open(INVENTORY_FILE, "w") as f:
            f.write("Total inventory = 0")
        return 0, []
    except ValueError:
        return 0, []

def save_inventory(total_units, transaction_history=None):
    with open(INVENTORY_FILE, "w") as f:
        f.write("Total inventory = " + str(total_units))
        if transaction_history is not None:
            f.write("\n" + str(transaction_history))

def clear_inventory():
    save_inventory(0, [])
    return 0, []

inventory, transaction_history = load_inventory()
fail = 0
delivery_count = 0

if transaction_history:
    next_order_id = max(order_id for order_id, _, _ in transaction_history) + 1
else:
    next_order_id = 1

print("Current Orders:")
if transaction_history:
    for order_id, product_name, quantity in transaction_history:
        print("Id:",order_id, "| Product Name:", product_name,  "| Quantity:", quantity)
else:
    print(0)

def get_valid_input():
    global fail
    while True:
        userInput = input("Enter Product Name, 'Clear' to reset, or 'Exit': ")
        if userInput == "Exit":
            return None

        if userInput.lower() == "clear":
            return "clear"

        product_name = userInput

        while True:
            quantityInput = input("Enter stock quantity: ")
            if not quantityInput.isnumeric():
                print("Invalid input, please enter a positive number.")
                fail += 1
            else:
                return product_name, int(quantityInput)

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts, delivery_count, transaction_history):
    print("Total inventory:", total_units)
    print("Number of errors:", failed_attempts)
    print("Total Number of deliveries:", delivery_count)
    print("Transaction history:", transaction_history)

while True:
    value = get_valid_input()

    if value == "clear":
        inventory, transaction_history = clear_inventory()
        fail = 0
        delivery_count = 0
        next_order_id = 1
        print("Inventory cleared. Starting fresh.")
        continue

    if value is None:
        save_inventory(inventory, transaction_history)
        print("Number of errors:", fail)
        print("Order successfully saved to inventory.txt")
        break

    product_name, quantity = value
    inventory = process_delivery(inventory, quantity)
    transaction_history.append((next_order_id, product_name, quantity))
    save_inventory(inventory, transaction_history)
    delivery_count += 1
    tax = calculate_tax(quantity)
    print()
    print("New Order Added:", next_order_id, ",", product_name, ",", quantity)
    print("Order successfully saved to inventory.txt")
    print("Total inventory:", inventory, "| Tax on this delivery:", tax, "| Delivery count:", delivery_count)
    print()
    next_order_id += 1

    if inventory > 500:
        print("Print Inventory is full, please stop adding stock.")
        break