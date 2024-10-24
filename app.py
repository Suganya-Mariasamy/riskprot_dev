from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.stock_profile_api import router as stock_profile_router  # Import the router

from api.search_stock import router as search_stock

# Initialize the FastAPI app
app = FastAPI()

origins = [
    "http://localhost:3000",  # Your local development URL
    "https://riskprotec.vercel.app",  # Your deployed backend URL
    "https://riskprotec-suganya-mariasamy-riskprotec.vercel.app"
]

# Add CORS middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specified origins
    allow_credentials=False,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Include the stock API router
app.include_router(stock_profile_router)
app.include_router(search_stock)

# Optional: Root path
@app.get("/")
def read_root():
    return {"message": "Welcome to the Stock Profile API!"}


