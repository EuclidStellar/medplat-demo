import os
import time
import signal
import sys
from src.schema_registry.registry import SchemaRegistry
from src.dispatcher.core import Dispatcher
from src.adapters.streaming.kafka_adapter import KafkaAdapter
from src.adapters.batch.api_adapter import ApiAdapter
from src.adapters.batch.csv_adapter import CsvAdapter
from src.utils.logging import logger

# Global flag for clean shutdown
running = True

def signal_handler(sig, frame):
    """Handle termination signals."""
    global running
    logger.info("Shutting down gracefully...")
    running = False
    
def main():
    """Main entry point of the application."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.info("Starting Unified Data Ingestion System...")
    
    # Create necessary directories
    for directory in ['output', 'input', 'logs', 'schemas']:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # Initialize schema registry
    schema_registry = SchemaRegistry(schema_dir='schemas')
    
    # Add default schema if missing
    location_schema = {
        "schema_id": "location_v1",
        "version": 1,
        "type": "json",
        "schema": {
            "type": "object",
            "properties": {
                "vehicle_id": {"type": "string"},
                "lat": {"type": "number"},
                "lng": {"type": "number"},
                "timestamp": {"type": "string"}
            },
            "required": ["vehicle_id", "lat", "lng", "timestamp"]
        }
    }
    
    try:
        schema_registry.register_schema("location_v1", location_schema)
    except ValueError:
        # Schema already exists, which is fine
        pass
    
    # Initialize dispatcher
    dispatcher = Dispatcher(schema_registry, output_dir='output')
    
    # Initialize adapters
    kafka_adapter = KafkaAdapter(dispatcher)
    api_adapter = ApiAdapter(dispatcher, interval=30)  # Fetch from API every 30 seconds
    csv_adapter = CsvAdapter(dispatcher)
    
    # Start adapters
    try:
        # Start streaming adapter
        kafka_adapter.ingest()
        logger.info("Kafka adapter started")
        
        # Start API adapter
        api_adapter.ingest()
        logger.info("API adapter started")
        
        # Process CSV files immediately
        csv_adapter.ingest()
        logger.info("CSV processing complete")
        
        # Keep the main thread running
        while running:
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Error in main loop: {str(e)}")
    
    finally:
        # Cleanup
        kafka_adapter.close()
        api_adapter.close()
        csv_adapter.close()
        logger.info("All adapters closed")
        
if __name__ == "__main__":
    main()