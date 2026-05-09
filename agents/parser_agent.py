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

Extract grocery items from this WhatsApp message and format them as a clean numbered list.
For each item identify: name, quantity, and unit.

Rules:
- If quantity is mentioned, use it
- If unit is mentioned (kg, litre, dozen, packet), use it
- If "each" is used, apply that quantity to all items
- Always respond in this exact format:

Here are your items:
1. Item Name - Xkg
2. Item Name - Xkg             
                
Message: {user_message}"""
            }
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    test_message = "2 litre milk, dozen eggs and brown bread"
    result = parse_grocery_message(test_message)
    print(result)

    