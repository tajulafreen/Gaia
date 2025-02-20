# Gaia

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

pip install openai

from openai import OpenAI

client = OpenAI(
api_key="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"
)

completion = client.chat.completions.create(
model="gpt-4o-mini",
store=True,
messages=[
{"role": "user", "content": "write a haiku about ai"}
]
)

print(completion.choices[0].message);
