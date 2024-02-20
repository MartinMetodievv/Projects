from Expense_Tracker.expense import Expense
import datetime
import calendar


def main():
    print("🎯Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 2000

    # Get user input for expense.
    expense = get_user_expense()
    # Write their expense to a file.
    save_expense_to_a_file(expense, expense_file_path)
    # Read file and summarize expenses.
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print("🎯Getting User Expense")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍔 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "👕 Shopping",
    ]
    while True:
        print("Select a category: ")
        for number, name in enumerate(expense_categories):
            print(f"  {number + 1}. {name}")
        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category. Please try again!")


def save_expense_to_a_file(expense: Expense, expense_file_path):
    # To save something to a file first need to open the file.\
    # And to open the file I need to know file name.\
    # And since I'm going to read the file later with my summarized expenses,\
    # I want to use the name as a constant or maybe as a second argument, but using global constant is quit dangerous\
    # because it's hard to debug the app and to be sure which variable you're actually using.
    print(f"🎯Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.category},{expense.amount}\n")


def summarize_expenses(expense_file_path, budget):
    print("🎯Summarizing User Expense")
    expenses = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()  # list of string
        for line in lines:
            expense_name, expense_category, expense_amount = line.strip().split(",")
            line_expense = Expense(name=expense_name,
                                   amount=float(expense_amount),
                                   category=expense_category
                                   )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")
    total_spend = sum([x.amount for x in expenses])
    remaining_budget = budget - total_spend

    if remaining_budget <= 0:
        budget = 0
        print("Hey! You go over budget!")
    else:
        print(f"💶You've spent ${total_spend:.2f} this month!")
        print(f"✅Budget Remaining: ${remaining_budget:.2f} this month!")

    # Get the current date
    now = datetime.datetime.now()
    # Get the number of days in the current month
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    # Calculate the remaining days
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days
    print(green(f"👉Budget Per Day: ${daily_budget:.2f}"))


def green(text):
    return f"\033[92m{text}\033[0m"


if __name__ == "__main__":
    main()
