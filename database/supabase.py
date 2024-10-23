# /database/supabase.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Supabase configuration
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Create a Supabase client
supabase: Client = create_client(url, key)

def get_supabase_client():
    return supabase
