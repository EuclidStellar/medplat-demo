# Unified Data Ingestion System

## Overview

The Unified Data Ingestion System is designed to handle both streaming and batch data ingestion with a modular architecture. It centralizes data flow through a dispatcher and validates incoming data against versioned schemas.

## Features

- **Streaming Data Ingestion**: Supports real-time data ingestion from Kafka.
- **Batch Data Ingestion**: Handles data from REST APIs and FTP servers.
- **Centralized Dispatcher**: Routes and validates data before sending it to the output layer.
- **Schema Management**: Utilizes a schema registry for versioned schema validation.

## Project Structure

```
unified-data-ingestion-system
├── src
│   ├── adapters          # Contains ingestion adapters
│   ├── dispatcher        # Centralized dispatcher logic
│   ├── schema_registry   # Manages schema versions
│   ├── config            # Configuration settings
│   ├── utils             # Utility functions
│   └── main.py           # Entry point of the application
├── tests                 # Unit tests for the application
├── schemas               # JSON schemas for validation
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker image build instructions
└── requirements.txt      # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.x
- Docker (for containerization)
- Kafka or another message queue service

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd unified-data-ingestion-system
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the Docker containers:
   ```
   docker-compose up -d
   ```

### Usage

1. Start the application:
   ```
   python src/main.py
   ```

2. Configure your data sources in the `src/config/settings.py` file.

3. Monitor the logs for ingestion events and errors.

## Testing

Run the unit tests to ensure everything is functioning correctly:
```
pytest tests/
```

## Future Enhancements

- Web UI for monitoring and managing data ingestion.
- Support for additional data sources and formats.
- Enhanced logging and error handling mechanisms.

## License

This project is licensed under the MIT License. See the LICENSE file for details.