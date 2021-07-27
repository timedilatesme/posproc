from posproc.networking.server import Server
from posproc.testing.newTests.testing_data import alice_key
import pickle

# python -m posproc.testing.newTests.server

s = Server("Alice", alice_key)

@s.event
def requestUserObjectFromClient(Client, Content):
    Client.send_message("userObject", "")
    clientUserObject = pickle.loads(Content)
    print("User Object: ", clientUserObject)

while True:
    s.process_net_events()