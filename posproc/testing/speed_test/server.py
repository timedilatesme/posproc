# python -m posproc.testing.speed_test.server
from posproc import constants
from posproc.networking.server import Server
from posproc.key import Random_Key_Generator

ak = Random_Key_Generator(10,1)
s = Server("Alice", ak)

