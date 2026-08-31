# # app.py

# import json
# import sys

# # Ensure UTF-8 output encoding on Windows consoles
# if hasattr(sys.stdout, 'reconfigure'):
#     sys.stdout.reconfigure(encoding='utf-8', errors='replace')
# if hasattr(sys.stderr, 'reconfigure'):
#     sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# from config import client, MODEL
# from schemas import TOOLS
# from registry import REGISTRY
# from memory import BudgetMemory

# # Create memory object
# memory = BudgetMemory()


# def run_agent(user_input, max_steps=8):
#     """
#     Manual Plan-Act Loop
#     """

#     # Store user message
#     memory.add_user(user_input)

#     for step in range(max_steps):

#         response = client.chat.completions.create(
#             model=MODEL,
#             messages=memory.get_messages(),
#             tools=TOOLS,
#             tool_choice="auto"
#         )

#         message = response.choices[0].message

#         # If the model gives the final answer
#         if not message.tool_calls:

#             final_answer = message.content

#             memory.add_assistant(final_answer)

#             return final_answer

#         # Save assistant tool-call message
#         memory.get_messages().append({
#             "role": "assistant",
#             "content": message.content or "",
#             "tool_calls": [
#                 {
#                     "id": tc.id,
#                     "type": "function",
#                     "function": {
#                         "name": tc.function.name,
#                         "arguments": tc.function.arguments
#                     }
#                 }
#                 for tc in message.tool_calls
#             ]
#         })

#         # Execute each tool
#         for tool_call in message.tool_calls:

#             tool_name = tool_call.function.name
#             arguments = json.loads(tool_call.function.arguments)

#             print(f"\n[Step {step+1}] Tool Called -> {tool_name}")
#             print("Arguments:", arguments)

#             result = REGISTRY[tool_name](**arguments)

#             print("Result:", result)

#             # Send tool result back to the model
#             memory.get_messages().append({
#                 "role": "tool",
#                 "tool_call_id": tool_call.id,
#                 "content": json.dumps(result)
#             })

#     return "Stopped after reaching the maximum number of steps."

# def is_budget_query(message):
#     message = message.lower()

#     keywords = [
#         "budget", "salary", "income", "expense", "spent", "spend",
#         "food", "rent", "metro", "travel", "remaining", "balance",
#         "summary", "save", "saving", "money", "afford", "delete",
#         "remove", "add", "rupee", "₹"
#     ]

#     return any(word in message for word in keywords)
# if __name__ == "__main__":

#     print("=== Personal Budget Assistant ===")

#     while True:

#         user = input("\nYou: ")

#         if user.lower() in ["exit", "quit"]:
#             break

#         answer = run_agent(user)

#         print("\nAssistant:", answer)
# app.py

import json
import sys

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from config import client, MODEL
from schemas import TOOLS
from registry import REGISTRY
from memory import BudgetMemory

# Create memory object
memory = BudgetMemory()


def is_budget_query(message):
    """
    Checks whether the user's query is related to personal budgeting.
    """
    message = message.lower()

    keywords = [
        "budget", "salary", "income", "expense", "expenses",
        "spent", "spend", "food", "rent", "metro", "travel",
        "remaining", "balance", "summary", "save", "saving",
        "money", "afford", "delete", "remove", "add",
        "rupee", "₹", "budget limit", "monthly"
    ]

    return any(word in message for word in keywords)


def run_agent(user_input, max_steps=8):
    """
    Manual Plan-Act Loop
    """

    # Domain guard: Only allow budget-related questions
    if not is_budget_query(user_input):
        return (
            "I'm a Personal Budget Assistant. I can only help with budgeting, "
            "salary, income, expenses, savings, spending summaries, and "
            "affordability questions."
        )

    # Store user message
    memory.add_user(user_input)

    for step in range(max_steps):

        response = client.chat.completions.create(
            model=MODEL,
            messages=memory.get_messages(),
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # If the model gives the final answer
        if not message.tool_calls:

            final_answer = message.content

            memory.add_assistant(final_answer)

            return final_answer

        # Save assistant tool-call message
        memory.get_messages().append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in message.tool_calls
            ]
        })

        # Execute each tool
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print(f"\n[Step {step+1}] Tool Called -> {tool_name}")
            print("Arguments:", arguments)

            result = REGISTRY[tool_name](**arguments)

            print("Result:", result)

            # Send tool result back to the model
            memory.get_messages().append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Stopped after reaching the maximum number of steps."


if __name__ == "__main__":

    print("=== Personal Budget Assistant ===")

    while True:

        user = input("\nYou: ")

        if user.lower() in ["exit", "quit"]:
            break

        answer = run_agent(user)

        print("\nAssistant:", answer)