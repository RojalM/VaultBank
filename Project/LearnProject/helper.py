def get_float_input(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError("Value must be positive")
            return value
        except ValueError as e:
            print(f"Invalid input: {e}")

def get_year_month():
    while True:
        try:
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (MM): "))
            return (month, year)
        except ValueError:
            print("Please enter numeric values")