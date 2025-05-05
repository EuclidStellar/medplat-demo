class IngestionAdapter:
    """Base class for all ingestion adapters."""
    
    def __init__(self, name, dispatcher):
        self.name = name
        self.dispatcher = dispatcher
        
    def connect(self):
        """Establish connection to the data source."""
        raise NotImplementedError("Connect method must be implemented by subclasses.")

    def ingest(self):
        """Ingest data from the source."""
        raise NotImplementedError("Ingest method must be implemented by subclasses.")

    def close(self):
        """Close any active connections."""
        raise NotImplementedError("Close method must be implemented by subclasses.")