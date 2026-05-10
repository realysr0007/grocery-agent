import razorpay 
import os
from dotenv import load_dotenv

load_dotenv()

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)

def create_payment_link(amount, platform, description):
    payment_link = client.payment_link.create({
        "amount": int(float(amount)) * 100,  # Amount in paise
        "currency": "INR",
        "description": f"Grocery order via {platform}: {description}",
        "reminder_enable": False,
        "notify": {
            "sms": False,
            "email": False
        },
    })
    return payment_link["short_url"]

if __name__ == "__main__":
    link = create_payment_link(489, "Instamart", "Rice 3kg, Sugar 3kg")
    print(f"Payment link: {link}")