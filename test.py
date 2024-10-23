from dotenv import load_dotenv
import time
import asyncio
from twelvedata import TDClient
from supabase import create_client
import os
import json
from collections import deque
from concurrent.futures import ThreadPoolExecutor
import logging
from websocket import WebSocketApp

# Load environment variables
load_dotenv()

# API configurations
TWELVE_DATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Buffer for batch processing
BATCH_SIZE = 50
BATCH_TIMEOUT = 1.0  # seconds
price_buffer = deque(maxlen=BATCH_SIZE)

class AsyncWebSocketClient:
    def __init__(self, symbols, price_handler):
        self.symbols = symbols
        self.price_handler = price_handler
        self.td = TDClient(apikey=TWELVE_DATA_API_KEY)
        self.ws = None
        self.is_connected = False
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        def on_message(ws, message):
            data = json.loads(message)
            asyncio.run_coroutine_threadsafe(
                self.price_handler.process_event(data),
                self.loop
            )

        def on_error(ws, error):
            logger.error(f"WebSocket error: {error}")

        def on_close(ws, close_status_code, close_msg):
            logger.info("WebSocket connection closed")
            self.is_connected = False

        def on_open(ws):
            logger.info("WebSocket connection opened")
            self.is_connected = True
            # Subscribe to all symbols after initial symbol
            if len(self.symbols) > 1:
                ws.send(json.dumps({
                    "action": "subscribe",
                    "params": {
                        "symbols": ",".join(self.symbols[1:])
                    }
                }))

        # Create WebSocket connection
        ws_url = f"wss://ws.twelvedata.com/v1/quotes/price?apikey={TWELVE_DATA_API_KEY}"
        self.ws = WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )

        # Run WebSocket in a separate thread
        self.ws_thread = threading.Thread(
            target=self.ws.run_forever,
            kwargs={'ping_interval': 30}
        )
        self.ws_thread.daemon = True
        self.ws_thread.start()

    def close(self):
        if self.ws:
            self.ws.close()

class PriceUpdateHandler:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.batch_lock = asyncio.Lock()
        self.last_batch_time = time.time()
        self.processed_count = 0
        
    async def process_event(self, event):
        try:
            if isinstance(event, dict) and event.get('event') == 'price':
                price_buffer.append(event)
                self.processed_count += 1
                
                # Process batch if buffer is full or timeout reached
                if (len(price_buffer) >= BATCH_SIZE or 
                    time.time() - self.last_batch_time >= BATCH_TIMEOUT):
                    await self.process_batch()
                    
                # Log processing stats periodically
                if self.processed_count % 100 == 0:
                    logger.info(f"Processed {self.processed_count} price updates")
                    
        except Exception as e:
            logger.error(f"Error processing event: {e}")

    async def process_batch(self):
        async with self.batch_lock:
            if not price_buffer:
                return

            batch = list(price_buffer)
            price_buffer.clear()
            self.last_batch_time = time.time()

            # Process batch in thread pool
            await asyncio.get_event_loop().run_in_executor(
                self.executor, 
                self.store_batch,
                batch
            )

    def store_batch(self, batch):
        try:
            # Prepare batch data

            price_data_batch = [
                {
                    'symbol': data.get('symbol'),
                    'price': float(data.get('price', 0)),
                    'type': data.get('type'),
                    'event': data.get('event'),
                    'mic_code': data.get('mic_code'),
                    'day_volume': data.get('day_volume'),
                    'updated_at': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                for data in batch
            ]

            print("price_data_batch === check=============", price_data_batch)
            
            # Batch insert to Supabase
            response = supabase.table('price').insert(price_data_batch).execute()
            
            logger.info(f"Stored batch of {len(batch)} price updates")
            
        except Exception as e:
            logger.error(f"Error storing batch data: {e}")

async def fetch_symbols_from_db():
    try:
        response = supabase.table('stocks').select('symbol, exchange').execute()
        
        if response.data:
            symbols = [
                f"{stock['symbol']}:{stock['exchange']}"
                for stock in response.data
                if stock['exchange'] in ['NSE', 'BSE']
            ]
            
            logger.info(f"Fetched {len(symbols)} symbols from database")
            return symbols
            
        logger.warning("No symbols found in database")
        return []
            
    except Exception as e:
        logger.error(f"Error fetching symbols: {e}")
        return []

async def main():
    try:
        # Initialize handlers
        price_handler = PriceUpdateHandler()
        
        # Fetch symbols
        symbols = await fetch_symbols_from_db()
        if not symbols:
            logger.error("No symbols to subscribe to.")
            return
            
        # Initialize WebSocket client
        ws_client = AsyncWebSocketClient(symbols, price_handler)
        await ws_client.connect()
        
        # Keep the main task running and monitor connection
        while True:
            if not ws_client.is_connected:
                logger.warning("WebSocket disconnected. Attempting to reconnect...")
                await ws_client.connect()
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
        if 'ws_client' in locals():
            ws_client.close()
    except Exception as e:
        logger.error(f"Error in main: {e}")

if __name__ == "__main__":
    import threading
    asyncio.run(main())







