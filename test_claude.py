from dotenv import load_dotenv
import os
import anthropic

load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=anthropic_api_key)

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{"role": "user", "content": "I need to buy milk, eggs and bread. Can you list these as a grocery list?"}]
)

print(message.content[0].text)