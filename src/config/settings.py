# Configuration settings for the Unified Data Ingestion System

MESSAGE_QUEUE = {
    'type': 'Kafka',  # Options: 'Kafka', 'RabbitMQ', 'Pulsar'
    'bootstrap_servers': 'localhost:9092',  # Change as needed
    'topic': 'data_ingestion'
}

SCHEMA_REGISTRY = {
    'url': 'http://localhost:8081',  # Change as needed
    'default_schema': 'location_v1'
}

BATCH_SETTINGS = {
    'api': {
        'base_url': 'https://api.example.com/data',  # Change as needed
        'timeout': 30  # seconds
    },
    'ftp': {
        'host': 'ftp.example.com',  # Change as needed
        'username': 'user',  # Change as needed
        'password': 'pass',  # Change as needed
        'directory': '/data'  # Change as needed
    }
}

LOGGING = {
    'level': 'INFO',  # Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    'log_file': 'ingestion.log'  # Change as needed
}