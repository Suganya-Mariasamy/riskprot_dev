# stock_service.py

import os
from dotenv import load_dotenv
from twelvedata import TDClient

load_dotenv()
api_key = os.getenv("TWELVE_DATA_API_KEY")

# Initialize the Twelve Data client
td = TDClient(apikey='eb060f32957c4d1088593fe3a7ecd4ce')

def get_stock_profile(symbol: str):
    """
    Fetch the profile of a stock given its symbol.
    """
    try:
        profile = td.get_profile(symbol=symbol).as_json()
        return profile
    except Exception as e:
        return {"error": str(e)}