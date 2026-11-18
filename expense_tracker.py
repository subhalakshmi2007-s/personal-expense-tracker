import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDNAMES = ["date", "category", "description", "amount"]


def create_file():
    """Create the CSV file with a header if it does not exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def load_expenses():
    """Read and validate expense records from the CSV file."""
    create_file()
    expenses = []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                datetime.strptime(row["date"], "%Y-%m-%d")
                amount = float(row["amount"])

                if amount < 0:
                    continue
                if not row["category"].strip() or not row["description"].strip():
                    continue

                row["amount"] = amount
                expenses.append(row)
            except (ValueError, KeyError, TypeError):
                # Ignore rows that contain invalid or incomplete data.
                continue

    return expenses


def save_expense(expense):
    """Append one expense to the CSV file."""
    create_file()
    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(expense)


def get_valid_date():
    while True:
        date_text = input("Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("Invalid date. Example: 2026-11-18")


def get_valid_amount():
    while True:
        amount_text = input("Amount: ").strip()
        try:
            amount = float(amount_text)
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number, such as 120 or 45.50.")


def add_expense():
    print("\n--- Add Expense ---")
    date = get_valid_date()

    category = input("Category (Food/Travel/Study/Bills/Fun): ").strip().title()
    while not category:
        print("Category cannot be empty.")
        category = input("Category: ").strip().title()

    description = input("Description: ").strip()
    while not description:
        print("Description cannot be empty.")
        description = input("Description: ").strip()

    amount = get_valid_amount()

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": f"{amount:.2f}"
    }
    save_expense(expense)
    print("Expense saved successfully!")


def display_expenses(expenses):
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n{:<12} {:<14} {:<25} {:>10}".format(
        "Date", "Category", "Description", "Amount"
    ))
    print("-" * 65)

    for expense in expenses:
        print("{:<12} {:<14} {:<25} {:>10.2f}".format(
            expense["date"],
            expense["category"][:14],
            expense["description"][:25],
            expense["amount"]
        ))


def view_expenses():
    print("\n--- All Expenses ---")
    display_expenses(load_expenses())


def filter_expenses():
    expenses = load_expenses()

    print("\n1. Filter by category")
    print("2. Filter by month")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        category = input("Enter category: ").strip().lower()
        filtered = [
            expense for expense in expenses
            if expense["category"].lower() == category
        ]
    elif choice == "2":
        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
            filtered = [
                expense for expense in expenses
                if expense["date"][:7] == month
            ]
        except ValueError:
            print("Invalid month. Use YYYY-MM, for example 2026-11.")
            return
    else:
        print("Invalid choice.")
        return

    display_expenses(filtered)


def show_summary():
    expenses = load_expenses()

    if not expenses:
        print("\nNo expenses available for summary.")
        return

    totals = {}
    grand_total = 0

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        totals[category] = totals.get(category, 0) + amount
        grand_total += amount

    print("\n--- Category Summary ---")
    for category, total in sorted(totals.items()):
        print(f"{category:<15} Rs. {total:.2f}")

    biggest = max(expenses, key=lambda expense: expense["amount"])

    print("-" * 30)
    print(f"Grand Total: Rs. {grand_total:.2f}")
    print(
        "Biggest Expense: "
        f"{biggest['description']} - Rs. {biggest['amount']:.2f}"
    )


def main():
    create_file()

    while True:
        print("\n====== PERSONAL EXPENSE TRACKER ======")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses")
        print("4. Category Summary")
        print("5. Quit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            show_summary()
        elif choice == "5":
            print("Thank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    main()
