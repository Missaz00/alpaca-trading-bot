
import os
from flask import Flask, request, jsonify
import alpaca_trade_api as tradeapi

app = Flask(__name__)

# Alpaca API credentials from environment
APCA_API_KEY_ID = os.getenv("APCA_API_KEY_ID")
APCA_API_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
APCA_API_BASE_URL = os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets")

# Customizable order size (defaults to 1 if not set)
ORDER_SIZE = int(os.getenv("ORDER_SIZE", 1))

# Connect to Alpaca
api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'action' not in data or 'symbol' not in data:
        return jsonify({"error": "Invalid request format"}), 400

    symbol = data['symbol']
    action = data['action'].lower()

    try:
        if action == 'buy':
            api.submit_order(symbol=symbol, qty=ORDER_SIZE, side='buy', type='market', time_in_force='gtc')
        elif action == 'sell':
            api.submit_order(symbol=symbol, qty=ORDER_SIZE, side='sell', type='market', time_in_force='gtc')
        else:
            return jsonify({"error": "Invalid action"}), 400

        return jsonify({"status": "Order submitted", "symbol": symbol, "action": action, "qty": ORDER_SIZE}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
