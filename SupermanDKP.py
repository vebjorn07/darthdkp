import os
from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ["CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])


user_points = {}

boss_values = {
    "170": {"4*": 10, "5*": 20, "6*": 30},
    "180": {"4*": 10, "5*": 20, "6*": 30},
    "185": {"4*": 5, "5*": 10, "6*": 20},
    "190": {"4*": 5, "5*": 10, "6*": 20},
    "195": {"4*": 5, "5*": 10, "6*": 20},
    "200": {"4*": 5, "5*": 10, "6*": 20},
    "205": {"4*": 5, "5*": 10, "6*": 30},
    "210": {"4*": 15, "5*": 30, "6*": 40},
    "215": {"4*": 15, "5*": 30, "6*": 40},
    "RB": {"5*": 20, "6*": 40},
    "Aggy": 15,
    "Mono": {"5*": 20, "6*": 40},
    "Hrung": 50,
    "Mord": 60,
    "Necro": 80,
    "Prot base": 150,
    "Prot prime": 250,
    "Gele": 300,
    "BT": 400,
    "Dino": 500,
}

item_values = {
    'dark_necro_mord': 200,
    'shadow_necro_mord': 300,
    'void_necro_mord': 400,
    'mighty_jewel': 100,
    'majestic_jewel': 150,
    'royal_jewel': 200,
    'imperial_jewel': 300,
    'godly_jewel': 400,
    'majestic_legacy_hrung': 100,
    'mighty_legacy_hrung': 200,
    'royal_legacy_hrung': 300,
    'imperial_legacy_hrung': 400,
    'godly_legacy_hrung': 500,
    'mighty_prot': 400,
    'majestic_prot': 800,
    'royal_prot': 1200,
    'imperial_prot': 1600,
    'godly_prot': 2000,
    'mighty_gele': 1000,
    'majestic_gele': 2000,
    'royal_gele': 3000,
    'imperial_gele': 4000,
    'godly_gele': 5000,
    'dark_gele_weapon': 2000,
    'shadow_gele_weapon': 3000,
    'void_gele_weapon': 4500,
}

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError: 
        abort(400)
    
    return "OK"

def generate_leaderboard_text():
    leaderboard_text = "Leaderboard:\n"
    sorted_points = sorted(user_points.items(), key=lambda x: x[1], reverse=True)

    for user_id, points in sorted_points:
        profile = line_bot_api.get_profile(user_id)
        leaderboard_text += f"{profile.display_name}: {points}\n"

    return leaderboard_text

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text

    if text.lower() == "leaderboard":
        reply_text = generate_leaderboard_text()
    elif text.lower().startswith("kill"):
        try:
            split_text = text.split(' ')
            boss_name = split_text[1]
            star_rating = split_text[2]

            if boss_name in boss_values:
                if isinstance(boss_values[boss_name], dict):
                    points = boss_values[boss_name].get(star_rating)
                else:
                    points = boss_values[boss_name]

                if points:
                    if user_id in user_points:
                        user_points[user_id] += points
                    else:
                        user_points[user_id] = points

                    reply_text = f"You've earned {points} points for the {boss_name} kill."
                else:
                    reply_text = f"Invalid star rating for {boss_name}."
            else:
                reply_text = "Invalid boss name."
        except IndexError:
            reply_text = "Incorrect format. Use 'kill [boss_name] [star_rating]'."
    else:
        reply_text = "Unknown command."

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


