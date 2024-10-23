from fastapi import APIRouter
from services.stock_profile_service import get_stock_profile

# Create an API router
router = APIRouter()

# Define a route to fetch the stock profile
@router.get("/profile/{symbol}")
def fetch_stock_profile(symbol: str):
    profile = get_stock_profile(symbol)
    return profile
