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
            
   # Assuming ws is your websocket instance
    symbols = [
        "ABB:BSE", "ABB:NSE", "ABCAPITAL:NSE", "ABCAPITAL:BSE", "ABFRL:NSE", "ABFRL:BSE", 
        "ACC:BSE", "ACC:NSE", "ADANIENSOL:NSE", "ADANIENSOL:BSE", "ADANIENT:NSE", "ADANIENT:BSE", 
        "ADANIGREEN:BSE", "ADANIGREEN:NSE", "ADANIPORTS:BSE", "ADANIPORTS:NSE", "ADANIPOWER:NSE", 
        "ADANIPOWER:BSE", "ALKEM:BSE", "ALKEM:NSE", "AMBUJACEM:BSE", "AMBUJACEM:NSE", "APLAPOLLO:NSE", 
        "APLAPOLLO:BSE", "APOLLOHOSP:NSE", "APOLLOHOSP:BSE", "APOLLOTYRE:BSE", "APOLLOTYRE:NSE", 
        "ASHOKLEY:BSE", "ASHOKLEY:NSE", "ASIANPAINT:NSE", "ASIANPAINT:BSE", "ASTRAL:BSE", "ASTRAL:NSE", 
        "ATGL:BSE", "ATGL:NSE", "AUBANK:BSE", "AUBANK:NSE", "AUROPHARMA:NSE", "AUROPHARMA:BSE", 
        "AXISBANK:NSE", "AXISBANK:BSE", "BAJAJFINSV:BSE", "BAJAJFINSV:NSE", "BAJAJHLDNG:BSE", 
        "BAJAJHLDNG:NSE", "BAJFINANCE:BSE", "BAJFINANCE:NSE", "BALKRISIND:NSE", "BALKRISIND:BSE", 
        "BANDHANBNK:NSE", "BANDHANBNK:BSE", "BANKBARODA:BSE", "BANKBARODA:NSE", "BANKINDIA:BSE", 
        "BANKINDIA:NSE", "BDL:BSE", "BDL:NSE", "BEL:NSE", "BEL:BSE", "BHARATFORG:NSE", "BHARATFORG:BSE", 
        "BHARTIARTL:NSE", "BHARTIARTL:BSE", "BHARTIHEXA:NSE", "BHARTIHEXA:BSE", "BHEL:NSE", "BHEL:BSE", 
        "BIOCON:BSE", "BIOCON:NSE", "BOSCHLTD:BSE", "BOSCHLTD:NSE", "BPCL:BSE", "BPCL:NSE", "BRITANNIA:NSE", 
        "BRITANNIA:BSE", "BSE:NSE", "CANBK:NSE", "CANBK:BSE", "CGPOWER:BSE", "CGPOWER:NSE", "CHOLAFIN:NSE", 
        "CHOLAFIN:BSE", "CIPLA:BSE", "CIPLA:NSE", "COALINDIA:NSE", "COALINDIA:BSE", "COCHINSHIP:NSE", 
        "COCHINSHIP:BSE", "COFORGE:BSE", "COFORGE:NSE", "COLPAL:NSE", "COLPAL:BSE", "CONCOR:NSE", "CONCOR:BSE", 
        "CUMMINSIND:BSE", "CUMMINSIND:NSE", "DABUR:BSE", "DABUR:NSE", "DELHIVERY:BSE", "DELHIVERY:NSE", 
        "DIVISLAB:NSE", "DIVISLAB:BSE", "DIXON:NSE", "DIXON:BSE", "DLF:BSE", "DLF:NSE", "DMART:NSE", 
        "DMART:BSE", "DRREDDY:NSE", "DRREDDY:BSE", "EICHERMOT:BSE", "EICHERMOT:NSE", "ESCORTS:BSE", 
        "ESCORTS:NSE", "EXIDEIND:BSE", "EXIDEIND:NSE", "FACT:NSE", "FACT:BSE", "FEDERALBNK:NSE", 
        "FEDERALBNK:BSE", "GAIL:NSE", "GAIL:BSE", "GMRINFRA:BSE", "GMRINFRA:NSE", "GODREJCP:BSE", 
        "GODREJCP:NSE", "GODREJPROP:BSE", "GODREJPROP:NSE", "GRASIM:BSE", "GRASIM:NSE", "HAL:NSE", 
        "HAL:BSE", "HAVELLS:NSE", "HAVELLS:BSE", "HCLTECH:NSE", "HCLTECH:BSE", "HDFCAMC:BSE", 
        "HDFCAMC:NSE", "HDFCBANK:NSE", "HDFCBANK:BSE", "HDFCLIFE:BSE", "HDFCLIFE:NSE", "HEROMOTOCO:BSE", 
        "HEROMOTOCO:NSE", "HINDALCO:BSE", "HINDALCO:NSE", "HINDPETRO:NSE", "HINDPETRO:BSE", "HINDUNILVR:BSE", 
        "HINDUNILVR:NSE", "HINDZINC:BSE", "HINDZINC:NSE", "HUDCO:NSE", "HUDCO:BSE", "ICICIBANK:NSE", 
        "ICICIBANK:BSE", "ICICIGI:NSE", "ICICIGI:BSE", "ICICIPRULI:NSE", "ICICIPRULI:BSE", "IDBI:BSE", 
        "IDBI:NSE", "IDEA:BSE", "IDEA:NSE", "IDFCFIRSTB:NSE", "IDFCFIRSTB:BSE", "IGL:BSE", "IGL:NSE", 
        "INDHOTEL:BSE", "INDHOTEL:NSE", "INDIANB:BSE", "INDIANB:NSE", "INDIGO:BSE", "INDIGO:NSE", 
        "INDUSINDBK:NSE", "INDUSINDBK:BSE", "INDUSTOWER:NSE", "INDUSTOWER:BSE", "INFY:BSE", "INFY:NSE", 
        "IOB:NSE", "IOB:BSE", "IOC:BSE", "IOC:NSE", "IRB:NSE", "IRB:BSE", "IRCTC:NSE", "IRCTC:BSE", 
        "IREDA:BSE", "IREDA:NSE", "IRFC:BSE", "IRFC:NSE", "ITC:BSE", "ITC:NSE", "JINDALSTEL:BSE", 
        "JINDALSTEL:NSE", "JIOFIN:NSE", "JIOFIN:BSE", "JSWENERGY:BSE", "JSWENERGY:NSE", "JSWINFRA:NSE", 
        "JSWINFRA:BSE", "JSWSTEEL:BSE", "JSWSTEEL:NSE", "JUBLFOOD:BSE", "JUBLFOOD:NSE", "KALYANKJIL:NSE", 
        "KALYANKJIL:BSE", "KOTAKBANK:NSE", "KOTAKBANK:BSE", "KPITTECH:BSE", "KPITTECH:NSE", "LICHSGFIN:NSE", 
        "LICHSGFIN:BSE", "LICI:NSE", "LICI:BSE", "LODHA:NSE", "LODHA:BSE", "LT:BSE", "LT:NSE", "LTF:NSE", 
        "LTF:BSE", "LTIM:BSE", "LTIM:NSE", "LUPIN:NSE", "LUPIN:BSE", "MAHABANK:NSE", "MAHABANK:BSE", 
        "MANKIND:NSE", "MANKIND:BSE", "MARICO:NSE", "MARICO:BSE", "MARUTI:BSE", "MARUTI:NSE", 
        "MAXHEALTH:NSE", "MAXHEALTH:BSE", "MAZDOCK:BSE", "MAZDOCK:NSE", "MFSL:BSE", "MFSL:NSE", 
        "M&M:BSE", "M&M:NSE", "M&MFIN:NSE", "M&MFIN:BSE", "MOTHERSON:BSE", "MOTHERSON:NSE", "MPHASIS:NSE", 
        "MPHASIS:BSE", "MRF:NSE", "MRF:BSE", "MRPL:BSE", "MRPL:NSE", "MUTHOOTFIN:BSE", "MUTHOOTFIN:NSE", 
        "NAUKRI:BSE", "NAUKRI:NSE", "NESTLEIND:NSE", "NESTLEIND:BSE", "NHPC:BSE", "NHPC:NSE", 
        "NLCINDIA:BSE", "NLCINDIA:NSE",     "NMDC:NSE", "NMDC:BSE", "NTPC:BSE", "NTPC:NSE", "NYKAA:NSE", "NYKAA:BSE", 
        "OBEROIRLTY:BSE", "OBEROIRLTY:NSE", "OFSS:NSE", "OFSS:BSE", "OIL:BSE", 
        "OIL:NSE", "ONGC:NSE", "ONGC:BSE", "PAGEIND:NSE", "PAGEIND:BSE", 
        "PATANJALI:BSE", "PATANJALI:NSE", "PAYTM:BSE", "PAYTM:NSE", "PERSISTENT:NSE", 
        "PERSISTENT:BSE", "PETRONET:NSE", "PETRONET:BSE", "PFC:NSE", "PFC:BSE", 
        "PHOENIXLTD:NSE", "PHOENIXLTD:BSE", "PIDILITIND:NSE", "PIDILITIND:BSE", 
        "PIIND:BSE", "PIIND:NSE", "PNB:NSE", "PNB:BSE", "POLICYBZR:BSE", 
        "POLICYBZR:NSE", "POLYCAB:NSE", "POLYCAB:BSE", "POONAWALLA:NSE", 
        "POONAWALLA:BSE", "POWERGRID:BSE", "POWERGRID:NSE", "PRESTIGE:NSE", 
        "PRESTIGE:BSE", "RECLTD:NSE", "RECLTD:BSE", "RELIANCE:NSE", "RELIANCE:BSE", 
        "RVNL:BSE", "RVNL:NSE", "SAIL:NSE", "SAIL:BSE", "SBICARD:BSE", 
        "SBICARD:NSE", "SBILIFE:NSE", "SBILIFE:BSE", "SBIN:BSE", "SBIN:NSE", 
        "SHREECEM:BSE", "SHREECEM:NSE", "SHRIRAMFIN:BSE", "SHRIRAMFIN:NSE", 
        "SIEMENS:NSE", "SIEMENS:BSE", "SJVN:NSE", "SJVN:BSE", "SOLARINDS:BSE", 
        "SOLARINDS:NSE", "SONACOMS:BSE", "SONACOMS:NSE", "SRF:NSE", "SRF:BSE", 
        "SUNDARMFIN:BSE", "SUNDARMFIN:NSE", "SUNPHARMA:NSE", "SUNPHARMA:BSE", 
        "SUPREMEIND:NSE", "SUPREMEIND:BSE", "SUZLON:BSE", "SUZLON:NSE", 
        "TATACHEM:BSE", "TATACHEM:NSE", "TATACOMM:BSE", "TATACOMM:NSE", 
        "TATACONSUM:BSE", "TATACONSUM:NSE", "TATAELXSI:NSE", "TATAELXSI:BSE", 
        "TATAMOTORS:NSE", "TATAMOTORS:BSE", "TATAPOWER:BSE", "TATAPOWER:NSE", 
        "TATASTEEL:NSE", "TATASTEEL:BSE", "TATATECH:BSE", "TATATECH:NSE", 
        "TCS:NSE", "TCS:BSE", "TECHM:NSE", "TECHM:BSE", "TIINDIA:BSE", 
        "TIINDIA:NSE", "TITAN:NSE", "TITAN:BSE", "TORNTPHARM:NSE", 
        "TORNTPHARM:BSE", "TORNTPOWER:NSE", "TORNTPOWER:BSE", "TRENT:NSE", 
        "TRENT:BSE", "TVSMOTOR:NSE", "TVSMOTOR:BSE", "ULTRACEMCO:NSE", 
        "ULTRACEMCO:BSE", "UNIONBANK:BSE", "UNIONBANK:NSE", "UNITDSPR:NSE", 
        "UNITDSPR:BSE", "UPL:BSE", "UPL:NSE", "VBL:BSE", "VBL:NSE", 
        "VEDL:BSE", "VEDL:NSE", "VOLTAS:BSE", "VOLTAS:NSE", "WIPRO:BSE", 
        "WIPRO:NSE", "YESBANK:NSE", "YESBANK:BSE", "ZOMATO:BSE", 
        "ZOMATO:NSE", "ZYDUSLIFE:NSE", "ZYDUSLIFE:BSE"
    ]

    # Subscribe to the symbols along with ETH/BTC



    # Subscribe to additional symbols
    ws.subscribe(['ETH/BTC'] + symbols)
    # ws.subscribe(['ETH/BTC', 'AAPL', 'GOOGL', 'RELIANCE.NS', 'TATAMOTORS.NS', 'HDFCBANK.NS'])

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
