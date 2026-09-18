inventory = int(0)
fail = 0

while True:
    userInput = input("Enter stock quantity or Exit: ")
    if userInput == "Exit":
        fail += 1
        break

    if not userInput.isnumeric():
        print("Invalid input, please enter a positive number.")
    else:
        inventory += int(userInput)
        print("Inventory:", inventory)
        if inventory >= 500:
            print("Inventory is full, please stop adding stock.")
            break

print("Total inventory:", inventory, "| Number of errors:", fail)
