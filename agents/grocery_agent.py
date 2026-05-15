import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

MOCK_PRICES = {
    "milk": {"blinkit": 28, "instamart": 30},
    "eggs": {"blinkit": 80, "instamart": 75},
    "bread": {"blinkit": 45, "instamart": 50},
    "butter": {"blinkit": 55, "instamart": 52},
    "rice": {"blinkit": 120, "instamart": 115},
    "sugar": {"blinkit": 45, "instamart": 48},
    "salt": {"blinkit": 20, "instamart": 18},
    "oil": {"blinkit": 150, "instamart": 145},
    "onion": {"blinkit": 30, "instamart": 35},
    "tomato": {"blinkit": 40, "instamart": 38},
}

def process_grocery_message(user_message):
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a grocery price comparison assistant.

Given this grocery message: {user_message}

And these prices (per unit in rupees):
{MOCK_PRICES}

Do these steps in one response:
1. Extract grocery items with quantities
2. Match each item to the price database
3. Calculate totals for both platforms
4. Find the best deal

Reply in exactly this format:
🛒 Price Comparison:

Blinkit: ₹[total]
Instamart: ₹[total]

[Winner] saves you ₹[difference]!

Item breakdown:
- [item] [quantity] - Blinkit ₹[price] vs Instamart ₹[price]

Unavailable items: [list any items not in database, or 'None']

Reply YES to confirm order on [winner]."""
            }
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    test = "2 litre milk, dozen eggs and brown bread"
    result = process_grocery_message(test)
    print(result)