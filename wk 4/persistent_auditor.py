import os

INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.txt")

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            return int(f.readline().strip())
    except FileNotFoundError:
        with open(INVENTORY_FILE, "w") as f:
            f.write("0")
        return 0
    except ValueError:
        return 0

def save_inventory(total_units):
    with open(INVENTORY_FILE, "w") as f:
        f.write(str(total_units))

inventory = load_inventory()
fail = 0
delivery_count = 0

def get_valid_input():
    global fail
    while True:
        userInput = input("Enter stock quantity or Exit: ")
        if userInput == "Exit":
            return None

        if not userInput.isnumeric():
            print("Invalid input, please enter a positive number.")
            fail += 1
        else:
            return int(userInput)

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

while True:
    value = get_valid_input()

    if value is None:
        save_inventory(inventory)
        break

    inventory = process_delivery(inventory, value)
    save_inventory(inventory)
    delivery_count += 1
    tax = calculate_tax(value)
    print("Total inventory:", inventory, "| Tax on this delivery:", tax, "| Number of errors:", fail, "| Delivery count:", delivery_count)

    if inventory > 500:
        print("Print Inventory is full, please stop adding stock.")
        break
