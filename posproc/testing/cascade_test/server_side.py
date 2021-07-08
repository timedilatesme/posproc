# python -m posproc.testing.cascade_test.server_side


from posproc.networking.server import Server
from posproc.testing.cascade_test.testing_data import alice_key

def run():
    print(f'Alice\'s Key: {alice_key}')
    s = Server('Alice',alice_key)

if __name__ == "__main__":
    run()