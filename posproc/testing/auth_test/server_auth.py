# python -m posproc.testing.auth_test.server_auth

from posproc.networking.user_data import UserData
from posproc.networking.server import Server
from posproc.testing.auth_test.testing_data import alice_key

# user_data = UserData()

def run():
    s = Server('Alice', alice_key, user_data=user_data)

if __name__ == "__main__":
    run()
