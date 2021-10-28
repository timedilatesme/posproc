from copy import deepcopy
from posproc import*
constants.DATA_STORAGE = 'data/'
# from testing_data import alice_key

file_name = '17072021_Alice_2.txt'

# > lab_data/results/14072021_1.txt
with open('lab_data/' + file_name) as fh:
    alice_key_f = Key( key_as_str= fh.read())
    # print(alice_key_f._size)
    
# alice_key_org = deepcopy(alice_key)

# with open('results/alice_key.txt', 'w') as f:
#     f.write(str(alice_key))

# Create the server
alice = QKDServer('Alice', current_key=alice_key_f)

# print(alice_key)

alice.Initialize_Events()

# Start the server socket
alice.start_ursina_server()

# Important calls for event based networking
alice.start_events_processing_thread()

@alice.event
def when_client_qkd_completes(Client,Content):
    with open('lab_data/final_key/' + file_name, 'w') as f:
        f.write(str(alice._current_key))

# Initialize all the protocols for authentication, error correction, privacy amplification.

# print('Alice Key: ', alice._current_key)

# alice.stopServer()
