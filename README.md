# Grocery Agent

Agentic grocery ordering system that accepts a grocery list on WhatsApp, compares prices with Claude, and sends a Razorpay payment link after user confirmation.

## Flow

1. User sends a grocery list on WhatsApp.
2. Twilio forwards the WhatsApp webhook to an ngrok URL.
3. ngrok forwards the request to the local FastAPI app in `main.py`.
4. `main.py` calls `agents/grocery_agent.py`.
5. Claude parses the grocery list and compares prices from the mock price database.
6. `main.py` sends the price comparison back to the user on WhatsApp.
7. User replies `YES`.
8. `main.py` reads the saved session and calls `agents/payment_agent.py`.
9. Razorpay creates a payment link.
10. The payment link is sent back to the user on WhatsApp.

## Project Structure

```text
.
├── main.py                    # FastAPI webhook, session handling, Twilio replies
├── agents/
│   ├── grocery_agent.py       # Claude grocery parsing and price comparison
│   ├── payment_agent.py       # Razorpay payment link creation
│   ├── parser_agent.py
│   └── price_checker.py
├── requirements.txt
└── test_claude.py             # Claude API smoke test
```

## Environment Variables

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```

Do not commit `.env`.

## Local Setup

```bash
cd /Users/yogeshsoni/Projects/Grocery-agents
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install razorpay
```

`razorpay` is imported by `agents/payment_agent.py`. If it is not already installed in your environment, install it with the command above.

## Run The App

Start FastAPI:

```bash
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

Start ngrok in another terminal:

```bash
ngrok http 8000
```

Copy the HTTPS forwarding URL from ngrok and configure Twilio WhatsApp sandbox webhook:

```text
https://your-ngrok-url.ngrok-free.app/whatsapp
```

Use `POST` as the webhook method.

## Test The Happy Path

Send a WhatsApp message to the Twilio sandbox:

```text
2 litre milk, dozen eggs, brown bread
```

Expected behavior:

1. Terminal logs show the incoming Twilio message.
2. Terminal logs show `Calling process_grocery_message...`.
3. WhatsApp receives a price comparison.
4. Reply `YES`.
5. WhatsApp receives a Razorpay payment link.

## Useful Commands

Check the app starts syntactically:

```bash
venv/bin/python -m py_compile main.py agents/grocery_agent.py agents/payment_agent.py
```

Test Claude separately:

```bash
venv/bin/python test_claude.py
```

See the latest Git commit:

```bash
git log -1 --oneline
```

## Debugging Notes

### WhatsApp receives no reply after `Has alnum: True`

The May 2026 fix in `main.py` addressed this by:

- Removing an accidental early `return` that caused non-empty messages to exit before grocery processing.
- Running blocking Claude and Razorpay calls with `asyncio.to_thread(...)`.
- Adding a 10 second timeout around `process_grocery_message(...)`.
- Initializing `reply` before branching so it is always defined.
- Wrapping grocery processing in `try/except`.
- Sending a fallback WhatsApp reply when Claude, parsing, payment, or Twilio fails.
- Parsing totals with regex instead of `line.split("₹")[-1]`.

If this issue returns, watch for these log lines:

```text
Message from: ...
Message content: ...
Has alnum: True
Calling process_grocery_message...
process_grocery_message took: ...
Reply sent to ...
```

If `Calling process_grocery_message...` appears but no comparison is returned, check:

- `ANTHROPIC_API_KEY` is present and valid.
- The Claude model name in `agents/grocery_agent.py` is available.
- The request finishes before `GROCERY_AGENT_TIMEOUT_SECONDS`.
- Network access is working from the machine running FastAPI.

If payment link generation fails after replying `YES`, check:

- `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`.
- The `razorpay` Python package is installed.
- The `total` saved in `user_sessions` is numeric.

## Current Price Database

The mock prices are stored in `agents/grocery_agent.py`:

```text
milk, eggs, bread, butter, rice, sugar, salt, oil, onion, tomato
```

Items outside this list may be returned as unavailable by the grocery agent.
