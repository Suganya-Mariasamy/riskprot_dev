# services/websocket_listener.py

import time
import os
from dotenv import load_dotenv
from twelvedata import TDClient
from supabase import create_client, Client

from models.market_data import MarketData

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
url = os.getenv("SUPABASE_URL")  # Get Supabase API URL from environment variable
key = os.getenv("SUPABASE_KEY")   # Get Supabase anon key from environment variable

# Create a Supabase client
supabase: Client = create_client(url, key)

# List to store received messages
messages_history = []

# Define a data model for market data
class MarketData:
    def __init__(self, symbol: str, price: float):
        self.symbol = symbol
        self.price = price

# Callback function to process incoming WebSocket messages
def on_event(e):
    # Print the received event data
    print(e)
    messages_history.append(e)
    # Extract data to insert into Supabase
    if 'symbol' in e and 'price' in e:
        # Create a MarketData instance
        market_data = MarketData(symbol=e['symbol'], price=e['price'])
        
        # Insert data into Supabase
        supabase.table('market_data').insert({
            'symbol': market_data.symbol,
            'price': market_data.price
        }).execute()

# Function to start the WebSocket listener
def start_websocket_listener():
    # Initialize the TDClient with your API key
    td = TDClient(apikey=os.getenv("TWELVEDATA_API_KEY"))  # Replace with your actual API key from env

    # Create a WebSocket connection for the specified symbol
    ws = td.websocket(symbols="GOOGL", on_event=on_event)

    # Subscribe to additional symbols
    ws.subscribe(['ETH/BTC', 'AAPL', 'GOOGL', 'RELIANCE.NS', 'TATAMOTORS.NS', 'HDFCBANK.NS'])

    # Connect to the WebSocket
    ws.connect()

    # Keep the application running to receive messages
    try:
        while True:
            print('messages received: ', len(messages_history))  # Display the number of received messages
            ws.heartbeat()  # Send a heartbeat to keep the connection alive
            time.sleep(10)  # Wait for 10 seconds before the next iteration
    except KeyboardInterrupt:
        print("Exiting...")  # Handle exit gracefully
        ws.close()  # Close the WebSocket connection
