from fastapi import FastAPI
from api.stock_profile_api import router as stock_profile_router  # Import the router

from api.search_stock import router as search_stock

# Initialize the FastAPI app
app = FastAPI()

# Include the stock API router
app.include_router(stock_profile_router)
app.include_router(search_stock)

# Optional: Root path
@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Profile API!"}
