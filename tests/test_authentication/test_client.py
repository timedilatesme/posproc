import unittest
from posproc import *
from testing_data import bob_key

# python -m test_client

class TestClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bob = QKDClient('Bob', bob_key)
    
    @classmethod
    def tearDownClass(cls) -> None:
        time.sleep(0.25)
        cls.bob.stopClient()
    
    def test_connect(self):
        self.bob.start_ursina_client()
    
    def test_startThreads(self):    
        self.bob.start_sending_messages_thread()
        self.bob.start_events_processing_thread()
    
    def test_initialize_events(self):
        self.bob.Initialize_Events()

if __name__ == '__main__':
    unittest.main()
