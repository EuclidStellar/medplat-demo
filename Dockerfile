FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY src/ ./src/

# Copy the schemas
COPY schemas/ ./schemas/

# Copy the docker-compose file (if needed for reference)
COPY docker-compose.yml .

# Set the command to run the application
CMD ["python", "src/main.py"]