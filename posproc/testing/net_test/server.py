# python -m posproc.testing.net_test.server

from posproc.constants import PUBLIC_SERVER,LOCAL_SERVER
from posproc.networking.server import Server
from posproc.error_correction.cascade.shuffle import Shuffle
from posproc.key import Key,Random_Key_Generator
from posproc.testing.net_test.constant_data import*

def test2():
    ak = Random_Key_Generator(size).get_random_key()
    s = Server('Alice',ak)

test2()
