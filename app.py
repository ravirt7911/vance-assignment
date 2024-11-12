from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from  
import yfinance as yf
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

swagger = Swagger(app)  

# In-memory SQLite database connection
conn = sqlite3.connect(':memory:', check_same_thread=False)

# Function to fetch historical data for given currency pair
def fetch_historic_data(from_currency, to_currency, period):
    quote = f'{from_currency}{to_currency}=X'
    
    end_date = datetime.now()
    if period == '1W':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1M':
        start_date = end_date - timedelta(weeks=4)
    elif period == '3M':
        start_date = end_date - timedelta(weeks=12)
    elif period == '6M':
        start_date = end_date - timedelta(weeks=26)
    elif period == '1Y':
        start_date = end_date - timedelta(weeks=52)
    else:
        return None  # Invalid period
    
    ticker = yf.Ticker(quote)
    data = ticker.history(start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    
    return data

# Function to scrape and store data periodically
def scrape_and_store():
    currencies = [('GBP', 'INR'), ('AED', 'INR')]
    periods = ['1W', '1M', '3M', '6M', '1Y']
    
    for from_currency, to_currency in currencies:
        for period in periods:
            historic_data_df = fetch_historic_data(from_currency, to_currency, period)
            if historic_data_df is not None and not historic_data_df.empty:
                historic_data_df.to_sql('forex_data', conn, if_exists='replace', index=True)

# Schedule the scraping every hour
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_and_store, 'interval', hours=1)
scheduler.start()

@app.route('/api/forex-data/', methods=['POST', 'GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'Successful response',
            'examples': {
                'application/json': [
                    {'Date': '2024-01-01', 'Close': 75.0},
                    {'Date': '2024-01-02', 'Close': 76.0}
                ]
            }
        },
        400: {
            'description': 'Missing required parameters'
        },
        404: {
            'description': 'No data found for the given parameters'
        }
    }
})
def get_forex_data():
    logging.info("Fetching forex data")
    try:
        from_currency = request.args.get('from')
        to_currency = request.args.get('to')
        period = request.args.get('period')

        if not from_currency or not to_currency or not period:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        historic_data_df = fetch_historic_data(from_currency, to_currency, period)

        if historic_data_df is None or historic_data_df.empty:
            return jsonify({'error': 'No data found for the given parameters'}), 404
        
        historic_data_df.to_sql('forex_data', conn, if_exists='replace', index=True)
        result_df = pd.read_sql_query("SELECT * FROM forex_data", conn)
        
        return jsonify(result_df.to_dict(orient='records')), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return error message if something goes wrong

if __name__ == "__main__":
    app.run(debug=True, port=5006)