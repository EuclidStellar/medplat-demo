import csv
import os
import time
from src.adapters.base import IngestionAdapter
from src.utils.logging import logger

class CsvAdapter(IngestionAdapter):
    def __init__(self, dispatcher, input_dir="input", schema_id="location_v1"):
        super().__init__("csv", dispatcher)
        self.input_dir = input_dir
        self.schema_id = schema_id
        
        # Create input directory if it doesn't exist
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
            
        # Create a sample CSV file for demo purposes
        self._create_sample_csv()
        
    def connect(self):
        """No connection needed for CSV adapter."""
        pass
        
    def ingest(self):
        """Process all CSV files in the input directory."""
        logger.info(f"Processing CSV files in {self.input_dir}")
        
        if not os.path.exists(self.input_dir):
            logger.warning(f"Input directory {self.input_dir} does not exist.")
            return
            
        # Process each CSV file
        for filename in os.listdir(self.input_dir):
            if filename.endswith('.csv'):
                self._process_file(os.path.join(self.input_dir, filename))
                
    def _process_file(self, filepath):
        """Process a single CSV file."""
        logger.info(f"Processing file: {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert numeric values (assuming lat/lng are numeric)
                    if 'lat' in row:
                        row['lat'] = float(row['lat'])
                    if 'lng' in row:
                        row['lng'] = float(row['lng'])
                        
                    # Send to dispatcher
                    self.dispatcher.receive_data(row, self.name, self.schema_id)
                    
            # Move processed file to a 'processed' subdirectory
            processed_dir = os.path.join(self.input_dir, 'processed')
            if not os.path.exists(processed_dir):
                os.makedirs(processed_dir)
                
            processed_path = os.path.join(processed_dir, os.path.basename(filepath))
            os.rename(filepath, processed_path)
            logger.info(f"Moved processed file to {processed_path}")
            
        except Exception as e:
            logger.error(f"Error processing file {filepath}: {str(e)}")
            
    def close(self):
        """Nothing to close for CSV adapter."""
        pass
        
    def _create_sample_csv(self):
        """Create a sample CSV file for demonstration."""
        sample_path = os.path.join(self.input_dir, "sample_locations.csv")
        
        if os.path.exists(sample_path):
            return  # Don't overwrite existing file
            
        try:
            with open(sample_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['vehicle_id', 'lat', 'lng', 'timestamp'])
                writer.writerow(['VEH-1001', '37.7749', '-122.4194', '2023-10-01T08:00:00Z'])
                writer.writerow(['VEH-1002', '37.3382', '-121.8863', '2023-10-01T08:05:00Z'])
                writer.writerow(['VEH-1003', '37.4275', '-122.1697', '2023-10-01T08:10:00Z'])
                
            logger.info(f"Created sample CSV file: {sample_path}")
        except Exception as e:
            logger.error(f"Error creating sample CSV: {str(e)}")