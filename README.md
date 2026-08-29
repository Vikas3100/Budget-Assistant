# Personal Budget Assistant (T1 – Finance)

**Course:** CSE476 – Agentic AI and Intelligent Automation
**Project:** CA1 – Build a Real Agent
**Topic:** T1 – Personal Budget Assistant

---

# Project Overview

The **Personal Budget Assistant** is an Agentic AI application developed as part of the CSE476 CA1 project. The objective of this project is to help students manage their monthly expenses through natural language conversations while demonstrating the three core characteristics of an AI agent required by the course:

* **Tool Calling**
* **Plan–Act Loop**
* **Conversation Memory**

Unlike a traditional chatbot that only generates text, this assistant performs real actions by selecting and executing Python tools, remembering previous interactions, and making decisions based on calculated results.

The project is implemented using the **OpenAI Python SDK** with the **Groq API** as the language model provider. The complete agent architecture was built manually using plain Python, following the structure demonstrated in the CSE476 lecture notebooks instead of using frameworks like LangChain or LangGraph.

---

# Features

The Personal Budget Assistant can:

* Add new expenses.
* Automatically categorize expenses.
* Calculate total spending.
* Calculate category-wise spending.
* Show remaining monthly budget.
* Remember previous expenses during the conversation.
* Decide whether a future purchase or trip is affordable.
* Execute multiple reasoning steps before producing the final answer.

Example:

> **User:** Can I afford a ₹2000 trip?

The agent performs the following steps:

1. Retrieves the current spending summary.
2. Calculates the remaining budget.
3. Compares the trip cost with the available balance.
4. Returns a reasoned decision.

This demonstrates true agentic behavior rather than simple text generation.

---

# Project Architecture

The project follows a modular architecture inspired by the CSE476 lecture notebooks.

User
↓
app.py (Plan–Act Loop)
↓
Groq Model (OpenAI SDK)
↙             ↘
schemas.py   registry.py
↓
tools.py
↓
memory.py

Each file has a single responsibility, making the project easier to understand, maintain, and explain during the viva.

---

# Project Structure

Personal_Budget2/
│
├── .env
├── config.py
├── tools.py
├── schemas.py
├── registry.py
├── memory.py
├── app.py
├── demo.ipynb
├── README.md
├── requirements.txt
│
├── test_connection.py
├── test_tools.py
├── test_registry.py
└── test_memory.py

---

# File-by-File Explanation

## 1. `.env`

### Purpose

Stores the Groq API key securely.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

### Why it is important

* Prevents exposing API keys inside source code.
* Makes the project safe for GitHub uploads.
* Separates sensitive configuration from application logic.

---

## 2. `requirements.txt`

### Purpose

Lists all required Python libraries.

```text
openai
python-dotenv
ipykernel
```

### Installation

```bash
pip install -r requirements.txt
```

This ensures anyone can recreate the same development environment.

---

## 3. `config.py`

### Purpose

Creates the connection between the application and the Groq API using the OpenAI SDK.

### Responsibilities

* Loads environment variables.
* Creates the API client.
* Stores the selected model.

Example:

```python
MODEL="openai/gpt-oss-20b"
```

This file keeps configuration separate from business logic, following the architecture demonstrated in the lecture notebooks.

---

## 4. `tools.py`

### Purpose

Contains the Python functions that perform actual work.

Instead of letting the model perform calculations internally, the agent calls these tools whenever real operations are needed.

### Tool 1 – `add_expense(item, amount)`

This function:

* Accepts an item name.
* Accepts the amount spent.
* Automatically classifies the expense.
* Stores the expense.

Example:

```python
add_expense("pizza",250)
```

Output:

* Category: Food
* Expense stored successfully.

### Automatic Categories

| Item   | Category  |
| ------ | --------- |
| Pizza  | Food      |
| Burger | Food      |
| Metro  | Transport |
| Bus    | Transport |
| Book   | Education |
| Others | Others    |

### Tool 2 – `get_summary(category)`

This function calculates:

* Total spending.
* Remaining budget.
* Category-wise spending.
* Individual category totals when requested.

Example:

```python
get_summary("all")
```

Returns:

* Total spent
* Remaining budget
* Food spending
* Transport spending
* Education spending

These two tools satisfy the project requirement of implementing at least two working tools.

---

## 5. `schemas.py`

### Purpose

Provides JSON tool schemas to the language model.

The model never receives the actual Python code.

Instead, it receives descriptions such as:

```json
{
"name":"add_expense",
"parameters":...
}
```

### Why schemas are important

The model first decides:

> "I need the add_expense tool."

Only after that does Python execute the function.

This matches the tool-calling mechanism demonstrated in the lecture notebooks.

---

## 6. `registry.py`

### Purpose

Implements a **Tool Whitelist**.

Example:

```python
REGISTRY={
"add_expense":add_expense,
"get_summary":get_summary
}
```

### Why this file exists

The model is never allowed to execute arbitrary Python code.

Instead:

1. Model requests a tool.
2. Registry checks whether the tool is allowed.
3. Approved tools are executed.
4. Unknown tools are rejected.

This improves security and follows the lecture architecture.

---

## 7. `memory.py`

### Purpose

Implements conversation memory.

The `BudgetMemory` class stores every conversation inside a `messages` list.

Example conversation stored:

