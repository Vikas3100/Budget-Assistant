from config import client, MODEL

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": "Say hello in one sentence."}
    ]
)

print(response.choices[0].message.content)