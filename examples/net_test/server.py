# python -m posproc.testing.net_test.server

from posproc.constants import PUBLIC_SERVER,LOCAL_SERVER
from posproc.networking.server import Server
from posproc.error_correction.cascade.shuffle import Shuffle
from posproc.testing.net_test.constant_data import ak
from posproc.testing.net_test.constant_data import*

def test2():
    s = Server('Alice',ak)

test2()
