from registry import REGISTRY

result = REGISTRY["add_expense"]("coffee", 120)
print(result)

print(REGISTRY["get_summary"]())