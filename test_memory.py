from memory import BudgetMemory

memory = BudgetMemory()

memory.add_user("Add ₹200 for pizza.")
memory.add_assistant("Expense added.")
memory.add_tool("add_expense", {"amount": 200})

memory.add_user("How much have I spent?")

for msg in memory.get_messages():
    print(msg)