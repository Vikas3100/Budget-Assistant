# tools.py

# Stores expenses during the session
expenses = []
deleted_expenses = []

# Default monthly budget (0 until set by user)
monthly_budget = 0
budget_set = False


def set_budget(amount):
    """
    Tool 4:
    Sets the user's monthly budget or monthly salary.
    """
    global monthly_budget, budget_set
    monthly_budget = float(amount)
    budget_set = True

    return {
        "status": "success",
        "monthly_budget": monthly_budget,
        "message": f"Monthly budget/salary has been set to ₹{int(monthly_budget):,}."
    }


def classify_category(item):
    """Automatically classify an expense."""

    item = item.lower()

    if item in ["pizza", "burger", "coffee", "tea", "food", "dinner", "lunch", "breakfast", "groceries"]:
        return "Food"

    elif item in ["metro", "bus", "uber", "petrol", "cab", "auto", "train", "flight"]:
        return "Transport"

    elif item in ["book", "pen", "notebook", "course", "tuition", "fees"]:
        return "Education"

    elif item in ["rent", "room rent", "flat rent", "electricity", "wifi", "bill", "maintenance"]:
        return "Housing & Bills"

    elif item in ["movie", "game", "party", "shopping", "clothes"]:
        return "Entertainment"

    else:
        return "Others"


def add_expense(item, amount):
    """
    Tool 1:
    Adds an expense and stores it.
    """

    category = classify_category(item)

    expense = {
        "item": item,
        "amount": amount,
        "category": category
    }
    expenses.append(expense)

    return {
        "status": "success",
        "item": item,
        "amount": amount,
        "category": category
    }

def delete_expense(item, amount):
    """
    Tool 3:
    Deletes one matching expense.
    """

    item = item.lower()

    for expense in expenses:
        if expense["item"].lower() == item and float(expense["amount"]) == float(amount):
            expenses.remove(expense)
            deleted_expenses.append(expense)

            return {
                "status": "success",
                "message": f"Removed ₹{amount} for {item}."
            }

    return {
        "status": "failed",
        "message": f"No matching expense found for {item} worth ₹{amount}."
    }

def get_summary(category="all"):
    """
    Tool 2:
    Returns spending summary.
    """

    total = sum(e["amount"] for e in expenses)
    total_deleted = sum(e["amount"] for e in deleted_expenses)

    if category.lower() == "all":
        categories = {}
        for e in expenses:
            categories[e["category"]] = categories.get(e["category"], 0) + e["amount"]

        remaining = (monthly_budget - total) if budget_set else 0

        return {
            "monthly_budget": monthly_budget,
            "budget_set": budget_set,
            "total_spent": total,
            "total_deleted": total_deleted,
            "remaining_budget": remaining,
            "categories": categories,
            "expenses": expenses,
            "deleted_expenses": deleted_expenses
        }

    category_total = sum(
        e["amount"]
        for e in expenses
        if e["category"].lower() == category.lower()
    )

    return {
        "category": category,
        "total": category_total
    }
