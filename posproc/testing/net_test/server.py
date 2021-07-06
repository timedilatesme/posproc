# python -m testing.net_test.server

from posproc.constants import PUBLIC_SERVER,LOCAL_SERVER
from posproc.networking.server import Server
from posproc.error_correction.cascade.shuffle import Shuffle
from posproc.key import Key

def test2():
    ak = Key(key_as_str='1100110101')
    s = Server('Alice',ak)

test2()