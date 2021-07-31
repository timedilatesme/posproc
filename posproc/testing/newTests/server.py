from posproc.networking.server import Server
from posproc.testing.newTests.testing_data import alice_key
import pickle

# python -m posproc.testing.newTests.server

server = Server("Alice", alice_key)

server.start_ursina_server()
server.start_sending_messages_thread()
server.start_events_processing_thread()
server.Initialize_Events()

# print(alice_key)