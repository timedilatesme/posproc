# python -m posproc.testing.net_test.client
from posproc.error_correction.cascade.block import Block
from posproc.key import Key
from posproc.error_correction.cascade.shuffle import Shuffle
from posproc.constants import PUBLIC_SERVER, LOCAL_SERVER
from posproc.networking.client import Client
import time
import random


def test1():
    # This tests show that multiple clients at bob end only decrease the speed
    # of this protocol so we'll use only 1 client and only one server !        
    bob = []

    instances = int(input("number of instances: "))
    key_length = int(input("Enter Key-Length: "))
    indexes_len = int(input("Enter Indexes-Length: "))

    for i in range(instances):
        bob.append(Client())

    st = time.perf_counter()

    if instances == 1:
        bob = bob[0]
        for block_no in range(100):
            indexes = random.sample(range(key_length), k=indexes_len)
            p = bob.ask_for_parity_from_server(indexes)
            print(f"Parity is: {p}")
    else:
        for i in range(instances):
            indexes = random.sample(range(key_length),k = indexes_len)
            p = bob[i].ask_for_parity_from_server(indexes)
            print(f"Parity is: {p}")

    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")

def test2():
    shuffle = Shuffle(10,0)
    bk = Key(key_as_str = '1100110101')
    
    st = time.perf_counter()
    
    c = Client('Bob',bk)
    blocks = [Block(bk,shuffle,0,2,None),Block(bk,shuffle,8,10,None)]
    ps = c.ask_parities(blocks)
    print(ps)
    
    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")

test2()
