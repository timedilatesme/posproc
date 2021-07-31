from posproc import *
from testing_data import alice_key

alice = QKDServer('Alice', alice_key)

alice.start_ursina_server()
alice.start_sending_messages_thread()
alice.start_events_processing_thread()
alice.Initialize_Events()