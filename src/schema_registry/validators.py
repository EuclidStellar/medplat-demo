from jsonschema import validate, ValidationError

def validate_schema(data, schema):
    """Validate data against a schema."""
    try:
        # Extract the actual schema part if it's a registry entry
        if isinstance(schema, dict) and 'schema' in schema:
            schema = schema['schema']
        
        validate(instance=data, schema=schema)
        return True, None
    except ValidationError as e:
        return False, str(e)

def validate_location_schema(data):
    from ..schemas.location_v1 import schema as location_schema
    return validate_schema(data, location_schema)