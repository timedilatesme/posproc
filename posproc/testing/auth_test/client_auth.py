# python -m posproc.testing.auth_test.client_auth


from posproc.networking.client import Client
from posproc.testing.auth_test.testing_data import bob_key, user_data


def run():
    c = Client('Alice', bob_key, user_data)


if __name__ == "__main__":
    run()