from posproc.networking.client import Client
from posproc.testing.newTests.testing_data import bob_key
import pickle

# python -m posproc.testing.newTests.client

c = Client("Bob", bob_key)

@c.event
def userObject(Content):
    msg_to_send = pickle.dumps(c.user)
    c.send_message("requestUserObjectFromClient",msg_to_send)

while True:
    c.process_net_events()