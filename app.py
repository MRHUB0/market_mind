from flask import Flask, request, jsonify
import os
import yfinance as yf
from openai import AzureOpenAI
from dotenv import load_dotenv
from utils.firebase import verify_firebase_token
from utils.usage import has_free_access, increment_usage
from utils.referrals import track_referral, get_referral_credits

# Load environment variables
load_dotenv()

# Azure OpenAI Client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
)

app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok"})

@app.route("/analyze", methods=["GET"])
def analyze():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_firebase_token(token)
    if not user_id:
        return jsonify({"error": "Unauthorized or invalid token"}), 401

    if not has_free_access(user_id):
        return jsonify({
            "error": "Daily limit reached. Refer 3 friends to unlock more access.",
            "limitReached": True
        }), 403

    ticker = request.args.get("ticker", "").upper()
    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400

    try:
        data = yf.Ticker(ticker).history(period="1d", interval="15m")
        if data.empty:
            return jsonify({"error": f"No data found for ticker {ticker}"}), 404

        price_data = data["Close"].tolist()
        latest_price = price_data[-1]
        previous_close = price_data[0]
        direction = "up" if latest_price > previous_close else "down"

        prompt = f"Based on current market data and sentiment, would you advise to buy, sell, or hold {ticker}? The latest price is {latest_price}."
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        sentiment = response.choices[0].message.content.strip()
        increment_usage(user_id)

        return jsonify({
            "user": user_id,
            "ticker": ticker,
            "price": latest_price,
            "sentiment": sentiment,
            "direction": direction
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/referral", methods=["POST"])
def referral():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_firebase_token(token)
    if not user_id:
        return jsonify({"error": "Unauthorized or invalid token"}), 401

    try:
        data = request.get_json()
        invitee_id = data.get("invitee_id", "")
        if not invitee_id:
            return jsonify({"error": "Missing invitee_id"}), 400

        success, message = track_referral(user_id, invitee_id)
        if not success:
            return jsonify({"error": message}), 400

        return jsonify({
            "message": message,
            "user": user_id,
            "unlocked": True
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/credits", methods=["GET"])
def credits():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_firebase_token(token)
    if not user_id:
        return jsonify({"error": "Unauthorized or invalid token"}), 401

    try:
        credits = get_referral_credits(user_id)
        return jsonify({
            "user": user_id,
            "credits": credits
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
