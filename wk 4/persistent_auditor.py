import os
import ast

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.txt")

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            total_line = f.readline().strip()
            history_line = f.readline().strip()

        total_units = int(total_line)

        try:
            history = ast.literal_eval(history_line) if history_line else []
        except (ValueError, SyntaxError):
            history = []

        return total_units, history
    except FileNotFoundError:
        with open(INVENTORY_FILE, "w") as f:
            f.write("0")
        return 0, []
    except ValueError:
        return 0, []

def save_inventory(total_units, transaction_history=None):
    with open(INVENTORY_FILE, "w") as f:
        f.write(str(total_units))
        if transaction_history is not None:
            f.write("\n" + str(transaction_history))

inventory, transaction_history = load_inventory()
fail = 0
delivery_count = 0

def get_valid_input():
    global fail
    while True:
        userInput = input("Enter Product Name or Exit: ")
        if userInput == "Exit":
            return None

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

while True:
    value = get_valid_input()

    if value is None:
        save_inventory(inventory, transaction_history)
        break

    product_name, quantity = value
    inventory = process_delivery(inventory, quantity)
    transaction_history.append((product_name, quantity))
    save_inventory(inventory)
    delivery_count += 1
    tax = calculate_tax(quantity)
    print("New Order Added:", product_name, quantity)
    print("Total inventory:", inventory, "| Tax on this delivery:", tax, "| Number of errors:", fail, "| Delivery count:", delivery_count)

    if inventory > 500:
        print("Print Inventory is full, please stop adding stock.")
        break
