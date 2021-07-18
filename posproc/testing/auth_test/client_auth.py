# python -m posproc.testing.auth_test.client_auth


from posproc.networking.client import Client
from posproc.testing.auth_test.testing_data import bob_key


def run():
    c = Client('Bob', bob_key)


if __name__ == "__main__":
    run()