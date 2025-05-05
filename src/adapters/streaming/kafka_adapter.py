import json
import threading
from src.adapters.base import IngestionAdapter
from src.utils.logging import logger

# Mock Kafka consumer class for demonstration
class MockKafkaConsumer:
    def __init__(self, topic):
        self.topic = topic
        self.running = True
        
    def consume(self, callback):
        """Simulate consuming messages."""
        import time
        import random
        
        # Sample location data generation
        while self.running:
            # Generate mock vehicle location data
            data = {
                "vehicle_id": f"VEH-{random.randint(1000, 9999)}",
                "lat": random.uniform(37.7, 38.2),
                "lng": random.uniform(-122.5, -122.1),
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }
            
            callback(data)
            time.sleep(random.uniform(0.5, 2.0))  # Random delay between messages
            
    def close(self):
        """Stop consuming messages."""
        self.running = False

class KafkaAdapter(IngestionAdapter):
    def __init__(self, dispatcher, topic="vehicle_locations", schema_id="location_v1"):
        super().__init__("kafka", dispatcher)
        self.topic = topic
        self.schema_id = schema_id
        self.consumer = None
        self.consumer_thread = None
        
    def connect(self):
        """Connect to Kafka."""
        logger.info(f"Connecting to Kafka topic: {self.topic}")
        self.consumer = MockKafkaConsumer(self.topic)
        
    def ingest(self):
        """Start ingesting data from Kafka."""
        logger.info("Starting Kafka ingestion")
        
        if not self.consumer:
            self.connect()
            
        def consume_messages():
            """Consumer thread function."""
            self.consumer.consume(self._process_message)
            
        self.consumer_thread = threading.Thread(target=consume_messages)
        self.consumer_thread.daemon = True
        self.consumer_thread.start()
        
    def _process_message(self, message):
        """Process an incoming Kafka message."""
        try:
            # Send the message to the dispatcher
            self.dispatcher.receive_data(message, self.name, self.schema_id)
        except Exception as e:
            logger.error(f"Error processing Kafka message: {str(e)}")
        
    def close(self):
        """Close the Kafka consumer."""
        if self.consumer:
            self.consumer.close()