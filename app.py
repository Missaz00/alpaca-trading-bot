
from flask import Flask, request, jsonify
import os
import alpaca_trade_api as tradeapi

app = Flask(__name__)

# Alpaca API keys (from environment variables)
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
BASE_URL = "https://paper-api.alpaca.markets"

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    action = data.get('action')
    symbol = data.get('symbol', 'AAPL')

    try:
        if action == 'buy':
            api.submit_order(symbol=symbol, qty=1, side='buy', type='market', time_in_force='gtc')
            return jsonify({'message': f'Buy order sent for {symbol}'})
        elif action == 'sell':
            api.submit_order(symbol=symbol, qty=1, side='sell', type='market', time_in_force='gtc')
            return jsonify({'message': f'Sell order sent for {symbol}'})
        elif action == 'close':
            api.close_position(symbol)
            return jsonify({'message': f'Position closed for {symbol}'})
        else:
            return jsonify({'error': 'Invalid action'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
