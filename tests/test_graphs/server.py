from posproc import *
constants.DATA_STORAGE = 'data/'
from testing_data import key_pairs_to_use

# python server.py

alice = QKDServer('Alice', key_pairs_to_use[0][0])
alice.Initialize_Events()
alice.start_ursina_server()
alice.start_events_processing_thread()

@alice.event
def completed(Client, Content):
    print('Alice :', Content)
    next_index = Content + 1
    alice._current_key = key_pairs_to_use[next_index][0]