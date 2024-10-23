from fastapi import APIRouter
from services.search_stock import search_stock_profile

# Create an API router
router = APIRouter()

# Define a route to fetch the stock profile
@router.get("/search/{keyword}")
def search_stock(keyword: str):
    profile = search_stock_profile(keyword)
    return profile
