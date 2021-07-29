from posproc.networking.client import Client
from posproc.testing.newTests.testing_data import bob_key
import pickle

# python -m posproc.testing.newTests.client

client = Client('Bob', bob_key)
client.start_ursina_client()
client.start_sending_messages_thread()
client.start_events_processing_thread()
client.Initialize_Events()

# client.stopClient()