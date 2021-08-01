from posproc import*
constants.DATA_STORAGE = 'data/'
from testing_data import alice_key


# Create the server
alice = QKDServer('Alice', current_key=alice_key)

# Start the server socket
alice.start_ursina_server()

# Important calls for event based networking
alice.start_sending_messages_thread()
alice.start_events_processing_thread()

# Initialize all the protocols for authentication, error correction, privacy amplification.
alice.Initialize_Events()

# print('Alice Key: ', alice._current_key)

# alice.stopServer()
