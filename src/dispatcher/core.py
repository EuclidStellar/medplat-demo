import time
import json
import os
from src.utils.logging import logger

class Dispatcher:
    def __init__(self, schema_registry, output_dir='output'):
        self.schema_registry = schema_registry
        self.output_dir = output_dir
        self.consumers = []
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def register_consumer(self, consumer):
        """Register a consumer to receive processed data."""
        self.consumers.append(consumer)
        
    def receive_data(self, data, source_name, schema_id):
        """Process incoming data from an adapter."""
        logger.info(f"Received data from {source_name}")
        
        # Validate data against schema
        is_valid, error = self.schema_registry.validate_data(data, schema_id)
        
        if not is_valid:
            logger.error(f"Validation error for data from {source_name}: {error}")
            self._write_to_rejected(data, source_name, error)
            return False
            
        # Process and route valid data
        return self.route_data(data, source_name)
        
    def route_data(self, data, source_name):
        """Route validated data to registered consumers."""
        logger.info(f"Routing data from {source_name} to {len(self.consumers)} consumers")
        
        # Default behavior: write to file if no consumers
        if not self.consumers:
            self._write_to_file(data, source_name)
            return True
            
        # Send to all registered consumers
        for consumer in self.consumers:
            try:
                consumer.process(data)
            except Exception as e:
                logger.error(f"Error in consumer {consumer.__class__.__name__}: {str(e)}")
                
        return True
        
    def _write_to_file(self, data, source_name):
        """Write data to JSON file."""
        timestamp = int(time.time())
        filename = f"{self.output_dir}/{source_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Data written to {filename}")
        
    def _write_to_rejected(self, data, source_name, error):
        """Write rejected data to a separate file."""
        timestamp = int(time.time())
        filename = f"{self.output_dir}/rejected_{source_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'data': data,
                'error': error,
                'timestamp': timestamp
            }, f, indent=2)
            
        logger.info(f"Rejected data written to {filename}")