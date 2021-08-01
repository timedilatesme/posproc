# python -m posproc.testing.speed_test.client
from posproc.networking.client import Client
from posproc.key import Random_Key_Generator

ak = Random_Key_Generator(10, 1)
b = Client("Bob", ak)

print(b.check_network_speed())
