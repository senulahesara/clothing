from flask import Flask, request
from pywa import WhatsApp
import os

app = Flask(__name__)

wa = WhatsApp(
    phone_number_id=os.getenv('PHONE_NUMBER_ID'),
    token=os.getenv('ACCESS_TOKEN'),
    verify_token=os.getenv('VERIFY_TOKEN')
)

stock = {
    "pink skirt": {"price": 2500, "sizes": ["S", "M", "L"]},
    "black tshirt": {"price": 1800, "sizes": ["M", "L"]}
}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        return wa.handle_verification(request)
    else:
        return wa.handle_request(request)

@wa.on_message()
def reply(ctx):
    msg = ctx.message.text.lower()

    if "pink skirt" in msg:
        item = stock["pink skirt"]
        ctx.reply(f"👗 Yes! Pink Skirt is Rs. {item['price']}. Sizes: {', '.join(item['sizes'])}.")
    elif "order" in msg:
        ctx.reply("📝 Great! What’s your full name, address, and phone number?")
    elif "custom" in msg:
        ctx.reply("✨ What color, fabric, and size would you like?")
    else:
        ctx.reply("👋 Hello! Type 'pink skirt', 'custom', or 'order' to get started!")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
