import os
from dotenv import load_dotenv
import anthropic

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

def check_prices(parsed_message):
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a price checking assistant.
Given this parsed grocery list:
{parsed_message}

And these prices (per unit in rupees):
{MOCK_PRICES}

Calculate the total cost on Blinkit and Instamart.
Match each item to the closest key in the price data.
If an item is not found, mention it as unavailable.

Reply in exactly this format:
🛒 Price Comparison:

Blinkit: ₹[total]
Instamart: ₹[total]

[Winner] saves you ₹[difference]!

Item breakdown:
- [item] - Blinkit ₹[price] vs Instamart ₹[price]

Reply YES to confirm order on [winner]."""
            }
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    test_parsed = """Got it! Here are your items:
- Milk - 2 litre
- Eggs - 1 dozen
- Bread - 1 loaf"""
    result = check_prices(test_parsed)
    print(result)