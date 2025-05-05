import unittest
from src.dispatcher.core import Dispatcher

class TestDispatcher(unittest.TestCase):

    def setUp(self):
        self.dispatcher = Dispatcher()

    def test_receive_data(self):
        test_data = {"vehicle_id": "123", "lat": 40.7128, "lng": -74.0060, "timestamp": "2023-10-01T12:00:00Z"}
        result = self.dispatcher.receive_data(test_data)
        self.assertTrue(result)

    def test_validate_data(self):
        valid_data = {"vehicle_id": "123", "lat": 40.7128, "lng": -74.0060, "timestamp": "2023-10-01T12:00:00Z"}
        invalid_data = {"vehicle_id": "123", "lat": "not_a_number", "lng": -74.0060, "timestamp": "2023-10-01T12:00:00Z"}
        
        self.assertTrue(self.dispatcher.validate_data(valid_data))
        self.assertFalse(self.dispatcher.validate_data(invalid_data))

    def test_route_data(self):
        test_data = {"vehicle_id": "123", "lat": 40.7128, "lng": -74.0060, "timestamp": "2023-10-01T12:00:00Z"}
        output = self.dispatcher.route_data(test_data)
        self.assertIn('output_destination', output)

if __name__ == '__main__':
    unittest.main()