from copy import deepcopy
from posproc import*
constants.DATA_STORAGE = 'data/'
# from testing_data import alice_key

with open('Alice.txt') as fh:
    alice_key = Key( key_as_str= fh.read())
    
# alice_key_org = deepcopy(alice_key)

# with open('results/alice_key.txt', 'w') as f:
#     f.write(str(alice_key))


# Create the server
alice = QKDServer('Alice', current_key=alice_key)

# print(alice_key)

alice.Initialize_Events()

# Start the server socket
alice.start_ursina_server()

# Important calls for event based networking
alice.start_events_processing_thread()



# @alice.event
# def onClientDisconnected(Client):
#     alice._current_key = alice_key
#     # alice.stopServer()

# Initialize all the protocols for authentication, error correction, privacy amplification.

# print('Alice Key: ', alice._current_key)

# alice.stopServer()