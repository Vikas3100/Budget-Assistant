# memory.py

class BudgetMemory:
    """
    Stores conversation history just like the ModelBasedAgent
    from the lecture.
    """

    def __init__(self):
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a smart Personal Budget Assistant. "
                    "Always use the available tools to record actions: "
                    "- When the user states their salary, income, or monthly budget (e.g., 'my salary is 60,000' or 'set budget to 50000'), call the set_budget tool with the specified amount. "
                    "- When the user mentions an expense or spending (e.g., 'room rent 25000', 'spent 500 on food'), call the add_expense tool. "
                    "- When the user wants to remove or delete an expense, call the delete_expense tool. "
                    "- When the user asks for their balance, remaining budget, spending summary, or if they can afford a purchase, call the get_summary tool. "
                    "Provide helpful, concise, and well-reasoned answers based on tool results."
                )
            }
        ]

    def add_user(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant(self, message):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def add_tool(self, tool_name, result):
        self.messages.append({
            "role": "tool",
            "name": tool_name,
            "content": str(result)
        })

    def get_messages(self):
        return self.messages