System
↓
User
↓
Assistant
↓
Tool Result
↓
User
↓
Assistant

### Methods

* `add_user()`
* `add_assistant()`
* `add_tool()`
* `get_messages()`

### Why memory is important

Without memory:

* Every question becomes independent.

With memory:

* Earlier expenses remain available.
* Later questions can use previous information.

Example:

User:

> Add ₹300 for coffee.

Later:

> How much have I spent?

The assistant already remembers the earlier expense.

This converts the assistant into a **Model-Based Agent**, similar to the progression shown in the lecture notebooks.

---

## 8. `app.py`

### Purpose

This is the heart of the project.

It implements the complete **Plan–Act Loop**.

### Execution Flow

1. User enters a goal.
2. User message is stored.
3. Model receives:

   * Conversation history
   * Tool schemas
4. Model decides whether a tool is needed.
5. Registry executes the tool.
6. Tool result returns to memory.
7. Model decides whether another step is required.
8. Final answer is produced.

### Plan–Act Loop

User
↓
Model
↓
Tool Decision
↓
Registry
↓
Tool Execution
↓
Memory Update
↓
Final Answer

The loop continues until the model no longer requests additional tools.

This satisfies the project requirement that the agent performs multiple reasoning steps.

---

## 9. `demo.ipynb`

### Purpose

Demonstrates the complete working agent.

The notebook includes:

* Adding expenses.
* Multiple tool calls.
* Spending summaries.
* Agentic decision making.
* Memory demonstration.
* Tool execution traces.

The notebook should be executed before submission so the outputs remain visible.

---

# How the Plan–Act Loop Works

The Plan–Act Loop is the most important concept in this project.

Example:

> User: Can I afford a ₹2000 trip?

The assistant performs multiple steps.

### Step 1

Model plans.

> "I need the budget summary."

### Step 2

Model requests:

```text
get_summary()
```

### Step 3

Python executes the tool.

Example:

```text
Remaining Budget: ₹7800
```

### Step 4

Model reasons.

Since:

```text
7800 > 2000
```

The assistant concludes:

> "Yes, you can afford the trip."

Instead of generating an answer immediately, the assistant performs reasoning based on actual tool results.

---

# Example Conversations

### Example 1

**User**

> Add ₹250 for pizza.

Agent:

* Calls `add_expense()`.
* Categorizes as Food.
* Stores the expense.

---

### Example 2

**User**

> Add ₹120 for metro.

Agent:

* Calls `add_expense()`.
* Categorizes as Transport.

---

### Example 3

**User**

> How much have I spent?

Agent:

* Calls `get_summary()`.
* Calculates totals.
* Returns category-wise spending.

---

### Example 4

**User**

> Can I afford a ₹2000 trip?

Agent:

* Calls `get_summary()`.
* Calculates remaining budget.
* Makes a reasoned decision.

---

# Memory Demonstration

Conversation:

```text
User: Add ₹300 for coffee.
User: Add ₹500 for books.
User: How much have I spent?
```

The assistant remembers both previous expenses because they are stored inside `BudgetMemory.messages`.

No information needs to be entered again.

---

# Testing Performed

Several test files were created during development.

| File                 | Purpose                    |
| -------------------- | -------------------------- |
| `test_connection.py` | Verify API connection      |
| `test_tools.py`      | Test tool functions        |
| `test_registry.py`   | Verify whitelist execution |
| `test_memory.py`     | Verify conversation memory |

Each component was tested individually before integrating everything into the final agent.

---

# Development Process

The project was built incrementally by following the CSE476 lecture notebooks.

### Step 1

Created the project structure.

### Step 2

Connected the OpenAI SDK with the Groq API.

### Step 3

Built the budget tools.

### Step 4

Created tool schemas.

### Step 5

Implemented the tool registry.

### Step 6

Added conversation memory.

### Step 7

Built the manual Plan–Act Loop.

### Step 8

Created the demonstration notebook.

### Step 9

Tested every module individually.

This modular approach made debugging easier and ensured every component worked correctly before integration.

---

# Challenges Faced

### Challenge 1

Initially attempted to use LangChain and LangGraph.

**Issue**

The course lecture notebooks followed a manual OpenAI SDK architecture instead.

**Solution**

Rebuilt the project using plain Python, the OpenAI SDK, and a custom Plan–Act Loop.

---

### Challenge 2

Encountered a `model_not_found` error while connecting to Groq.

**Solution**

Switched to the supported free model `openai/gpt-oss-20b` and verified the connection successfully.

---

# Future Improvements

The current implementation satisfies the CA1 requirements, but future versions could include:

* Savings goals.
* Overspending warnings.
* Expense deletion.
* Monthly history.
* Charts and graphs.
* CSV export.
* Daily spending limits.

These features would make the assistant more practical while keeping the same agent architecture.

---

# Conclusion

The **Personal Budget Assistant** successfully demonstrates all three characteristics required for an Agentic AI system in CSE476.

* **Tool Calling** through `add_expense()` and `get_summary()`
* **Conversation Memory** through `BudgetMemory`
* **Plan–Act Loop** through the custom implementation in `app.py`

The project was built using the **OpenAI Python SDK**, **Groq API**, and **plain Python**, closely following the architecture demonstrated in the CSE476 lecture notebooks while satisfying the CA1 project requirements.
