from tools import add_expense, delete_expense, get_summary

add_expense("pizza",500)
add_expense("metro",120)

print(get_summary())

print(delete_expense("pizza",500))

print(get_summary())