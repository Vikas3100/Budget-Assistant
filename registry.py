# registry.py

from tools import add_expense, get_summary, delete_expense, set_budget

# Whitelist of allowed tools
REGISTRY = {
    "add_expense": add_expense,
    "get_summary": get_summary,
    "delete_expense": delete_expense,
    "set_budget": set_budget
}