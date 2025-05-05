import unittest
from src.schema_registry.registry import SchemaRegistry
from src.schema_registry.validators import validate_schema

class TestSchemaRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = SchemaRegistry()
        self.schema = {
            "schema_id": "location_v1",
            "version": 1,
            "type": "json",
            "schema": {
                "type": "object",
                "properties": {
                    "vehicle_id": {"type": "string"},
                    "lat": {"type": "number"},
                    "lng": {"type": "number"},
                    "timestamp": {"type": "string", "format": "date-time"}
                },
                "required": ["vehicle_id", "lat", "lng", "timestamp"]
            }
        }
        self.registry.register_schema(self.schema)

    def test_register_schema(self):
        self.assertIn("location_v1", self.registry.schemas)
        self.assertEqual(len(self.registry.schemas["location_v1"]), 1)

    def test_validate_schema_success(self):
        valid_data = {
            "vehicle_id": "123ABC",
            "lat": 37.7749,
            "lng": -122.4194,
            "timestamp": "2023-10-01T12:00:00Z"
        }
        result = validate_schema(valid_data, self.schema)
        self.assertTrue(result)

    def test_validate_schema_failure(self):
        invalid_data = {
            "vehicle_id": "123ABC",
            "lat": "not_a_number",
            "lng": -122.4194,
            "timestamp": "2023-10-01T12:00:00Z"
        }
        result = validate_schema(invalid_data, self.schema)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()