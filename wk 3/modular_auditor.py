inventory = int(0)
fail = 0
delivery_count = 0

def get_valid_input():
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

def generate_report(total_units, failed_attempts, delivery_count):
    print("Total inventory:", total_units)
    print("Number of errors:", failed_attempts)
    print("Total Number of deliveries:", delivery_count)

while True:
    value = get_valid_input()

    if value == "quit":
        break

    if value is None:
        fail+=1
        break
    print("Total inventory:", inventory, "| Number of errors:", fail)

    inventory = process_delivery(inventory, value)
    delivery_count += 1
    tax = calculate_tax(value)
    print("Inventory:", inventory, "| Tax on this delivery:", tax)

    if inventory > 500:
        print("Print Inventory is full, please stop adding stock.")
        break