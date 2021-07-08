# python -m posproc.testing.net_test.client
from posproc.error_correction.cascade.block import Block
from posproc.key import Key, Random_Key_Generator
from posproc.error_correction.cascade.shuffle import Shuffle
from posproc.constants import PUBLIC_SERVER, LOCAL_SERVER
from posproc.networking.client import Client
import time
import random
from posproc.testing.net_test.constant_data import bk

def test1():
    # This may not work due to some changes added to client class and server class.
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

def test2_ask_parities():
    shuffle = Shuffle(size,0)
    bk = Random_Key_Generator(size).get_random_key()
    st = time.perf_counter()
    
    c = Client('Bob',bk)
    number_of_blocks = 1000
    blocks = []
    for i in range(number_of_blocks):
        a,b = random.randint(0, size), random.randint(0, size)
        if a > b:
            sti = b
            eni = a
        elif (b>a):
            sti = a
            eni = b
        else:
            sti = 0
            eti = a
            
        blocks.append(Block(bk,shuffle,sti,eni,None))
    
    ps = c.ask_parities(blocks)
    print(ps)
    
    end = time.perf_counter()
    print(f"Finished in {end-st} second(s).")

def test3_simple_connection_for_acessing_client_socket():
    c = Client('Bob',bk)

test3_simple_connection_for_acessing_client_socket()