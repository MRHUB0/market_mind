from flask import Flask, request, jsonify
import os
import yfinance as yf
from openai import AzureOpenAI
from dotenv import load_dotenv
from utils.firebase import verify_firebase_token

# Load environment variables
load_dotenv()

# Azure OpenAI Client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT")
)

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def health():
    return jsonify({"status": "ok"})

@app.route("/analyze", methods=["GET"])
def analyze():
    # Firebase Auth check
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    user_id = verify_firebase_token(token)
    if not user_id:
        return jsonify({"error": "Unauthorized or invalid token"}), 401

    # Parse input
    ticker = request.args.get("ticker", "").upper()
    if not ticker:
        return jsonify({"error": "Missing 'ticker' parameter"}), 400

    try:
        # Get intraday stock data
        data = yf.Ticker(ticker).history(period="1d", interval="15m")
        if data.empty:
            return jsonify({"error": f"No data found for ticker {ticker}"}), 404

        price_data = data["Close"].tolist()
        latest_price = price_data[-1]
        previous_close = price_data[0]

        # Determine if stock is rising or falling
        is_rising = latest_price > previous_close
        direction = "up" if is_rising else "down"

        # Generate sentiment from OpenAI
        prompt = f"Based on current market data and sentiment, would you advise to buy, sell, or hold {ticker}? The latest price is {latest_price}."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        sentiment = response.choices[0].message.content.strip()

        return jsonify({
            "user": user_id,
            "ticker": ticker,
            "price": latest_price,
            "sentiment": sentiment,
            "direction": direction  # "up" or "down"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run locally
if __name__ == "__main__":
    app.run(debug=True, port=5000)
