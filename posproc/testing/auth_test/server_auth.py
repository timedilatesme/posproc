# python -m posproc.testing.auth_test.server_auth

from posproc.networking.server import Server
from posproc.testing.auth_test.testing_data import alice_key

def run():
    s = Server('Alice',alice_key)

if __name__ == "__main__":
    run()
