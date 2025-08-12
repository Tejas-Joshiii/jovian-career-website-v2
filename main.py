
def main():
    print("Welcome to your new Python application!")
    print("This is a new Python file created in Replit.")
    
    # Example: Simple calculator
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        operation = input("Enter operation (+, -, *, /): ")
        
        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 != 0:
                result = num1 / num2
            else:
                print("Error: Division by zero!")
                return
        else:
            print("Invalid operation!")
            return
        
        print(f"Result: {num1} {operation} {num2} = {result}")
    except ValueError:
        print("Error: Please enter valid numbers!")

if __name__ == "__main__":
    main()
