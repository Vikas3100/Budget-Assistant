# schemas.py

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "add_expense",
            "description": "Add a new expense to the user's monthly budget.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Name of the purchased item."
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount spent in rupees."
                    }
                },
                "required": ["item", "amount"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_summary",
            "description": "Return a spending summary for all categories or a specific category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category name or 'all'."
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_expense",
            "description": "Delete a previously recorded expense.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Name of the expense item."
                    },
                    "amount": {
                        "type": "number",
                        "description": "Amount to delete."
                    }
                },
                "required": ["item", "amount"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "set_budget",
            "description": "Set or update the user's monthly salary, income, or monthly budget limit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Monthly budget or salary amount in rupees."
                    }
                },
                "required": ["amount"]
            }
        }
    }

]