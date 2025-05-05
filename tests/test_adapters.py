import unittest
from src.adapters.batch.api_adapter import ApiAdapter
from src.adapters.batch.ftp_adapter import FtpAdapter
from src.adapters.streaming.kafka_adapter import KafkaAdapter

class TestAdapters(unittest.TestCase):

    def setUp(self):
        self.api_adapter = ApiAdapter()
        self.ftp_adapter = FtpAdapter()
        self.kafka_adapter = KafkaAdapter()

    def test_api_adapter_initialization(self):
        self.assertIsInstance(self.api_adapter, ApiAdapter)

    def test_ftp_adapter_initialization(self):
        self.assertIsInstance(self.ftp_adapter, FtpAdapter)

    def test_kafka_adapter_initialization(self):
        self.assertIsInstance(self.kafka_adapter, KafkaAdapter)

    def test_api_adapter_fetch_data(self):
        # Assuming fetch_data method exists and returns a list of data
        data = self.api_adapter.fetch_data()
        self.assertIsInstance(data, list)

    def test_ftp_adapter_download_file(self):
        # Assuming download_file method exists and returns a boolean
        result = self.ftp_adapter.download_file('test_file.txt')
        self.assertTrue(result)

    def test_kafka_adapter_consume_messages(self):
        # Assuming consume_messages method exists and returns a list of messages
        messages = self.kafka_adapter.consume_messages()
        self.assertIsInstance(messages, list)

if __name__ == '__main__':
    unittest.main()