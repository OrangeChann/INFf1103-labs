inventory = int(0)
fail = 0

while True:
    userInput = input("Enter stock quantity or Exit: ")
    if userInput == "Exit":
        break

    if not userInput.isnumeric():
        print("Invalid input, please enter a positive number.")
    else:
        inventory += int(userInput)
        print("Inventory:", inventory)
        if inventory >= 500:
            print("Inventory is full, please stop adding stock.")
            break
     