import os
from openai import OpenAI

client = OpenAI(
    base_url=os.environ["LLM_BASE_URL"],   # https://openrouter.ai/api/v1
    api_key=os.environ["LLM_API_KEY"],     # your real OpenRouter key
)

res = client.chat.completions.create(
    model=os.environ["LLM_MODEL"],         # "openrouter/free"
    messages=[{"role": "user", "content": "Reply with exactly the word: ready"}],
)

print(res.choices[0].message.content)