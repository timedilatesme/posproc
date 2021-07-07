# python -m posproc.testing.cascade_test.server_side

from posproc.networking.server import Server
from posproc.testing.cascade_test.testing_data import*

def run():
    print(f'Alice\'s Key: {ak}')
    s = Server('Alice',ak)

if __name__ == "__main__":
    run()