import json
import threading
import time
import random
from src.adapters.base import IngestionAdapter
from src.utils.logging import logger

class ApiAdapter(IngestionAdapter):
    def __init__(self, dispatcher, api_url=None, interval=60, schema_id="location_v1"):
        super().__init__("api", dispatcher)
        self.api_url = api_url or "https://mock-api/vehicle-locations"
        self.interval = interval  # Seconds between API calls
        self.schema_id = schema_id
        self.running = False
        self.timer_thread = None
        
    def connect(self):
        """Initialize API connection (no actual connection needed for mock)."""
        logger.info(f"Initializing API adapter for URL: {self.api_url}")
        
    def ingest(self):
        """Start periodic ingestion from the API."""
        self.running = True
        
        def fetch_periodically():
            """Periodically fetch data from the API."""
            while self.running:
                try:
                    data = self._fetch_data()
                    if data:
                        # Send each record to the dispatcher
                        for record in data:
                            self.dispatcher.receive_data(record, self.name, self.schema_id)
                except Exception as e:
                    logger.error(f"Error in API fetch: {str(e)}")
                
                time.sleep(self.interval)
                
        self.timer_thread = threading.Thread(target=fetch_periodically)
        self.timer_thread.daemon = True
        self.timer_thread.start()
        
    def _fetch_data(self):
        """Mock API data fetch."""
        logger.info(f"Fetching data from API: {self.api_url}")
        
        # In a real implementation, this would make an HTTP request
        # For demo, generate mock data
        data = []
        
        # Generate 5-10 random vehicle locations
        for _ in range(random.randint(5, 10)):
            record = {
                "vehicle_id": f"VEH-{random.randint(1000, 9999)}",
                "lat": random.uniform(37.7, 38.2),
                "lng": random.uniform(-122.5, -122.1),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            data.append(record)
            
        return data
        
    def close(self):
        """Stop the periodic ingestion."""
        self.running = False
        if self.timer_thread:
            self.timer_thread.join(timeout=1)