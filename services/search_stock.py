# stock_service.py
import requests
import os
from dotenv import load_dotenv
from twelvedata import TDClient

load_dotenv()
api_key = os.getenv("TWELVE_DATA_API_KEY")

# Initialize the Twelve Data client
td = TDClient(apikey='eb060f32957c4d1088593fe3a7ecd4ce')

def search_stock_profile(searchQuery: str):
    url = f"https://api.twelvedata.com/symbol_search?symbol={searchQuery}&apikey=${api_key}"
    
    try:
        # Make a GET request to the Twelve Data API
        response = requests.get(url)
        response_data = response.json()  # Parse the JSON response
        
        # Check if the request was successful
        if response.status_code == 200:
            return response_data  # Return the parsed data
        else:
            return {"error": response_data.get("message", "An error occurred.")}
    except Exception as e:
        return {"error": str(e)}
