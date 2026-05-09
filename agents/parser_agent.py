import anthropic 
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def parse_grocery_message(user_message):
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user", 
                "content": f"""You are grocery list parser. 

Extract grocery items from this WhatsApp message and format them as a clean list.
For each item identify: name, quantity, and unit.
Reply in this exact format:
Got it! Here are your items:
- Item 1 - quantity unit
- Item 2 - quantity unit                
                
Message: {user_message}"""
            }
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    test_message = "2 litre milk, dozen eggs and brown bread"
    result = parse_grocery_message(test_message)
    print(result)

    