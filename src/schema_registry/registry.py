import json
import os
from jsonschema import validate, ValidationError

class SchemaRegistry:
    def __init__(self, schema_dir='schemas'):
        self.schemas = {}
        self.schema_dir = schema_dir
        self._load_schemas()
        
    def _load_schemas(self):
        """Load schemas from the schema directory."""
        if not os.path.exists(self.schema_dir):
            return
            
        for filename in os.listdir(self.schema_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.schema_dir, filename)
                with open(filepath, 'r') as f:
                    schema_data = json.load(f)
                    schema_id = schema_data.get('schema_id')
                    if schema_id:
                        self.schemas[schema_id] = schema_data
    
    def register_schema(self, schema_id, schema):
        """Register a new schema."""
        if schema_id in self.schemas:
            raise ValueError(f"Schema with ID {schema_id} already exists.")
        self.schemas[schema_id] = schema
        
    def get_schema(self, schema_id):
        """Get a schema by ID."""
        return self.schemas.get(schema_id)
        
    def validate_data(self, data, schema_id):
        """Validate data against a schema."""
        schema = self.get_schema(schema_id)
        if not schema:
            raise ValueError(f"Schema {schema_id} not found.")
            
        try:
            validate(instance=data, schema=schema.get('schema', {}))
            return True, None
        except ValidationError as e:
            return False, str(e)
            
    def list_schemas(self):
        """List all available schemas."""
        return list(self.schemas.keys())