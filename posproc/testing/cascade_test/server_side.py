# python -m posproc.testing.cascade_test.server_side


from posproc import constants
from posproc.networking.server import Server
from posproc.testing.cascade_test.testing_data import alice_key, user_data
from posproc.networking.user_data import User

def run():
    # print(f'Alice\'s Key: {alice_key}')    
    alice = Server('Alice',alice_key) # This will loop over and over # TODO: Find a way to stop the server!
        

if __name__ == "__main__":
    run()
