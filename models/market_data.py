# /models/market_data.py
from pydantic import BaseModel

class MarketData(BaseModel):
    id: int
    symbol: str
    price: float
    timestamp: str  # or you can use `datetime` type if you're using datetime
